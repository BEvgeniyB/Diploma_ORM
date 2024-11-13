from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from .models import User,Task ,Cinema
from .forms import UserRegister
# Create your views here.


def main(request):
    title = 'Главная страница сайта'
    context = {'Title':title,}
    return render(request,"index.html",context=context)

def user_list(request):
    title = 'Список'
    users = User.objects.all()

    context = {'list':users,'Title':title}
    return render(request,"users.html",context=context)

def task_list(request):
    if request.method == "POST":
        user_id = request.POST['idd']
        user_str = f'У пользователя :{User.objects.get(id=user_id)}'
        tasks = Task.objects.filter(user_id=user_id)
        there_is = Task.objects.filter(user_id=user_id).exists()
        completed_tasks = Task.objects.filter(user_id=user_id , completed=True).count()
        not_completed_tasks = Task.objects.filter(user_id=user_id, completed=False).count()
        title = 'Задания'
        #context = {'title':title,'list':tasks,'there_is':there_is,completed_tasks:completed_tasks,not_completed_tasks:not_completed_tasks}
    else:
        tasks = Task.objects.all()
        there_is = Task.objects.all().exists()
        user_str = 'По всем пользователям'
        completed_tasks = Task.objects.filter(completed=True).count()
        not_completed_tasks = Task.objects.filter(completed=False).count()
        title = 'Все задания'
        #context = {'title': title, 'list': tasks,'there_is':there_is}
    context = {'title': title, 'list': tasks, 'there_is': there_is, 'completed_tasks': completed_tasks,
               'not_completed_tasks': not_completed_tasks,'user_str':user_str}
    return render(request,"tasks.html",context=context)

def registration_user(request: WSGIRequest):
    info = {}
    if request.method == "POST":
        form = UserRegister(request.POST)
        info['form'] = form
        if form.is_valid():
            info['username'] = form.cleaned_data["username"]
            info['firstname'] = form.cleaned_data["firstname"]
            info['lastname'] = form.cleaned_data["lastname"]
            info['age'] = form.cleaned_data["age"]

            if  not User.objects.filter(username=info['username']).exists():
                User.objects.create(username=info['username'],firstname=info['firstname'],lastname=info['lastname'], age= info['age'])
                info["generated"] = f"Приветствуем, {info['username']}!"
            elif User.objects.filter(username=info['username']).count() > 0:
                info["error"] = "Пользователь уже существует"

            else:
                info["error"] = "Вы должны быть старше 18"
        return render(request, template_name="registration_page.html", context=info)

    else:
        form = UserRegister()
        return render(request, template_name="registration_page.html",context={'form':form})

################################     ПРОИЗВОДИТЕЛЬНОСТЬ   ###################################
import csv
from os import path as pathes
import time
import asyncio
from django.db import connection
from django.db.models import Count
from .views_sqlalchemy import sql_alchem
from .views_tortoise import tortoise_main

def productivity(request):
    title = "Тестирование производительности"
    head = "Сравнительная таблица"
    data = {}
    perf = Perfomance('Django')


    # rez = perf.import_from_csv()
    # data['Загрузка тестовых данных']= [[rez, 2, 3 ]]



    data = calculation_of_indicators(data, perf).copy()
    data = sql_alchem(data).copy()
    data = asyncio.run(tortoise_main(data))



    context = {
        'title': title,
        'head': head,
        'data': data,

    }
    return render(request, 'productivity.html', context)

# запуск тестирования
def calculation_of_indicators(data: dict, perf):
    rez = perf.list_all()
    rez = perf.simple_query()
    data['Простой запрос к таблице есть запись'] = [[rez, 2, 3]]

    rez = perf.simple_query_not_find_record()
    data['Простой запрос к таблице нет записи'] = [[rez, 2, 3]]

    rez = perf.group_by()
    data['Запрос с GROUP BY'] = [[rez, 2, 3]]

    rez = perf.sort_()
    data['Запрос с сортировкой'] = [[rez, 2, 3]]

    rez = perf.count_filter()
    data['Запрос с условием фильтрации'] = [[rez, 2, 3]]

    rez = perf.add_record()
    data['Добавить запись'] = [[rez, 2, 6]]

    rez = perf.update_records()
    data['Обновление по фильтру'] = [[rez, 2, 6]]

    return data


class Perfomance():
    def __init__(self, name_):
        self.name_ = name_

    def __str__(self):
        return self.name_

    def import_from_csv(self):
        csv_path = 'movies_30000.csv'
        model_name = 'Cinema'
        if pathes.exists(csv_path):
            start = time.time()
            with open(csv_path, encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Cinema.objects.create(
                        name=row['name'],
                        movie_duration=row['movie_duration'],
                        movie_year=row['movie_year'],
                        genres=row['genres'],
                        countries=row['countries'],
                    )
            end = time.time()
            return (f"{(end - start):.3f} сек.")
        else:
            return (f" тестового  файла для загрузки/n не существует по пути: {csv_path}")

    def list_all(self):
        start = time.time()
        Cinema.objects.all()
        end = time.time()
        return  (f"{(end - start):.3f} сек.")

    def del_all_data(self):
        start = time.time()
        Cinema.objects.all().delete()
        end = time.time()
        return (f"{(end - start):.3f} сек.")

    def simple_query(self):
        start = time.time()
        is_cinema = Cinema.objects.filter(id=5).exists()
        end = time.time()
        return (f"{(end - start):.3f} сек.")

    def simple_query_not_find_record(self):
        start = time.time()
        Cinema.objects.filter(name="value").first()
        end = time.time()
        return (f"{(end - start):.3f} сек.")

    def group_by(self):
        start = time.time()
        Cinema.objects.values('movie_year').annotate(total_posts=Count('movie_year')).order_by('movie_year')

        end = time.time()
        return (f"{(end - start):.3f} сек.")

    def sort_(self):
        start = time.time()
        Cinema.objects.all().order_by('countries')
        end = time.time()
        return (f"{(end - start):.3f} сек.")

    def count_filter(self):
        start = time.time()
        Cinema.objects.all().filter(countries='[США]').aggregate(Count('countries'))
        end = time.time()
        return (f"{(end - start):.3f} сек.")

    def add_record(self):
        start = time.time()
        a = Cinema.objects.create(name="test", movie_duration="test")
        a.save()
        end = time.time()
        return (f"{(end - start):.3f} сек.")

    def update_records(self):
        start = time.time()
        query_for_filter = Cinema.objects.filter(countries='test Updated')
        query_for_filter.update(countries=('test') + ' Updated')
        # query_for_filter.save()
        end = time.time()
        return (f"{(end - start):.3f} сек.")
