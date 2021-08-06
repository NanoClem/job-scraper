from abc import ABCMeta, abstractmethod
from typing import List

from bs4 import BeautifulSoup
import requests as rq
import unidecode as unidc
import dateparser


class JobScraper(object, metaclass=ABCMeta):
    """[summary]
    
    Parameters
        object ([type]) -- [description]
        metaclass ([type]) -- [description] (default: ABCMeta)
    
    Returns
        [type] -- [description]
    """

    @abstractmethod
    def __init__(self, base_url: str, date_format: str='%Y-%m-%d', encoding: str='utf-8'):
        """[summary]
        
        Parameters
            base_url (str) -- [description]
            date_format (str) -- [description] (default: '%Y-%m-%d')
            encoding (str) -- [description] (default: 'utf-8')
        """
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.date_format = date_format
        self.html_encoding = encoding


    def parse_date(self, str_date: str, date_format: str) -> str:
        """[summary]
        
        Parameters
            str_date (str) -- [description]
            date_format (str) -- [description]
        
        Returns
            str -- [description]
        """
        date = dateparser.parse(str_date)
        return date.strftime(date_format)


    def get_page_content(self) -> bytes:
        """[summary]
        
        Returns
            bytes -- [description]
        """
        page = rq.get(self.get_full_url())
        return page.content


    @abstractmethod
    def get_full_url(self):
        pass

    @abstractmethod
    def _clean_data(self, data):
        pass

    @abstractmethod
    def scrap_jobs(self):
        pass


# =======================================================================
#       JOBUP WEBSITE
# =======================================================================

class JobupScraper(JobScraper):
    """[summary]
    
    Parameters
        JobScraper ([type]) -- [description]
    """
    
    def __init__(self, base_url: str, region: str, activity_rate: int, job_type: int, term: str, date_format: str='%Y-%m-%d', encoding='utf-8'):
        """[summary]
        
        Parameters
            web_url (str) -- [description]
            region (str) -- [description]
            activity_rate (int) -- [description]
            job_type (int) -- [description]
            term (str) -- [description]
            date_format (str) -- [description] (default: '%Y-%m-%d')
            encoding (str) -- [description] (default: 'utf-8')
        """
        super().__init__(base_url, date_format, encoding)

        # url params
        self.region = region
        self.activity_rate = activity_rate
        self.job_type = job_type
        self.term = term

        # trans table
        self.trans_table = {
            'eXzNTw': 'title',
            'fJSCvO': 'company',
            'ljqydn': 'company',
            'dXyOot': 'location'
        }


    def get_full_url(self) -> str:
        """[summary]
        
        Returns
            str -- [description]
        """
        params = f'?employment-grade-min={self.activity_rate}&region={self.region}&term={self.term}'
        return self.base_url + params


    def _clean_data(self, data: dict) -> dict:
        """[summary]
        
        Parameters
            data (dict) -- [description]
        
        Returns
            dict -- [description]
        """
        data_clean = data.copy()
        ommit = ['published_at']

        data_clean['published_at'] = self.parse_date(data_clean['published_at'], self.date_format)
        data_clean = {k: unidc.unidecode(v) if k not in ommit else v for k,v in data_clean.items()}

        return data_clean


    def scrap_jobs(self) -> List[dict]:
        """[summary]
        
        Returns
            List[dict] -- [description]
        """
        job_list = []
        soup = BeautifulSoup(self.get_page_content(), 'html.parser', from_encoding=self.html_encoding)
        jobs = soup.find_all('div', class_='sc-dkPtyc Flex-sc-8fidy7-0 bKFyVS')

        for job in jobs:
            data = {}

            # Get publication date
            pub_date = job.find('span', class_='sc-fotPbf Text__span-jiiyzm-8 Text-jiiyzm-9 VacancySerpItem___StyledText-y84gv4-6 jaHdBs eQChBQ cxIvvs')
            data['published_at'] = pub_date.text

            # Get information about the job offer
            job_infos = job.find('div', class_='sc-dkPtyc Flex-sc-8fidy7-0 VacancySerpItem___StyledFlex-y84gv4-5 jAozwM fyzElZ')
            for child in job_infos.children:
                id = child['class'][3]              # get unique id among class attr
                key = self.trans_table[id]          # translate id into data field
                data[key] = next(child.strings)     # get text inside tag
            
            # Clean data and append to list
            data = self._clean_data(data)
            job_list.append(data)

        return job_list


# =======================================================================
#       ACADEMIC WORK WEBSITE
# =======================================================================

class AcademicWorkScraper(JobScraper):
    """[summary]
    
    Parameters
        JobScraper ([type]) -- [description]
    """
    pass