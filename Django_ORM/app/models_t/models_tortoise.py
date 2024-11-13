
from tortoise.models import Model
from tortoise import fields


class TCinema(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256)
    movie_duration = fields.CharField(max_length=256)
    movie_year = fields.IntField()
    genres = fields.CharField(max_length=50)
    countries = fields.CharField(max_length=40)

    class Meta:
        table = "app_cinema"
