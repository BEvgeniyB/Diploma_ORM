from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url='sqlite://taskmanager.db',
        modules={'models': ['models']}
    )
