import json
from sqlalchemy.orm import Session
from datetime import date
from . import models, schemas

# ====================================================================
# Student CRUD 함수
# ====================================================================
def get_students(db: Session):
    return db.query(models.Student).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        **student.model_dump(),
        consultations=json.dumps([])
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, updated_student: schemas.StudentUpdate):
    db_student = get_student_by_id(db, student_id)
    if db_student:
        for key, value in updated_student.model_dump().items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student_by_id(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

def delete_all_students(db: Session):
    db.query(models.Student).delete()
    db.commit()
    return True

def add_consultation(db: Session, student_id: int, consultation: schemas.Consultation):
    db_student = get_student_by_id(db, student_id)
    if db_student:
        consultations = json.loads(db_student.consultations)
        consultations.append(consultation.model_dump())
        db_student.consultations = json.dumps(consultations)
        db.commit()
        db.refresh(db_student)
    return db_student

# ====================================================================
# WorkLog CRUD 함수
# ====================================================================
def get_work_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WorkLog).offset(skip).limit(limit).all()

def get_work_log_by_date(db: Session, log_date: date):
    return db.query(models.WorkLog).filter(models.WorkLog.date == log_date).first()

def create_work_log(db: Session, work_log: schemas.WorkLogCreate):
    db_log = models.WorkLog(date=work_log.date, content=work_log.content)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def update_work_log(db: Session, log_date: date, content: str):
    db_log = get_work_log_by_date(db, log_date)
    if db_log:
        db_log.content = content
        db.commit()
        db.refresh(db_log)
    return db_log

def delete_work_log(db: Session, log_date: date):
    db_log = get_work_log_by_date(db, log_date)
    if db_log:
        db.delete(db_log)
        db.commit()
        return True
    return False

# ====================================================================
# ToDoItem CRUD 함수
# ====================================================================
def get_todo_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ToDoItem).offset(skip).limit(limit).all()

def get_todo_item(db: Session, todo_id: int):
    return db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()

def create_todo_item(db: Session, item: schemas.ToDoItemCreate):
    db_item = models.ToDoItem(content=item.content, is_completed=item.is_completed)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_todo_item(db: Session, todo_id: int, item: schemas.ToDoItemUpdate):
    db_item = get_todo_item(db, todo_id)
    if db_item:
        if item.content is not None:
            db_item.content = item.content
        if item.is_completed is not None:
            db_item.is_completed = item.is_completed
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_todo_item(db: Session, todo_id: int):
    db_item = get_todo_item(db, todo_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False