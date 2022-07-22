import json
from typing import Iterator, Optional

import scrapy
from scrapy.http import Request, Response

import job_scraping.utils as utils
from job_scraping.configs.config import Config
from job_scraping.items import AWItem


class AcademicworkSpider(scrapy.Spider):
    name: str = 'academicwork'
    allowed_domains: list[str] = ['jobs.academicwork.ch']
    start_urls: list[str] = []

    custom_settings: Optional[dict] = {
        'ITEM_PIPELINES': {
            'job_scraping.pipelines.aw_pipelines.ValidationPipeline': 100,
            'job_scraping.pipelines.aw_pipelines.JobUrlPipeline': 200,
            'job_scraping.pipelines.pipelines.SnakeCasePipeline': 300,
            'job_scraping.pipelines.pipelines.JsonLoadingPipeline': 400,
        }
    }

    curr_cookie: dict = {}
    curr_body: dict = {}
    config: Config = None
    fields_filter: list[str] = ['JobCity','Requirements', 'ExtentOfWork', 'PublishDate', 'JobRef', 
                                'Saved', 'Applied', 'NewLogoUrl', 'JobAdvertEntityId', 'JobTag']

    def make_request(self) -> Request:
        return Request(
            url=self.config.base_url,
            method='POST',
            headers=self.config.headers,
            body=json.dumps(self.curr_body),
            cookies=self.curr_cookie,
            callback=self.parse,
        )

    def start_requests(self) -> Iterator[Request]:
        self.config = Config.load_configs(self.name)
        self.curr_cookie = utils.parse_cookie(self.config.raw_cookie)
        self.curr_body = self.config.payload.copy()
        yield self.make_request()

    def parse(self, response: Response):
        data = json.loads(response.body.decode('utf-8'))
        for job_add in data['Adverts']:
            item = AWItem.construct(**{k: v for k, v in job_add.items() if k not in self.fields_filter})
            yield item.dict()

        if self.curr_body['StartIndex'] < data['TotalIndexes'] - 1:
            self.curr_body['StartIndex'] += 1
            yield self.make_request()
