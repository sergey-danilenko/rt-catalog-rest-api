from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.uow import UoW


class SQLAlchemyUoW(UoW):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def flush(self) -> None:
        await self.session.flush()
