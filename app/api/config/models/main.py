from __future__ import annotations

from dataclasses import dataclass

from app.common.config import Config


@dataclass
class AuthConfig:
    static_key: str


@dataclass
class ApiConfig(Config):
    auth: AuthConfig

    @classmethod
    def from_base(
        cls,
        base: Config,
        auth: AuthConfig,
    ) -> ApiConfig:
        return cls(
            app=base.app,
            paths=base.paths,
            db=base.db,
            auth=auth,
        )
