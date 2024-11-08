
from fastapi import APIRouter, status, HTTPException
from tortoise import Tortoise
from backend.db import init_db
from models import Task,User

from schemas import CreateUser, UpdateUser, UpdateTask, CreateTask
from slugify import slugify

router = APIRouter(prefix="/task",tags=["task"])


@router.get("/")
async def get_task():
    await init_db()  # подключаемся к базе
    tasks = await Task.all()
    await Tortoise.close_connections()  # закрываем соединения
    return tasks

@router.get("/task_id")
async def all_tasks( task_id: int):
    await init_db()  # подключаемся к базе
    tasks = await Task.get_or_none(id = task_id)
    await Tortoise.close_connections()  # закрываем соединения

    if not tasks :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found')
    return tasks

@router.post ("/create")
async def create_task(creates_task: CreateTask,user_id: int):
    await init_db()  # подключаемся к базе
    user = await User.get_or_none(id=user_id)
    if not user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    await Task.create(
        title=creates_task.title, content=creates_task.content,
        priority=creates_task.priority, user=user, completed=False,
        slug=slugify(creates_task.title)
        )

    await Tortoise.close_connections()  # закрываем соединения
    return {"status_code": status.HTTP_201_CREATED,
            "transaction": "Successful"}

@router.put("/update")
async def update_tas(task_id: int, up_task: UpdateTask):
    await init_db()
    tasks = await Task.get_or_none(id= task_id)
    if not tasks :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found')
    upd_task = {'title':up_task.title, 'content':up_task.content,
        'priority':up_task.priority}
    await tasks.update_from_dict(upd_task)
    await tasks.save()  # обязательно сохранить после изменения
    await Tortoise.close_connections()  # закрываем соединения
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task  update is successful'}

@router.delete("/delete")
async def delete_task( task_id: int):
    await init_db()
    tasks = await Task.get_or_none(id=task_id)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found')

    await tasks.delete()
    await Tortoise.close_connections()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful!'}