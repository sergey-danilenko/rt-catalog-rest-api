from app.infrastructure.di.config import ConfigProvider, DbConfigProvider
from app.infrastructure.di.db import DbProvider
from app.infrastructure.di.gateways import GatewayProvider
from app.infrastructure.di.interactors import get_interactor_providers
from app.infrastructure.di.utils import UtilsProvider


def get_providers(path_env):
    return [
        ConfigProvider(path_env),
        *get_interactor_providers(),
        DbConfigProvider(),
        DbProvider(),
        GatewayProvider(),
        UtilsProvider(),
    ]
