import sqlalchemy
from sqlalchemy.orm import Session
from . import models, schemas

def create_lead(db: Session, lead: schemas.LeadCreate):
    try:
        db_lead = models.Lead(**lead.model_dump())
        db.add(db_lead)
    except:
        db.rollback()
        raise
    else:
        db.commit()
        db.refresh(db_lead)
        return db_lead

def get_leads(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Lead).offset(skip).limit(limit).all()

def update_lead_state(db: Session, lead_id: int, state: str):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead:
        lead.state = state
        db.commit()
        db.refresh(lead)
    return lead

def delete_leads(db: Session):
    leads = db.query(models.Lead)
    for lead in leads:
        db.delete(lead)
        db.commit()
    return