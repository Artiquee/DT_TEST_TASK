import uvicorn
from fastapi import FastAPI
from src.spy_cat.router import router as spy_cat_router
from src.mission.router import router as mission_router

app = FastAPI()

app.include_router(spy_cat_router)
app.include_router(mission_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
