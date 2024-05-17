from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Union
from sqlalchemy.orm import Session
from . import mail, models, schemas, crud, database
from .database import engine
import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from typing import Annotated

attorney_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2"
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(attorney_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = attorney_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

# API to get details about the current user
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

# API to submit a lead form
@app.post("/leads/", response_model=schemas.ExistingLead)
def create_lead(lead: schemas.LeadCreate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    db_lead = crud.create_lead(db=db, lead=lead)
    background_tasks.add_task(mail.send_email, lead.email, "Lead Received", "Thank you for submitting your information.")
    background_tasks.add_task(mail.send_email, os.getenv("ATTORNEY_EMAIL_ID"), "New Lead Submitted", f"Lead details: {lead.model_dump()}")
    return db_lead

# API to get all the submitted leads (access restricted to authenticated attorneys only)
@app.get("/leads/", response_model=list[schemas.ExistingLead])
def get_leads(token: Annotated[str, Depends(oauth2_scheme)], skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    leads = crud.get_leads(db=db, skip=skip, limit=limit)
    return leads

# API to update the state of a submitted lead (access restricted to authenticated attorneys only)
@app.put("/leads/{lead_id}", response_model=schemas.ExistingLead)
def update_lead(token: Annotated[str, Depends(oauth2_scheme)], lead_id: int, db: Session = Depends(database.get_db)):
    db_lead = crud.update_lead_state(db=db, lead_id=lead_id, state="REACHED_OUT")
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

# API to delete all the submitted leads (access restricted to authenticated attorneys only)
@app.delete("/leads/")
def delete_lead(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    crud.delete_leads(db=db)
    return True
