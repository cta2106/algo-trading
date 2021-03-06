from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import yaml

from intraday_trading.src.config.directories import directories

_BASE_CONFIG_FILENAME = "config.yml"


@dataclass(frozen=True)
class Config:
    params: Dict
    start_date_str: str
    end_date_str: str


def get_config() -> Config:
    config_filepath = directories.config / _BASE_CONFIG_FILENAME
    config = _load_config_file(config_filepath)
    return Config(**config)


def _load_config_file(path) -> Dict:
    cfg = yaml.load(Path(path).read_text(), Loader=yaml.FullLoader)
    return cfg
