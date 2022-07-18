from collections import defaultdict
from pydantic import ValidationError

from job_scraping.items import AWItem


class AWValidationPipeline:
    
    def process_item(self, item, spider):
        try:
            print('validation')
            AWItem.validate(item)
        except ValidationError as validErr:
            item["_validation"] = defaultdict(list)
            for err in validErr.errors():
                field_name = "/".join(str(loc) for loc in err["loc"])
                item["_validation"][field_name] = err["msg"]
        return item
