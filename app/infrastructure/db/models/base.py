from sqlalchemy.orm import DeclarativeBase
from typing_extensions import Annotated

from sqlalchemy import MetaData, String
from sqlalchemy.orm import registry
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from sqlalchemy.orm import mapped_column

from datetime import datetime


class UTSnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(UTSnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(UTSnow, 'sqlite')
def sqlite_utcnow(element, compiler, **kw):
    return "CURRENT_TIMESTAMP"


UTC_datetime = Annotated[
    datetime,
    mapped_column(server_default=UTSnow()),
]

UTC_update = Annotated[
    datetime,
    mapped_column(default=datetime(1900, 1, 1, 00, 00, 00, 00000),
                  onupdate=UTSnow(), nullable=True),
]

convention = {
    'ix': 'ix__%(column_0_label)s',
    'uq': 'uq__%(table_name)s__%(column_0_name)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(column_0_name)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}
my_metadata = MetaData(naming_convention=convention)

str_5 = Annotated[str, 5]
str_10 = Annotated[str, 10]
str_30 = Annotated[str, 30]
str_50 = Annotated[str, 50]
str_100 = Annotated[str, 100]
str_150 = Annotated[str, 150]
str_200 = Annotated[str, 200]


class Base(DeclarativeBase):
    metadata = my_metadata
    registry = registry(
        type_annotation_map={
            str_5: String(5),
            str_10: String(10),
            str_30: String(30),
            str_50: String(50),
            str_100: String(100),
            str_150: String(150),
            str_200: String(200),
            UTC_datetime: DateTime(),
            UTC_update: DateTime(),
        }
    )
