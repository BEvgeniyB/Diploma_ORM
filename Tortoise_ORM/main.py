from fastapi import FastAPI
from routers import user,task
from contextlib import asynccontextmanager
from backend.db import init_db
from tortoise import Tortoise

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    #await Tortoise.generate_schemas()   #создает таблицы  вынес в отдельный файл "createSchema.py" так как нужно только при изменении
    yield
    await Tortoise.close_connections()
    pass
app = FastAPI(title='Dnevnik', lifespan=lifespan)

@app.get("/welcome")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(user.router)
app.include_router(task.router)




if __name__ == '__main__':
    import pkgutil
    import sys
    search_path = ['.']  # Используйте None, чтобы увидеть все модули, импортируемые из sys.path
    all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
    print(all_modules)
    print(sys.path)




