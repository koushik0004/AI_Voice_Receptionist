from fastapi import FastAPI

from app.api.routes import router
from app.core.settings import settings

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
)

app.include_router(router)
