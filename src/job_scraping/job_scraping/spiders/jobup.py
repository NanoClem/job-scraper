import json
from typing import Optional

import scrapy


class JobupSpider(scrapy.Spider):
    name: str = 'jobup'
    allowed_domains: list[str] = ['www.jobup.ch']
    start_urls: list[str] = [
        'https://www.jobup.ch/api/v1/public/search?location=Lausanne&query=data%20engineer&region-ids%5B%5D=37&rows=20'
    ]

    custom_settings: Optional[dict] = {
        'ITEM_PIPELINES': {
            'job_scraping.pipelines.pipelines.JsonLoadingPipeline': 100,
        }
    }

    page_index: int = 1

    def parse(self, response):
        data = json.loads(response.body)
        yield from data['documents']

        if self.page_index < data['num_pages']:
            self.page_index += 1
            yield scrapy.Request(
                url=f'{self.start_urls[0]}&page={self.page_index}', callback=self.parse
            )
