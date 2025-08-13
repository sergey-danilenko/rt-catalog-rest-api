from dishka import Provider, Scope, provide

from app.api.config import ApiConfig, AuthConfig, load_config
from app.common.config import Paths


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_config(self, paths: Paths) -> ApiConfig:
        return load_config(paths)

    @provide
    def get_auth_config(self, config: ApiConfig) -> AuthConfig:
        return config.auth
