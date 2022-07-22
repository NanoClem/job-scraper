from collections import defaultdict

import scrapy
from pydantic import ValidationError

import job_scraping.utils as utils
from job_scraping.items import AWItem


class ValidationPipeline:
    @utils.logged
    def process_item(self, item, spider: scrapy.Spider):
        try:
            AWItem.validate(item)
        except ValidationError as validErr:
            item["_validation"] = defaultdict(list)
            for err in validErr.errors():
                field_name = "/".join(str(loc) for loc in err["loc"])
                item["_validation"][field_name] = err["msg"]
        return item


class JobUrlPipeline:
    def process_item(self, item, spider: scrapy.Spider):
        item['JobUrl'] = f'https://{spider.allowed_domains[0]}/job-list/{item["Slug"]}/{item["Id"]}'
        return item