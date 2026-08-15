from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="SL Business Intelligence Copilot"
)

app.include_router(router)