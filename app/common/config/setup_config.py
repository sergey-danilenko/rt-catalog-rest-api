import logging

from app.common.common import dcf
from app.common.config.config_reader import read_config
from app.common.config.models.paths import Paths
from app.common.config.models.main import Config, DbConfig

logger = logging.getLogger(__name__)


def load_db_config(db_data: dict) -> DbConfig:
    return dcf.make_dataclass(DbConfig, db_data)


def load_config(paths: Paths, config_data: dict = None) -> Config:
    if config_data is None:
        config_data = read_config(paths=paths)
    config: Config = dcf.make_dataclass(Config, config_data)
    config.paths = paths
    config.db.path = paths.app_dir.as_posix()
    logger.info("Config loading successfully %s", config)
    return config
