import json
from typing import Iterator, Optional

import scrapy
from scrapy.http import Request, Response

import job_scraping.utils as utils
from job_scraping.configs.config import Config
from job_scraping.items import AWItem


class AcademicworkSpider(scrapy.Spider):
    name: str = 'academicwork'
    allowed_domains: dict[str] = ['jobs.academicwork.ch']
    start_urls: dict[str] = []

    custom_settings: Optional[dict] = {
        'ITEM_PIPELINES': {
            'job_scraping.pipelines.AWValidationPipeline': 100,
            'job_scraping.pipelines.JsonLoadingPipeline': 200,
        }
    }

    cookie: dict = {}
    curr_body: dict = {}
    config: Config = None

    def make_request(self) -> Request:
        return Request(
            url=self.config.base_url,
            method='POST',
            headers=self.config.headers,
            body=json.dumps(self.curr_body),
            cookies=self.cookie,
            callback=self.parse,
        )

    def start_requests(self) -> Iterator[Request]:
        self.config = Config.load_configs(self.name)
        self.cookie = utils.parse_cookie(self.config.raw_cookie)
        self.curr_body = self.config.payload.copy()
        yield self.make_request()

    def parse(self, response: Response):
        data = json.loads(response.body.decode('utf-8'))
        for job_add in data['Adverts']:
            item = AWItem.construct(**job_add)
            yield item.dict()

        if self.curr_body['StartIndex'] < data['TotalIndexes'] - 1:
            self.curr_body['StartIndex'] += 1
            yield self.make_request()
