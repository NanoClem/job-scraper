import json

import requests as rq
from bs4 import BeautifulSoup
import dateparser


def parse_date(str_date: str, date_format: str) -> str:
    """[summary]
    
    Parameters
        str_date (str) -- [description]
    
    Returns
        str -- [description]
    """
    date = dateparser.parse(str_date)
    return date.strftime(date_format)


def clean_data(data: dict) -> dict:
    """[summary]
    
    Parameters
        data (dict) -- [description]
    
    Returns
        dict -- [description]
    """
    data_clean = data.copy()
    data_clean['published_at'] = parse_date(data_clean['published_at'], '%Y-%m-%d')

    return data_clean



if __name__ == "__main__":
    
    region = 34             # geneva district code
    activity_rate = 100     # full-time job
    job_type = 5            # fixed-term contract
    term = 'fullstack'      # job searching term
    encoding = 'utf-8'

    # Get html page
    base_url = 'https://www.jobup.ch/fr/emplois/'
    params = f'?employment-grade-min&region={region}&term={term}'
    page = rq.get(base_url + params)

    # Init web-scrap
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding=encoding)
    jobs = soup.find_all('div', class_='sc-dkPtyc Flex-sc-8fidy7-0 bKFyVS')
    job_list = []

    # Transcription table
    trans_table = {
        'eXzNTw': 'title',
        'fJSCvO': 'company',
        'ljqydn': 'company',
        'dXyOot': 'location'
    }

    # Get job data
    for job in jobs:
        data = {
            'published_at': job.find('span', class_='sc-fotPbf Text__span-jiiyzm-8 Text-jiiyzm-9 VacancySerpItem___StyledText-y84gv4-6 jaHdBs eQChBQ cxIvvs').text
        }

        # Get information about the job
        job_infos = job.find('div', class_='sc-dkPtyc Flex-sc-8fidy7-0 VacancySerpItem___StyledFlex-y84gv4-5 jAozwM fyzElZ')
        for child in job_infos.children:
            id = child['class'][3]          # get unique id among class attr
            key = trans_table[id]           # translate id into data field
            data[key] = next(child.strings) # get text inside tag
         
        # Clean data and append to list
        data = clean_data(data)
        print(data)
        job_list.append(data)

    print(json.dumps(job_list, indent=4))

    