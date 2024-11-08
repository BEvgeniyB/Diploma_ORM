from tortoise import fields
from tortoise.models import Model


class User(Model):

    id = fields.IntField(primary_key=True, index=True)
    username =fields.CharField(max_length=15)
    firstname = fields.CharField(max_length=15)
    lastname = fields.CharField(max_length=15)
    age = fields.IntField()
    slug = fields.CharField(unique=True,max_length=15,index=True)
    #task = fields.ForeignKeyField('models.Task','user')

#print(CreateTable(User.__table__))
