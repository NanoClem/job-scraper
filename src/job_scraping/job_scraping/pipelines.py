import json
import sqlite3
from datetime import datetime
from collections import defaultdict

import scrapy
from pydantic import ValidationError

import job_scraping.utils as utils
from job_scraping.items import JobItem


class ValidationPipeline:
    """Data validation pipeline according to defined item model."""

    @utils.logged
    def process_item(self, item, spider: scrapy.Spider):
        try:
            JobItem.validate(item)
        except ValidationError as validErr:
            item["_validation"] = defaultdict(list)
            for err in validErr.errors():
                field_name = "/".join(str(loc) for loc in err["loc"])
                item["_validation"][field_name] = err["msg"]
        return item


class JsonLoadingPipeline:
    """Load incoming item into a jsonlines file."""

    def open_spider(self, spider: scrapy.Spider) -> None:
        load_path = utils.get_src_path() / 'data' / spider.name
        load_path.mkdir(parents=True, exist_ok=True)
        filename = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonlines'
        self.file = open(load_path / filename, 'w', encoding='utf-8')

    def close_spider(self, spider: scrapy.Spider) -> None:
        self.file.close()

    @utils.logged
    def process_item(self, item, spider: scrapy.Spider):
        line = (json.dumps(item, ensure_ascii=False) + "\n")  # ensure utf-8 encoding
        self.file.write(line)
        return item


class SqlLoadingPipeline:
    """Load incoming item into a sqlite database."""

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS jobs(
                job_id VARCHAR(50) PRIMARY KEY NOT NULL,
                title VARCHAR(50),
                slug VARCHAR(50),
                url VARCHAR(50),
                source_website VARCHAR(50),
                employment_type VARCHAR(50),
                job_category VARCHAR(50),
                job_extent VARCHAR(50),
                description VARCHAR(210),
                location VARCHAR(50),
                publication_date VARCHAR(50),
                employment_rate INT,
                company VARCHAR(50)
            )"""
        )

    def open_spider(self, spider: scrapy.Spider) -> None:
        self.con = sqlite3.connect('jobs.db')
        self.cur = self.con.cursor()
        self.create_table()

    def close_spider(self, spider: scrapy.Spider) -> None:
        self.con.commit()
        self.con.close()

    @utils.logged
    def process_item(self, item, spider: scrapy.Spider):
        self.cur.execute(
            """INSERT OR IGNORE INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            tuple(val for val in item.values()),
        )
        return item
