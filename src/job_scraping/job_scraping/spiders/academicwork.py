import json
from typing import Iterator, Optional

import scrapy
from scrapy.http import Request, Response

import job_scraping.utils as utils
from job_scraping.configs.config import Config
from job_scraping.items import JobItem


class AcademicworkSpider(scrapy.Spider):
    name: str = 'academicwork'
    allowed_domains: list[str] = ['jobs.academicwork.ch']
    start_urls: list[str] = []

    custom_settings: Optional[dict] = {
        'ITEM_PIPELINES': {
            'job_scraping.pipelines.ValidationPipeline': 100,
            'job_scraping.pipelines.SqlLoadingPipeline': 200,
            # 'job_scraping.pipelines.JsonLoadingPipeline': 400,
        }
    }

    curr_cookie: dict = {}
    curr_body: dict = {}
    config: Config = None

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
        data: dict = json.loads(response.body.decode('utf-8'))

        for job in data.get('Adverts', list()):
            item = JobItem.construct(
                job_id=str(job.get('Id')),
                title=job.get('JobTitle'),
                slug=job.get('Slug'),
                url=f'https://{self.allowed_domains[0]}/job-list/{job.get("Slug")}/{job.get("Id")}',
                source_website=self.name,
                employment_type=job.get('OrderType'),
                job_category=job.get('Category'),
                job_extent=job.get('WorkExtent'),
                description=job.get('LeadIn'),
                location=job.get('Location'),
                publication_date=job.get('CreatedDate'),
            )
            yield item.dict()

        if self.curr_body['StartIndex'] < data['TotalIndexes'] - 1:
            self.curr_body['StartIndex'] += 1
            yield self.make_request()
