from dataclasses import dataclass
from pathlib import Path


@dataclass
class Paths:
    app_dir: Path

    @property
    def config_path(self) -> Path:
        return self.app_dir / "config"

    @property
    def config_file(self) -> Path:
        return self.config_path / "config.yml"

    @property
    def logging_config_file(self) -> Path:
        return self.config_path / "logging.yml"
