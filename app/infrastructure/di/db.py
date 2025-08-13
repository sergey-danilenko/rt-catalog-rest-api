from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from app.common.config import DbConfig
from app.core.interfaces.uow import UoW
from app.infrastructure.db.factory import (
    create_engine, create_session_maker,
)
from app.infrastructure.db.sqlalchemy_uow import SQLAlchemyUoW


class DbProvider(Provider):
    scope = Scope.APP

    def __init__(self, echo: bool = False):
        super().__init__()
        self.echo = echo

    @provide
    async def get_engine(
        self, db_config: DbConfig,
    ) -> AsyncIterable[AsyncEngine]:
        engine = create_engine(db_config, self.echo)
        yield engine
        await engine.dispose(True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, pool: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_uow(self, session: AsyncSession) -> UoW:
        return SQLAlchemyUoW(session)
