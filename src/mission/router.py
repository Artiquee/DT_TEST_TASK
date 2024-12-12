from fastapi import APIRouter, Depends, HTTPException
from .schemas import TargetBase, MissionSchema, MissionUpdate, TargetUpdate
from .dependencies import get_mission_service
from .service import MissionService


router = APIRouter()


@router.get("/missions/")
async def get_missions(
        mission_service: MissionService = Depends(get_mission_service)
):
    mission = await mission_service.get_missions()
    return mission


@router.get("/mission/{mission_id}")
async def get_mission(
        mission_id: int,
        mission_service: MissionService = Depends(get_mission_service)
):
    mission = await mission_service.get_mission(mission_id)
    return mission


@router.post("/missions/")
async def create_mission(
        mission_data: MissionSchema,
        mission_service: MissionService = Depends(get_mission_service)
):
    mission = await mission_service.add_mission(mission_data)
    return mission


@router.put("/missions/{mission_id}", response_model=MissionUpdate)
async def update_mission(
        mission_id: int,
        updated_data: MissionUpdate,
        mission_service: MissionService = Depends(get_mission_service)
):
    mission = await mission_service.update_mission(mission_id, updated_data)
    return mission


@router.delete("/missions/{mission_id}", response_model=dict)
async def delete_mission(
        mission_id: int,
        mission_service: MissionService = Depends(get_mission_service)
):
    mission = await mission_service.delete_mission(mission_id)
    return {"detail": "Mission deleted successfully"}


@router.put("/missions/{mission_id}/assign-cat/{cat_id}", response_model=MissionUpdate)
async def assign_cat_to_mission(
    mission_id: int,
    cat_id: int,
    mission_service: MissionService = Depends(get_mission_service),
):

    mission = await mission_service.assign_cat_to_mission(mission_id, cat_id)
    if not mission:
        raise HTTPException(status_code=400, detail="Cannot assign cat to mission")
    return mission


@router.put("/missions/{mission_id}/targets/{target_id}/complete", response_model=TargetBase)
async def complete_target(
    mission_id: int,
    target_id: int,
    mission_service: MissionService = Depends(get_mission_service)
):
    target = await mission_service.complete_target(mission_id, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target or Mission not found")
    return {'mission': "Completed mission successfully", 'target': target}


@router.put("/missions/{mission_id}/targets/{target_id}/notes", response_model=TargetBase)
async def update_target_notes(
    mission_id: int,
    target_id: int,
    notes: TargetUpdate,
    mission_service: MissionService = Depends(get_mission_service)
):
    target = await mission_service.target_service.update_notes(mission_id, target_id, notes.notes)
    return target
