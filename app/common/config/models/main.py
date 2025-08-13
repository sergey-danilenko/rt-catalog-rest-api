import logging
from dataclasses import dataclass

from .paths import Paths

logger = logging.getLogger(__name__)


@dataclass
class DbConfig:
    type: str
    connector: str
    user: str
    password: str
    host: str
    port: int
    dbname: str
    path: str | None = None
    echo: bool = False
    pool_pre_ping: bool = False

    @property
    def uri(self):
        if self.type in ("mysql", "postgresql"):
            url = (
                f"{self.type}+{self.connector}://"
                f"{self.user}:{self.password}"
                f"@{self.host}:{self.port}/{self.dbname}"
            )
        elif self.type == "sqlite":
            url = f"{self.type}+{self.connector}:///{self.path}/{self.dbname}"
        else:
            raise ValueError("DB_TYPE not mysql, sqlite or postgres")
        logger.debug(url)
        return url


@dataclass
class AppConfig:
    name: str


@dataclass
class Config:
    app: AppConfig
    paths: Paths
    db: DbConfig
