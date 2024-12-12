from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import CatRepository
from .service import CatService
from ..database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_cat_service(db: AsyncSession = Depends(get_db)) -> CatService:
    repository = CatRepository(db)
    return CatService(repository)
