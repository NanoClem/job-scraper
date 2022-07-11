import os
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

import yaml


@dataclass
class QueryItems:

    type: str
    value: str
    id: str


@dataclass
class Payload:

    sort: Optional[str]
    ascending: Optional[bool]
    searchQueryItems: list[QueryItems] = field(default_factory=list)


@dataclass
class Config:

    base_url: str
    payload: Payload
    headers: dict = field(default_factory=dict)

    def to_dict(self):
        """d"""
        return asdict(self)

    @classmethod
    def load_configs(cls, conf_path: str | Path) -> 'Config':
        """d"""
        # Default configuration
        if not os.path.exists(conf_path):
            conf_path = Path(__file__).parent / 'default_config.yml'

        logging.info(f'Loading config file {conf_path}')
        try:
            with open(conf_path, 'r', encoding='utf-8') as conf_file:
                yml_conf = yaml.safe_load(conf_file.read())
        except IOError as err:
            logging.error(err)
            raise IOError(err)

        return cls(**yml_conf)
