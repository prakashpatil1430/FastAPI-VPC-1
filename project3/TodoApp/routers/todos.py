from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from starlette import status
from typing import Optional
from .auth import get_current_user

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: Optional[bool] = False  # Make it optional with a default value

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new Todo',
                'description': 'description about todo',
                'priority': 5,
                'complete': True
            }
        }


@router.get('/todo/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    return HTTPException(status_code=404, detail='data not found!!!')


@router.post('/todo/create-data/', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                     db: db_dependency,
                    todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    new_todo = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(new_todo)
    db.commit()
    return new_todo


@router.put('/todo/update-data/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def create_todo(user: user_dependency, db: db_dependency, 
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    
    if todo_model:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.add(todo_model)
        db.commit()
        return todo_model


@router.delete('/todo/delete-data/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def create_todo(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()
