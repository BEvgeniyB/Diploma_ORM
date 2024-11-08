from fastapi import APIRouter, status, HTTPException
from tortoise import Tortoise
from backend.db import init_db
from models import User,Task
from schemas import CreateUser, UpdateUser
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users():
    await init_db()  # подключаемся к базе
    users = await User.all()
    await Tortoise.close_connections()  # закрываем соединения
    return users


@router.get("/user_id")
async def user_by_id( user_id: int):
    await init_db()  # подключаемся к базе
    users = await User.get_or_none(id=user_id)
    await Tortoise.close_connections()  # закрываем соединения
    if not users :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    return users

@router.get("/user_id/task")
async def tasks_by_user_id(user_id: int):
    await init_db()
    users = await User.get_or_none(id=user_id)
    if not users :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    tasks = await Task.filter(user=users)
    await Tortoise.close_connections()  # закрываем соединения
    if tasks is None:
        return {'status_code': status.HTTP_200_OK,
        'transaction': 'Task not found'}
    return tasks

@router.post("/create")
async def create_user( create_users: CreateUser):
    await init_db()
    user, is_created = await User.get_or_create(username=create_users.username, firstname=create_users.firstname,
                                   lastname=create_users.lastname, age=create_users.age,
                                   slug=slugify(create_users.username))
    await Tortoise.close_connections()  # закрываем соединения
    if is_created:
        return {"status_code": status.HTTP_201_CREATED,
            "transaction": "Successful"}
    return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "transaction": "not created"}

@router.put("/update")
async def update_user(user_id: int, up_user: UpdateUser):
    await init_db()
    users = await User.get_or_none(id=user_id)
    if not users :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')

    users.firstname=up_user.firstname,
    users.lastname=up_user.lastname,
    users.age=up_user.age
    await users.save()
    await Tortoise.close_connections()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User  update is successful'}


@router.delete("/delete")
async def delete_user(user_id: int):
    await init_db()
    users = await User.get_or_none(id=user_id)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    await users.delete()
    await Tortoise.close_connections()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful!'}
