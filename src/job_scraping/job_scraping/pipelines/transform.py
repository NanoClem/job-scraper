import job_scraping.utils as utils
from job_scraping.spiders import AcademicworkSpider, JobupSpider


class JobUpTransformPipeline:

    def process_item(self, item, spider: JobupSpider):
        """d"""
        return item


class AwTransformPipeline:

    def process_item(self, item, spider: AcademicworkSpider):
        """d"""
        item['publication_date'] = utils.to_date_format(
            item['publication_date'], '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S%z'
        )
        item['employment_rate'] = (
            100 if item['job_extent'].lower() == 'temps plein' else 80
        )
        
        return item
