import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models_alchemy import *
from sqlalchemy import func
from sqlalchemy.orm import Session

def sql_alchem(data : dict):

    engine=create_engine('sqlite:///db.sqlite3')
    with Session(autoflush=False, bind=engine) as db:
        rez = list_all(db)
        rez = al_simple_query(db, True)
        data['Простой запрос к таблице есть запись'][0][1] = rez
        rez = al_simple_query(db, False)
        data['Простой запрос к таблице нет записи'][0][1] = rez
        rez = al_group_by(db)
        data['Запрос с GROUP BY'][0][1] = rez
        rez = al_sort(db)
        data['Запрос с сортировкой'][0][1] = rez
        rez = al_filter(db)
        data['Запрос с условием фильтрации'][0][1] = rez
        rez = al_add_record(db)
        data['Добавить запись'][0][1] = rez
        rez = al_update_records(db)
        data['Обновление по фильтру'][0][1] = rez

    db.close()
    return data

def list_all(db : Session ):
   start = time.time()
   # получение всех объектов
   review = db.query(A_Cinema).all()
   end = time.time()
   return (f"{(end - start):.3f} сек.")

def al_simple_query(db: Session, find_yes : bool):
    start = time.time()
    if find_yes :
    # получение первого из всех объектов
        review = db.query(A_Cinema).filter(A_Cinema.countries=='[США]').first()
    else:
        review = db.query(A_Cinema).filter(A_Cinema.countries == '[ХХХ]').first()

    end = time.time()
    return (f"{(end - start):.3f} сек.")

def al_group_by(db: Session):
    start = time.time()
    review = db.query(A_Cinema.movie_year, func.count(A_Cinema.movie_year)).group_by(A_Cinema.movie_year).all()
    end = time.time()
    return (f"{(end - start):.3f} сек.")

def al_sort(db: Session):
    start = time.time()
    db.query(A_Cinema).order_by(A_Cinema.countries).all()
    end = time.time()
    return (f"{(end - start):.3f} сек.")

def al_filter(db: Session):
    start = time.time()
    db.query(A_Cinema).filter(A_Cinema.countries == '[США]').all()
    end = time.time()
    return (f"{(end - start):.3f} сек.")


def al_add_record(db: Session):
    start = time.time()
    one_record = A_Cinema (
        name = "Какой то фильм",
        movie_duration="50",
        movie_year = 1900,
        genres = "о чем то",
        countries = "где то"
    )
    db.add(one_record)
    db.commit()
    end = time.time()
    return (f"{(end - start):.3f} сек.")

def al_update_records(db: Session):
    start = time.time()
    db.query(A_Cinema).filter(A_Cinema.countries ==  'test Updated').update({'countries': 'TEST'}, synchronize_session='fetch')
    db.commit()
    end = time.time()
    return (f"{(end - start):.3f} сек.")