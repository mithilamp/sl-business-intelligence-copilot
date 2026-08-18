from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.settings import settings


app = FastAPI(
    title=settings.PROJECT_NAME
)


app.mount(
    "/documents",
    StaticFiles(directory=settings.RAW_DATA_DIR),
    name="documents",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)