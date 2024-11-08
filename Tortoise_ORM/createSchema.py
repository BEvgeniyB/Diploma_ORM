from tortoise import Tortoise, run_async
from backend.db import init_db

async def main():
    await init_db()
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(main())