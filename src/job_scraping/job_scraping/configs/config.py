import os
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict

import yaml


@dataclass
class Config:

    base_url: str
    raw_cookie: str = ''
    headers: dict = field(default_factory=dict)
    payload: dict = field(default_factory=dict)

    def to_dict(self):
        """d"""
        return asdict(self)

    @classmethod
    def load_configs(cls, name: str) -> 'Config':
        """Load configs from given spider name."""
        conf_file = (Path(__file__).parent / f'{name}_config.yml').resolve()
        logging.info(f'Loading config file {conf_file}')

        if not os.path.exists(conf_file):
            error = f'File {conf_file} not found'
            logging.error(error)
            raise FileNotFoundError(error)

        try:
            with open(conf_file, 'r', encoding='utf-8') as yml_file:
                yml_conf = yaml.safe_load(yml_file.read())
        except IOError as err:
            logging.error(err)
            raise IOError(err)

        return cls(**yml_conf)
