from tortoise import fields
from tortoise.models import Model


class Task(Model):


    id = fields.IntField(primary_key=True, index=True)
    title = fields.CharField(max_length=250)
    content = fields.TextField()
    priority = fields.IntField(default=0)
    completed = fields.BooleanField( default=False)
    user = fields.ForeignKeyField('models.User',related_name='task' )
    slug = fields.CharField( unique=True, index=True,max_length=250)




#print(CreateTable(Task.__table__))
