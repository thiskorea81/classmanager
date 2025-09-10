from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

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

class Student(StudentBase):
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

class WorkLog(WorkLogBase):
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

class ToDoItem(ToDoItemBase):
    id: int
    model_config = {"from_attributes": True}

class ConsultationList(BaseModel):
    consultations: List[Consultation]
    
    model_config = {"from_attributes": True}