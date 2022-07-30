from pydantic import BaseModel


class JobItem(BaseModel):
    
    job_id: str
    title: str
    slug: str
    url: str
    source_website: str
    employment_type: str
    job_category: str
    job_extent: str
    description: str
    location: str
    publication_date: str
    employment_rate: int = None
    company: str = None
