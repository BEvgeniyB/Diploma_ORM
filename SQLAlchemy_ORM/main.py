from fastapi import FastAPI
from routers import user,task

app = FastAPI()

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




