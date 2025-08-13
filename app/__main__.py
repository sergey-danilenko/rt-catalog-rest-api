import logging

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.api import routes
from app.api.config.models import ApiConfig
from app.api.config.setup_config import load_config
from app.api.dependencies import get_api_providers
from app.common.config import get_paths, setup_logging
from app.infrastructure.di import get_providers

logger = logging.getLogger(__name__)


def create_app(config: ApiConfig) -> FastAPI:
    app = FastAPI(
        title=f"Тестовое REST API приложение: {config.app.name}",
        version="1.0.0",
        description="""
        Взаимодействие с пользователем посредством HTTP запросов к API серверу
        с использованием статического API ключа.
        Все ответы в формате JSON.
        """
    )
    app.include_router(routes.setup())
    return app


def main():
    paths = get_paths()
    setup_logging(paths)
    config: ApiConfig = load_config(paths)
    dishka = make_async_container(
        *get_providers("APP_DIR"),
        *get_api_providers(),
    )
    app = create_app(config=config)
    setup_dishka(dishka, app)
    return app


def run():
    uvicorn.run(
        main(),
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, SystemExit) as e:
        logger.error("Server was interrupted with error: %s", e)
    except Exception as e:  # Noqa
        logger.exception("An unexpected error occurred: %s", e)
    finally:
        logger.warning(f"\n\nServer stopped!!!\n")
