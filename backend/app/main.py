from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.settings import settings


app = FastAPI(
    title=settings.PROJECT_NAME
)

settings.RAW_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

app.mount(
    "/documents",
    StaticFiles(directory=settings.RAW_DATA_DIR),
    name="documents",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
