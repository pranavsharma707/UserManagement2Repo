
from pydantic import BaseModel,EmailStr


class User(BaseModel):
    organization_name: str
    tenant_name : str
    company_logo : str
    username:str
    firstname: str
    lastname: str
    email: str
    password: str
    account_name: str
    title: str
    country: str
    line_manager: str
    address: str
    department: str
    job_title: str
    date_of_birth: str
    start_date: str
    town: str
    postcode: str
    cell_number: str
    level_twomanager: str

class userRole(BaseModel):

    name:str