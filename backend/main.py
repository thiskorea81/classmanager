import json
import os
import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from google import genai
from google.genai import types # 변경된 import 구문

# ====================================================================
# 데이터베이스 설정
# ====================================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ====================================================================
# 모델 (ORM)
# ====================================================================
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Integer)
    class_num = Column(Integer)
    student_num = Column(Integer)
    name = Column(String, index=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    guardian_phone1 = Column(String, nullable=True)
    guardian_phone2 = Column(String, nullable=True)
    consultations = Column(String, nullable=True)

class WorkLog(Base):
    __tablename__ = "work_logs"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True)
    content = Column(String)

class ToDoItem(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    is_completed = Column(Boolean, default=False)

# ====================================================================
# 스키마 (Pydantic)
# ====================================================================
class Consultation(BaseModel):
    date: str
    content: str
    model_config = {"from_attributes": True}

class StudentBase(BaseModel):
    grade: int
    class_num: int
    student_num: int
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    guardian_phone1: Optional[str] = None
    guardian_phone2: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentSchema(StudentBase):
    id: int
    consultations: Optional[List[Consultation]] = None
    model_config = {"from_attributes": True}

class WorkLogBase(BaseModel):
    date: date
    content: str

class WorkLogCreate(WorkLogBase):
    pass

class WorkLogUpdate(WorkLogBase):
    pass

class WorkLogSchema(WorkLogBase):
    id: int
    model_config = {"from_attributes": True}

class ToDoItemBase(BaseModel):
    content: str
    is_completed: bool = False

class ToDoItemCreate(ToDoItemBase):
    pass

class ToDoItemUpdate(ToDoItemBase):
    content: Optional[str] = None
    is_completed: Optional[bool] = None

class ToDoItemSchema(ToDoItemBase):
    id: int
    model_config = {"from_attributes": True}

class ConsultationList(BaseModel):
    consultations: List[Consultation]
    model_config = {"from_attributes": True}

# ====================================================================
# CRUD 함수
# ====================================================================
def get_students(db: Session):
    return db.query(Student).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump(), consultations=json.dumps([]))
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, updated_student: StudentUpdate):
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
    db.query(Student).delete()
    db.commit()
    return True

def add_consultation(db: Session, student_id: int, consultation: Consultation):
    db_student = get_student_by_id(db, student_id)
    if db_student:
        consultations = json.loads(db_student.consultations)
        consultations.append(consultation.model_dump())
        db_student.consultations = json.dumps(consultations)
        db.commit()
        db.refresh(db_student)
    return db_student

def get_work_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(WorkLog).offset(skip).limit(limit).all()

def get_work_log_by_date(db: Session, log_date: date):
    return db.query(WorkLog).filter(WorkLog.date == log_date).first()

def create_work_log(db: Session, work_log: WorkLogCreate):
    db_log = WorkLog(date=work_log.date, content=work_log.content)
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

def get_todo_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ToDoItem).offset(skip).limit(limit).all()

def get_todo_item(db: Session, todo_id: int):
    return db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()

def create_todo_item(db: Session, item: ToDoItemCreate):
    db_item = ToDoItem(content=item.content, is_completed=item.is_completed)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_todo_item(db: Session, todo_id: int, item: ToDoItemUpdate):
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

# ====================================================================
# FastAPI 앱 및 엔드포인트
# ====================================================================
app = FastAPI(title="교사업무도우미 API")

# Gemini API 클라이언트 초기화
try:
    client = genai.Client()
except Exception as e:
    print(f"Failed to initialize Gemini client: {e}")
    client = None

# CORS 설정
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/students/", response_model=List[StudentSchema])
def read_students_endpoint(db: Session = Depends(get_db)):
    students = get_students(db)
    for student in students:
        student.consultations = json.loads(student.consultations) if student.consultations else []
    return students

