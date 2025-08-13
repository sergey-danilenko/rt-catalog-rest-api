import logging

from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession,
)
from sqlalchemy.engine import make_url

from app.common.config import DbConfig

logger = logging.getLogger(__name__)


def create_alembic_url(
    db_config: DbConfig,
    async_fallback: bool = False,
) -> str:
    uri = db_config.uri
    if db_config.type in ("mysql", "postgresql"):
        if async_fallback:
            uri += "?async_fallback=True"
    elif db_config.type == "sqlite":
        uri = f"{db_config.type}:///{db_config.dbname}"
    return uri


def create_engine(db_config: DbConfig, echo: bool = False) -> AsyncEngine:
    url = make_url(db_config.uri)
    logger.info("Sqlalchemy URL: %s", url)
    return create_async_engine(
        url=url,
        echo=echo if echo else db_config.echo,
        pool_pre_ping=db_config.pool_pre_ping,
    )


def create_session_maker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, future=True, autoflush=False
    )
    return pool
