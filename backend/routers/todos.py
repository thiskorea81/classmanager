import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from google.genai import types

from .. import crud, models, schemas
from ..database import SessionLocal, engine, get_db
from ..main import get_gemini_client


router = APIRouter()

@router.get("/", response_model=List[schemas.ToDoItem])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_todo_items(db)

@router.post("/", response_model=schemas.ToDoItem, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoItemCreate, db: Session = Depends(get_db)):
    return crud.create_todo_item(db, item=todo)

@router.put("/{todo_id}", response_model=schemas.ToDoItem)
def update_todo(todo_id: int, todo: schemas.ToDoItemUpdate, db: Session = Depends(get_db)):
    updated_item = crud.update_todo_item(db, todo_id, item=todo)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return updated_item

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    if not crud.delete_todo_item(db, todo_id):
        raise HTTPException(status_code=404, detail="Todo item not found")

@router.post("/from-log/", response_model=List[schemas.ToDoItem])
def extract_todos_from_log(log: schemas.WorkLogCreate, db: Session = Depends(get_db)):
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
            """,
            config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)  # Turn off thinking
            # Thinking max:
            # thinking_config=types.ThinkingConfig(thinking_budget=24576)
            # Turn on dynamic thinking:
            # thinking_config=types.ThinkingConfig(thinking_budget=-1)
            ),
        )
        
        extracted_text = response.text.replace('*', '').strip()
        
        if extracted_text == '없음':
            return []
            
        todo_list = [item.strip() for item in extracted_text.split(',') if item.strip()]
        
        created_todos = []
        for content in todo_list:
            todo_item = schemas.ToDoItemCreate(content=content)
            created_item = crud.create_todo_item(db, item=todo_item)
            created_todos.append(created_item)
            
        return created_todos

    except Exception as e:
        print(f"Gemini API 호출 오류: {e}")
        raise HTTPException(status_code=500, detail="Gemini API 호출 중 오류가 발생했습니다.")