@app.post("/students/", response_model=StudentSchema, status_code=status.HTTP_201_CREATED)
def create_student_endpoint(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = create_student(db, student)
    new_student.consultations = json.loads(new_student.consultations)
    return new_student

@app.delete("/students/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_students_endpoint(db: Session = Depends(get_db)):
    delete_all_students(db)

@app.get("/students/{student_id}", response_model=StudentSchema)
def read_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    student = get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student.consultations = json.loads(student.consultations) if student.consultations else []
    return student

@app.put("/students/{student_id}", response_model=StudentSchema)
def update_student_endpoint(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    updated_student = update_student(db, student_id, student)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    updated_student.consultations = json.loads(updated_student.consultations)
    return updated_student

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    if not delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")

@app.post("/students/{student_id}/consultations", response_model=StudentSchema)
def add_consultation_endpoint(student_id: int, consultation: Consultation, db: Session = Depends(get_db)):
    updated_student = add_consultation(db, student_id, consultation)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    updated_student.consultations = json.loads(updated_student.consultations)
    return updated_student

@app.post("/students/{student_id}/summarize-consultations")
def summarize_consultations_endpoint(student_id: int, consultations: ConsultationList):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API client not initialized. Check your API key.")
    try:
        consultation_text = ""
        if not consultations.consultations:
            return {"summary": "상담 기록이 없습니다."}

        for c in consultations.consultations:
            consultation_text += f"날짜: {c.date}\n내용: {c.content}\n---\n"
        
        prompt = f"""
        다음은 학생의 상담 기록이야. 이 기록 전체에서 가장 중요한 핵심 내용과 주요 변화를 3~4줄로 간결하게 요약해줘.
        
        상담 기록:
        "{consultation_text}"
        """
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        
        summary_text = response.text.replace('*', '').strip()
        return {"summary": summary_text}
    except Exception as e:
        print(f"Gemini API 호출 오류: {e}")
        raise HTTPException(status_code=500, detail="Gemini API 호출 중 오류가 발생했습니다.")

@app.get("/work-logs/", response_model=List[WorkLogSchema])
def read_work_logs_endpoint(db: Session = Depends(get_db)):
    return get_work_logs(db)

@app.get("/work-logs/{log_date}", response_model=WorkLogSchema)
def read_work_log_by_date_endpoint(log_date: date, db: Session = Depends(get_db)):
    db_log = get_work_log_by_date(db, log_date)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Work log not found for this date")
    return db_log

@app.post("/work-logs/", response_model=WorkLogSchema)
def create_or_update_work_log_endpoint(work_log: WorkLogCreate, db: Session = Depends(get_db)):
    db_log = get_work_log_by_date(db, work_log.date)
    if db_log:
        updated_log = update_work_log(db, work_log.date, work_log.content)
        return updated_log
    else:
        new_log = create_work_log(db, work_log)
        return new_log

@app.delete("/work-logs/{log_date}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_log_endpoint(log_date: date, db: Session = Depends(get_db)):
    if not delete_work_log(db, log_date):
        raise HTTPException(status_code=404, detail="Work log not found for this date")

@app.get("/todos/", response_model=List[ToDoItemSchema])
def read_todos_endpoint(db: Session = Depends(get_db)):
    return get_todo_items(db)

@app.post("/todos/", response_model=ToDoItemSchema, status_code=status.HTTP_201_CREATED)
def create_todo_endpoint(todo: ToDoItemCreate, db: Session = Depends(get_db)):
    return create_todo_item(db, item=todo)

@app.put("/todos/{todo_id}", response_model=ToDoItemSchema)
def update_todo_endpoint(todo_id: int, todo: ToDoItemUpdate, db: Session = Depends(get_db)):
    updated_item = update_todo_item(db, todo_id, item=todo)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return updated_item

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    if not delete_todo_item(db, todo_id):
        raise HTTPException(status_code=404, detail="Todo item not found")

@app.post("/todos/from-log/", response_model=List[ToDoItemSchema])
def extract_todos_from_log_endpoint(log: WorkLogCreate, db: Session = Depends(get_db)):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API client not initialized. Check your API key.")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=f"""
            다음은 교사의 하루 업무일지 내용이야. 이 내용에서 주요한 할 일들을 명확한 행동 동사로 시작하는 짧고 간결한 목록으로 추출해줘.
            각 항목을 쉼표로 구분해. 만약 할 일이 없다면 '없음'이라고만 답변해줘.
            
            업무일지 내용:
            "{log.content}"
            
            예시:
            - 학생 A 상담 진행, - 학부모 B 전화하기, - 수업 준비하기
            """
        )
        extracted_text = response.text.replace('*', '').strip()
        if extracted_text == '없음':
            return []
            
        todo_list = [item.strip() for item in extracted_text.split(',') if item.strip()]
        
        created_todos = []
        for content in todo_list:
            todo_item = ToDoItemCreate(content=content)
            created_item = create_todo_item(db, item=todo_item)
            created_todos.append(created_item)
        return created_todos
    except Exception as e:
        print(f"Gemini API 호출 오류: {e}")
        raise HTTPException(status_code=500, detail="Gemini API 호출 중 오류가 발생했습니다.")

@app.get("/test/gemini-status")
async def get_gemini_status_endpoint():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Google API Key not found in environment variables.")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-latest",
            contents="Is the Gemini API working?",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        return {"status": "success", "message": "Gemini API is working correctly!", "response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Gemini API. Error: {e}")