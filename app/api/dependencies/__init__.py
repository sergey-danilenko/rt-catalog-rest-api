from app.api.dependencies.config import ConfigProvider


def get_api_providers():
    return [
        ConfigProvider(),
    ]
