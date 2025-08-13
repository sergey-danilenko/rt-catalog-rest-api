from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi.security import APIKeyHeader

from app.api.config import AuthConfig
from fastapi import HTTPException, status, Security

api_key_header = APIKeyHeader(
    name="X-API-KEY",
    auto_error=False,
    description="Укажите ваш статический API ключ для доступа к API"
)


@inject
async def check_api_key(
    config: FromDishka[AuthConfig],
    api_key: str = Security(api_key_header),
):
    if api_key != config.static_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",

        )
