from typing import TypeVar, Generic, Sequence

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from app.infrastructure.db.models import Base

Model_co = TypeVar("Model_co", bound=Base, covariant=True, contravariant=False)


class BaseGateway(Generic[Model_co]):
    def __init__(
        self,
        model: type[Model_co],
        session: AsyncSession,
    ):
        self.model = model
        self.session = session

    async def _get_by_id(
        self, id_: int, options: Sequence[ORMOption] = None,
    ) -> Model_co:
        result = await self.session.get(
            self.model, id_, options=options,
        )
        return result

    async def _get_all(
        self, options: Sequence[ORMOption] = None,
    ) -> Sequence[Model_co]:
        query = select(self.model)
        if options:
            query = query.options(*options)
        result: ScalarResult[Model_co] = await self.session.scalars(query)
        return result.all()

    def _add(self, obj: Base):
        self.session.add(obj)

    def _add_all(self, *objects: Base):
        self.session.add_all(objects)

    async def commit(self):
        await self.session.commit()

    async def _flush(self, *objects: Base):
        await self.session.flush(objects)
