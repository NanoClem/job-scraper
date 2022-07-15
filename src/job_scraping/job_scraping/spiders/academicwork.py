import json
from http.cookies import SimpleCookie
from typing import Iterator

import scrapy
from scrapy.http import Request, Response

from job_scraping.configs.config import Config


class AcademicworkSpider(scrapy.Spider):
    name: str = 'academicwork'
    allowed_domains: dict[str] = ['jobs.academicwork.ch']
    start_urls: dict[str] = []

    cookie: dict = {}
    config: Config = None

    def parse_cookie(self) -> None:
        cookie_parser = SimpleCookie()
        cookie_parser.load(self.config.raw_cookie)
        self.cookie = {k: v.value for k, v in cookie_parser.items()}

    def make_request(self) -> Request:
        return Request(
            url=self.config.base_url,
            method='POST',
            headers=self.config.headers,
            body=json.dumps(self.config.payload),
            cookies=self.cookie,
            callback=self.parse,
        )

    def start_requests(self) -> Iterator[Request]:
        self.config = Config.load_configs(self.name)
        self.parse_cookie()
        yield self.make_request()

    def parse(self, response: Response):
        data = json.loads(response.body.decode('utf-8'))
        yield from data['Adverts']

        if self.config.payload['StartIndex'] < data['TotalIndexes'] - 1:
            self.config.payload['StartIndex'] += 1
            yield self.make_request()
