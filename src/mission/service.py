from fastapi import HTTPException
from starlette import status
from src.mission.models import Target, Mission
from src.mission.repository import MissionRepository, TargetMissionRepository
from src.spy_cat.repository import CatRepository


class TargetService:
    def __init__(self, target_mission_repository: TargetMissionRepository):
        self.target_mission_repository = target_mission_repository

    async def add_targets(self, mission_id: int, targets: list):
        targets_obj = [
            Target(
                mission_id=mission_id,
                name=target.name,
                country=target.country
            )
            for target in targets
        ]
        await self.target_mission_repository.add_target(targets_obj)

    async def mark_target_completed(self, mission_id: int, target_id: int):
        target = await self.target_mission_repository.get_target_by_id_and_mission(mission_id, target_id)
        if not target:
            raise HTTPException(status_code=404, detail="Target not found")

        if target.complete:
            raise HTTPException(status_code=400, detail="Target is already completed")

        target.complete = True
        self.target_mission_repository.db_session.add(target)
        await self.target_mission_repository.db_session.commit()
        await self.target_mission_repository.db_session.refresh(target)
        return target

    async def get_remaining_targets(self, mission_id: int):
        targets = await self.target_mission_repository.get_targets_by_mission_id(mission_id)
        return [target for target in targets if not target.complete]

    async def update_notes(self, mission_id: int, target_id: int, notes: str):
        target = await self.target_mission_repository.get_target_by_id_and_mission(mission_id, target_id)
        if not target:
            raise HTTPException(status_code=404, detail="Target not found")

        if target.complete:
            raise HTTPException(status_code=400, detail="Cannot update notes for a completed target")

        mission = await self.target_mission_repository.get_mission_by_id(mission_id)
        if not mission:
            raise HTTPException(status_code=404, detail="Mission not found")

        if mission.is_complete:
            raise HTTPException(status_code=400, detail="Cannot update notes for a target in a completed mission")

        target.notes = notes
        self.target_mission_repository.db_session.add(target)
        await self.target_mission_repository.db_session.commit()
        await self.target_mission_repository.db_session.refresh(target)
        return target


class MissionService:
    def __init__(self, mission_repository: MissionRepository, target_service: TargetService, cat_repository: CatRepository):
        self.mission_repository = mission_repository
        self.target_service = target_service
        self.cat_repository = cat_repository

    async def get_mission(self, mission_id):
        mission = await self.mission_repository.get_mission_by_id(mission_id)
        return mission

    async def get_missions(self):
        missions = await self.mission_repository.get_missions()
        return missions

    async def add_mission(self, mission_data):
        existing_mission = await self.mission_repository.get_mission_by_name(mission_data.name)
        if existing_mission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mission already exists"
            )
        if mission_data.cat_id and await self.mission_repository.get_mission_by_cat_id(mission_data.cat_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cat mission already exists"
            )

        if len(mission_data.targets) > 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Too many targets"
            )

        new_mission = Mission(
            name=mission_data.name,
            cat_id=mission_data.cat_id
        )
        await self.mission_repository.add_mission(new_mission)

        created_mission = await self.mission_repository.get_mission_by_name(mission_data.name)
        mission_id = created_mission.id

        await self.target_service.add_targets(mission_id, mission_data.targets)

        return {"mission_name": new_mission.name, "mission_id": mission_id}

    async def delete_mission(self, mission):
        mission = await self.mission_repository.get_mission_by_name(mission_name=mission.name)
        if mission.cat_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete already started mission")

        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
            )

        await self.mission_repository.delete_mission(mission)

    async def update_mission(self, mission_id, updated_mission):
        mission = await self.mission_repository.get_mission_by_id(mission_id)
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
            )
        updated_mission = await self.mission_repository.update_mission(mission, updated_mission)
        return updated_mission

    async def complete_target(self, mission_id: int, target_id: int):
        target = await self.target_service.mark_target_completed(mission_id, target_id)
        if not target:
            raise HTTPException(status_code=404, detail="Target not found")

        remaining_targets = await self.target_service.get_remaining_targets(mission_id)
        if not remaining_targets:
            await self.mission_repository.mark_mission_completed(mission_id)

        return target

    async def assign_cat_to_mission(self, mission_id: int, cat_id: int):
        mission = await self.mission_repository.get_mission_by_id(mission_id)
        if not mission:
            raise HTTPException(
                status_code=404,
                detail="Mission not found"
            )

        cat = await self.cat_repository.get_cat_by_id(cat_id)
        if not cat:
            raise HTTPException(
                status_code=404,
                detail="Cat not found"
            )

        if mission.cat_id:
            raise HTTPException(
                status_code=400,
                detail="Mission already assigned to a cat"
            )

        mission.cat_id = cat_id
        updated_mission = await self.mission_repository.update_mission(mission, {"cat_id": cat_id})
        return updated_mission
