from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import MissionRepository, TargetMissionRepository
from .service import MissionService, TargetService
from ..database import get_db
from ..spy_cat.repository import CatRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_mission_service(db: AsyncSession = Depends(get_db)) -> MissionService:
    mission_repository = MissionRepository(db)
    target_repository = TargetMissionRepository(db)
    target_service = TargetService(target_repository)
    cat_repository = CatRepository(db)
    return MissionService(mission_repository, target_service, cat_repository)

