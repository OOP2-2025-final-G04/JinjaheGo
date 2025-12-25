from peewee import *
import os

db = SqliteDatabase("app.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    age = IntegerField(null=True)


def initialize_database():
    db.connect()
    db.create_tables([User])
