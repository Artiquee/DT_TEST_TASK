from pydantic import BaseModel
from typing import List, Optional


class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    is_completed: bool = False


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_completed: Optional[bool] = None


class Target(TargetBase):

    class Config:
        orm_mode = True


class MissionSchema(BaseModel):
    name: str
    is_completed: bool = False
    cat_id: int = None
    targets: List[Target] = []


class MissionUpdate(BaseModel):
    name: Optional[str] = None
    is_completed: Optional[bool] = None

