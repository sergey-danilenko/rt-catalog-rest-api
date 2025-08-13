from app.api.config.models import ApiConfig, AuthConfig
from app.common.common import dcf
from app.common.config import (
    Paths,
    read_config,
    load_config as load_common_config,
)


def load_auth_config(auth_data: dict) -> AuthConfig:
    return dcf.make_dataclass(AuthConfig, auth_data)


def load_config(paths: Paths) -> ApiConfig:
    config_data = read_config(paths=paths)
    return ApiConfig.from_base(
        base=load_common_config(paths, config_data),
        auth=load_auth_config(config_data["api"]["auth"]),
    )
