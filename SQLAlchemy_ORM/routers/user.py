from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from backend.db_depends import get_db
from typing import Annotated
from models import User,Task
from schemas import CreateUser, UpdateUser
import crud
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalar(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    return users

@router.get("/user_id/task")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalar(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if tasks is None:
        return {'status_code': status.HTTP_200_OK,
        'transaction': 'Task not found'}
    return tasks

@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], creates_user: CreateUser):
    db.execute(insert(User).values(username=creates_user.username, firstname=creates_user.firstname,
                                   lastname=creates_user.lastname, age=creates_user.age,
                                   slug=slugify(creates_user.username)))
    db.commit()
    return {"status_code": status.HTTP_201_CREATED,
            "transaction": "Successful"}

@router.post('/create2')
async def create_user2(db: Annotated[Session, Depends(get_db)],creates_user: CreateUser):
    return {"status_code": status.HTTP_201_CREATED,"transaction":crud.create_db(db, creates_user)}

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, up_user: UpdateUser):
    users = db.scalar(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    db.execute(update(User).where(User.id == user_id).values(
        firstname=up_user.firstname,
        lastname=up_user.lastname,
        age=up_user.age))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User  update is successful'}


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalar(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')

    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful!'}
