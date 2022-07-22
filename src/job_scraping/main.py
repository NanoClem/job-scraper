import logging

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from job_scraping.spiders import academicwork as aw, jobup as jbp
from job_scraping.utils import get_src_path


def run(runner: CrawlerRunner) -> None:
    runner.crawl(aw.AcademicworkSpider)
    runner.crawl(jbp.JobupSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def main():
    
    # Only with a runner (call configure_logging with a process)
    logging.basicConfig(
        filename=str(get_src_path() / 'scrap.log'),
        level=logging.INFO,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
    )
 
    runner = CrawlerRunner(get_project_settings())
    run(runner)


if __name__ == "__main__":
    main()
