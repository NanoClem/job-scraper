import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Iterable

import requests as rq

import models as mdl
from config import Config

# ENABLE LOGGING
logging.basicConfig(
    filename='scrap.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(levelname)s %(asctime)s %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
)


def extract(session: rq.Session, base_url: str, headers: dict, payload: dict) -> dict:
    """d"""
    with session.post(base_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        result = response.content.decode('utf-8')
    return json.loads(result)['Adverts']


def parse(data: dict) -> Iterable[mdl.BaseModel]:
    """d"""
    return (mdl.AWModel(**d) for d in data)


def load(load_path: Path, parsed_data: Iterable[mdl.BaseModel]) -> None:
    """d"""
    load_path.mkdir(parents=True, exist_ok=True)
    filename = load_path / f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    try:
        with open(filename, 'w', encoding='utf-8') as json_f:
            logging.info(f'Writing data to {filename}')
            json.dump(
                [parsed.dict() for parsed in parsed_data],
                json_f,
                indent=4,
                ensure_ascii=False,
            )
    except IOError as err:
        logging.error(f'{err} | data loading failed for {filename}')


if __name__ == "__main__":

    # -----------------
    #   Load configs
    # -----------------
    CONFIG = Config.load_configs(Path(__file__).parent / 'config.yml')

    # -----------------
    #   ETL job
    # -----------------
    with rq.Session() as session:
        # ... get cookie
        raw_data = extract(session, **CONFIG.to_dict())

    parsed = parse(raw_data)

    load_path = Path(__file__).parent / 'data' / 'AW'
    load(load_path, parsed)
