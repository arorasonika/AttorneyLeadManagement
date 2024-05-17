from pydantic import BaseModel, EmailStr
from datetime import datetime

class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    resume: str

class ExistingLead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    resume: str
    state: str
    created_at: datetime

class LeadUpdate(BaseModel):
    state: str
