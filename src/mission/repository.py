from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Mission, Target


class MissionRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_mission_by_id(self, mission_id: int) -> Mission:
        mission = await self.db_session.execute(select(Mission).where(Mission.id == mission_id))
        return mission.scalar_one_or_none()

    async def get_mission_by_name(self, mission_name: str) -> Mission:
        result = await self.db_session.execute(select(Mission).where(Mission.name == mission_name))
        return result.scalar_one_or_none()

    async def get_mission_by_cat_id(self, cat_id: int) -> Mission:
        cat = await self.db_session.execute(select(Mission).where(Mission.cat_id == cat_id))
        return cat.scalar_one_or_none()

    async def get_missions(self):
        missions = await self.db_session.execute(select(Mission))
        return missions.scalars().all()

    async def add_mission(self, mission: Mission):
        self.db_session.add(mission)
        await self.db_session.commit()
        return Mission.name

    async def update_mission(self, mission: Mission, updated_data: dict) -> Mission:
        for key, value in updated_data.items():
            setattr(mission, key, value)
        self.db_session.add(mission)
        await self.db_session.commit()
        await self.db_session.refresh(mission)
        return mission

    async def delete_mission(self, mission):
        await self.db_session.delete(mission)
        await self.db_session.commit()

    async def mark_mission_completed(self, mission_id: int):
        mission = await self.get_mission_by_id(mission_id)
        if mission:
            mission.is_completed = True
            self.db_session.add(mission)
            await self.db_session.commit()
            return True
        return False

    async def assign_cat_to_mission(self, mission: Mission, cat_id: int):
        mission.cat_id = cat_id
        self.db_session.add(mission)
        await self.db_session.commit()
        await self.db_session.refresh(mission)
        return mission


class TargetMissionRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_target(self, target_data):
        self.db_session.add_all(target_data)
        await self.db_session.commit()
        return True

    async def get_targets_by_mission_id(self, mission_id):
        targets = await self.db_session.execute(select(Target).where(Target.mission_id == mission_id))
        return targets.scalars().all()

    async def get_target_by_id_and_mission(self, mission_id: int, target_id: int):
        result = await self.db_session.execute(
            select(Target).where(Target.mission_id == mission_id, Target.id == target_id)
        )
        return result.scalar_one_or_none()

    async def get_mission_by_id(self, mission_id: int) -> Mission:
        mission = await self.db_session.execute(select(Mission).where(Mission.id == mission_id))
        return mission.scalar_one_or_none()
