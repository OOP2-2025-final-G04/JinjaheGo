from peewee import *

db = SqliteDatabase("app.db")

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    age = IntegerField(null=True)
