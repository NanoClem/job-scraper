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