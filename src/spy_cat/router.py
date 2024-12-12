from fastapi import APIRouter, Depends, HTTPException
from typing import List
from starlette import status
from .schemas import SpySchema, SpySchemaUpdate, AllCatsSchema
from .dependencies import get_cat_service
from .service import CatService

router = APIRouter()


@router.get("/cats", response_model=List[AllCatsSchema])
async def get_cats(
        cat_service: CatService = Depends(get_cat_service)
):
    cats = await cat_service.get_cats()
    return cats


@router.get("/cats/{cat_id}")
async def get_cat(
        cat_id: int,
        cat_service: CatService = Depends(get_cat_service)
):
    cat = await cat_service.get_cat(cat_id)
    return cat


@router.post("/cats")
async def add_cat(
        cat_data: SpySchema,
        cat_service: CatService = Depends(get_cat_service)
):
    cat = await cat_service.add_cat(cat_data)
    return HTTPException(status_code=status.HTTP_201_CREATED, detail=f"{cat} is added")


@router.put("/cats/{cat_id}", response_model=SpySchema)
async def update_cat(
        cat_id: int,
        updated_data: SpySchemaUpdate,
        cat_service: CatService = Depends(get_cat_service)
):
    cat = await cat_service.update_cat(cat_id, updated_data)
    return cat


@router.delete("/cats/{cat_id}", status_code=status.HTTP_204_NO_CONTENT, description="Cat deleted successfully")
async def delete_cat(
        cat_id: int,
        cat_service: CatService = Depends(get_cat_service)
):
    await cat_service.delete_cat(cat_id)
    return {"detail": "Cat deleted successfully"}


@router.post("/cats/notes", response_model=List[SpySchema])
async def add_notes(
        note_data: dict
):
    notes = note_data["notes"]
    return notes
