from anyio.abc import TaskStatus
from fastapi import APIRouter,Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import Task,User

from schemas import CreateUser, UpdateUser, UpdateTask, CreateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task",tags=["task"])


@router.get("/")
async def get_task(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/task_id")
async def all_tasks(db: Annotated[Session, Depends(get_db)], task_id: int):

    tasks = db.scalar(select(Task).where(Task.id == task_id))
    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found')
    return tasks

@router.post ("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask,user_id: int):
    users = db.scalar(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    db.execute(insert(Task).values(title=create_task.title, content=create_task.content,
                                   priority=create_task.priority, user_id=user_id,completed=False,
                                   slug=slugify(create_task.title)))
    db.commit()
    return {"status_code": status.HTTP_201_CREATED,
            "transaction": "Successful"}


@router.put("/update")
async def update_tas(db: Annotated[Session, Depends(get_db)], task_id: int, up_task: UpdateTask):
    tasks = db.scalar(select(Task).where(Task.id == task_id))
    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found')
    db.execute(update(Task).where(Task.id == task_id).values(
        title=up_task.title,
        content=up_task.content,
        priority=up_task.priority))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task  update is successful'}

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.scalar(select(Task).where(Task.id == task_id))
    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found')

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful!'}