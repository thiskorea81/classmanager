from sqlalchemy import Column, Integer, String, Date, Boolean
from .database import Base

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
    consultations = Column(String, nullable=True) # 상담 기록을 JSON 문자열로 저장

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