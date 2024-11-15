from operator import index

from django.db import models

# Create your models here.
class User(models.Model):


    username =models.CharField(max_length=15,db_index=True)
    firstname = models.CharField(max_length=15)
    lastname = models.CharField(max_length=15)
    age = models.IntegerField()
    slug = models.CharField(max_length=15,db_index=True)
    def __str__(self):
        return f'{self.username} {self.firstname} {self.lastname}'

class Task(models.Model):



    title = models.CharField(max_length=250,db_index=True)
    content = models.TextField()
    priority = models.IntegerField(default=0)
    completed = models.BooleanField( default=False)
    user = models.ForeignKey(User,related_name='tasks', on_delete=models.PROTECT,null=True)
    slug = models.CharField(max_length=15,db_index=True)

class Cinema(models.Model):
    name = models.CharField(max_length=200)
    movie_duration = models.CharField(max_length=50)
    movie_year = models.IntegerField(default=1900)
    genres = models.CharField(max_length=50, default=" ")
    countries = models.CharField(max_length=40, default=" ")


    def __str__(self):
        return self.name