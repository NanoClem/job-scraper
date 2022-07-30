import json
from typing import Optional

import scrapy

from job_scraping.items import JobItem


class JobupSpider(scrapy.Spider):
    name: str = 'jobup'
    allowed_domains: list[str] = ['www.jobup.ch']
    start_urls: list[str] = [
        'https://www.jobup.ch/api/v1/public/search?location=Lausanne%20OR%20Gen%C3%A8ve&query=IT&rows=20'
    ]

    custom_settings: Optional[dict] = {
        'ITEM_PIPELINES': {
            'job_scraping.pipelines.ValidationPipeline': 100,
            'job_scraping.pipelines.SqlLoadingPipeline': 200,
            # 'job_scraping.pipelines.JsonLoadingPipeline': 200,
        }
    }

    page_index: int = 0

    def parse(self, response):
        data = json.loads(response.body)

        for job in data['documents']:
            item = JobItem.construct(
                job_id=job.get('job_id'),
                title=job.get('title'),
                slug=job.get('slug'),
                url=job.get('_links').get('detail_en').get('href'),
                source_website=self.name,
                employment_type=job.get('employment_type_ids', list())[0],
                employment_rate=job.get('employment_grades', list())[0],
                job_category='',
                job_extent=str(job.get('employment_grades', list())[0]),
                description=job.get('preview'),
                location=job.get('place'),
                publication_date=job.get('publication_date'),
                company=job.get('company_name'),
            )
            yield item.dict()

        if self.page_index < data['num_pages']:
            self.page_index += 1
            yield scrapy.Request(
                url=f'{self.start_urls[0]}&page={self.page_index}', callback=self.parse
            )
