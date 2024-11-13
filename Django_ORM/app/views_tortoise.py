import time

from tortoise import Tortoise, fields, models, run_async
from tortoise.functions import Count
from .models_t import TCinema




async def tortoise_init():
    await Tortoise.init(
        db_url="sqlite:C:\\Project\\Diplom_ORM\\Django_ORM\\db.sqlite3",
        modules={'models': ['app.models_t',]},
    )
    await Tortoise.generate_schemas()


async def t_simple_query(data: dict, find_yes: bool):
    start = time.time()
    if find_yes:
        review = await TCinema.filter(countries='[США]').first()
        end = time.time()
        data['Простой запрос к таблице есть запись'][0][2] = f"{(end - start):.3f} сек."
    else:
        review = await TCinema.filter(countries='[ХХХ]').first()
        end = time.time()
        data['Простой запрос к таблице нет записи'][0][2] = f"{(end - start):.3f} сек."


async def t_group_by(data: dict):
    start = time.time()
    review = await TCinema.annotate(count=Count("movie_year")).group_by("movie_year").all()
    end = time.time()
    data['Запрос с GROUP BY'][0][2] = f"{(end - start):.3f} сек."


async def t_sort(data: dict):
    start = time.time()
    review = await TCinema.all().order_by("countries")
    end = time.time()
    data['Запрос с сортировкой'][0][2] = f"{(end - start):.3f} сек."


async def t_filter(data: dict):
    start = time.time()
    review = await TCinema.filter(countries='[США]').all()
    end = time.time()
    data['Запрос с условием фильтрации'][0][2] = f"{(end - start):.3f} сек."



async def t_add_record(data: dict):
    start = time.time()
    review = await TCinema.create( name = "Какой то фильм 2",
        movie_duration="50",
        movie_year = 1900,
        genres = "о чем то",
        countries = "где то")
    end = time.time()
    data['Добавить запись'][0][2] = f"{(end - start):.3f} сек."


async def t_update_records(data: dict):
    start = time.time()
    await TCinema.filter(countries='test Updated').update(countries='TEST')
    end = time.time()
    data['Обновление по фильтру'][0][2] = f"{(end - start):.3f} сек."


async def tortoise_main(data: dict):
    await tortoise_init()
    await t_simple_query(data, True)
    await t_simple_query(data, False)
    await t_group_by(data)
    await t_sort(data)
    await t_filter(data)
    await t_add_record(data)
    await t_update_records(data)
    await Tortoise.close_connections()
    return data


if __name__ == "__main__":
    data = {
        'Простой запрос к таблице есть запись': [["", "", ""]],
        'Простой запрос к таблице нет записи': [["", "", ""]],
        'Запрос с GROUP BY': [["", "", ""]],
        'Запрос с сортировкой': [["", "", ""]],
        'Запрос с условием фильтрации': [["", "", ""]],
        'Запрос с JOIN': [["", "", ""]],
        'Добавить запись': [["", "", ""]],
        'Обновление по фильтру': [["", "", ""]]
    }
    run_async(tortoise_main(data))


