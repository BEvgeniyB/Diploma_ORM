from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from .models import User,Task
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
    user_id = request.POST['idd']
    tasks = Task.objects.filter(user_id=user_id)
    there_is = Task.objects.filter(user_id=user_id).exists()
    title = 'Задания'
    context = {'title':title,'list':tasks,'there_is':there_is}
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
