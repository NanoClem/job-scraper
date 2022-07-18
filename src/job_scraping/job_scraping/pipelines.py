import json
from collections import defaultdict

from pydantic import ValidationError

import job_scraping.utils as utils
from job_scraping.items import AWItem


class AWValidationPipeline:
    
    def process_item(self, item, spider):
        try:
            AWItem.validate(item)
        except ValidationError as validErr:
            item["_validation"] = defaultdict(list)
            for err in validErr.errors():
                field_name = "/".join(str(loc) for loc in err["loc"])
                item["_validation"][field_name] = err["msg"]
        return item
    
    
class JsonLoadingPipeline:

    def open_spider(self, spider):
        load_path = utils.get_src_path() / 'data' / spider.name
        load_path.mkdir(parents=True, exist_ok=True)
        self.file = open(load_path / 'items.jsonlines', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item, ensure_ascii=False) + "\n"
        self.file.write(line)
        return item