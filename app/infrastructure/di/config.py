from dishka import Provider, Scope, provide

from app.common.config import (
    Config, Paths, DbConfig,
)
from app.common.config import load_config
from app.common.config import common_get_paths


class ConfigProvider(Provider):
    scope = Scope.APP

    def __init__(self, path_env: str = "APP_DIR"):
        super().__init__()
        self.path_env = path_env

    @provide
    def get_paths(self) -> Paths:
        return common_get_paths(self.path_env)

    @provide
    def get_config(self, paths: Paths) -> Config:
        return load_config(paths)


class DbConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_config(self, config: Config) -> DbConfig:
        return config.db
