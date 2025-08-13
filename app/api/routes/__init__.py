from fastapi import APIRouter, Depends

from app.api.dependencies.auth import check_api_key
from app.api.routes import (
    organization,
)


def setup() -> APIRouter:
    router = APIRouter(
        dependencies=[Depends(check_api_key)]
    )
    router.include_router(organization.setup())
    return router
