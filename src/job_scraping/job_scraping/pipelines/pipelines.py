import json
from datetime import datetime

import scrapy

import job_scraping.utils as utils


class SnakeCasePipeline:
    def process_item(self, item, spider: scrapy.Spider) -> None:
        return {utils.to_snake_case(k): v for k, v in item.items()}


class JsonLoadingPipeline:
    def open_spider(self, spider: scrapy.Spider) -> None:
        load_path = utils.get_src_path() / 'data' / spider.name
        filename = load_path / f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonlines'
        load_path.mkdir(parents=True, exist_ok=True)
        self.file = open(filename, 'w', encoding='utf-8')

    def close_spider(self, spider: scrapy.Spider) -> None:
        self.file.close()

    @utils.logged
    def process_item(self, item, spider: scrapy.Spider):
        line = (
            json.dumps(item, ensure_ascii=False) + "\n"
        )  # ensure utf-8 encoding when writing in file
        self.file.write(line)
        return item
