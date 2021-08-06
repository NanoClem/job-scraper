import json
from scrapers.website_scrapers import JobupScraper


if __name__ == "__main__":
    
    jobup_conf = {
        'base_url': 'https://www.jobup.ch/fr/emplois/',
        'term': 'fullstack',      # job field
        'region': 34,             # geneva district code
        'activity_rate': 100,     # full-time job
        'job_type': 5,            # fixed-term contract
    }
    
    jobup = JobupScraper(**jobup_conf)
    jobs_data = jobup.scrap_jobs()
    print(json.dumps(jobs_data, indent=4))