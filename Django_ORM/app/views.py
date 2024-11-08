from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from .models import User,Task
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
    user_id = request.POST['idd']
    tasks = Task.objects.filter(user_id=user_id)
    title = 'Задания'
    context = {'title':title,'list':tasks}
    return render(request,"tasks.html",context=context)
