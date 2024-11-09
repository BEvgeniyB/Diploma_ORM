from django import forms



class UserRegister(forms.Form):
    username = forms.CharField(min_length=4,max_length=30 ,label="Введите Фамилию")
    firstname = forms.CharField(min_length=4, max_length=30, label="Введите Имя")
    lastname = forms.CharField(min_length=4, max_length=30, label="Введите Отчество")
    age = forms.IntegerField(min_value=19, max_value=120, label="Введите свой возраст")
