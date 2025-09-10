import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import crud, models, schemas
from ..database import SessionLocal, engine, get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.WorkLog])
def read_work_logs(db: Session = Depends(get_db)):
    return crud.get_work_logs(db)

@router.get("/{log_date}", response_model=schemas.WorkLog)
def read_work_log_by_date(log_date: date, db: Session = Depends(get_db)):
    db_log = crud.get_work_log_by_date(db, log_date)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Work log not found for this date")
    return db_log

@router.post("/", response_model=schemas.WorkLog)
def create_or_update_work_log(work_log: schemas.WorkLogCreate, db: Session = Depends(get_db)):
    db_log = crud.get_work_log_by_date(db, work_log.date)
    if db_log:
        updated_log = crud.update_work_log(db, work_log.date, work_log.content)
        return updated_log
    else:
        new_log = crud.create_work_log(db, work_log)
        return new_log

@router.delete("/{log_date}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_log(log_date: date, db: Session = Depends(get_db)):
    if not crud.delete_work_log(db, log_date):
        raise HTTPException(status_code=404, detail="Work log not found for this date")
    return {"message": "Work log deleted successfully"}