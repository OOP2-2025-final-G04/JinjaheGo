from peewee import *
from datetime import datetime
from models.models import BaseModel

class OmikujiHistory(BaseModel):
    fortune = CharField()
    wish = CharField()
    lost = CharField()
    wait = CharField()
    health = CharField()
    study = CharField()
    created_at = DateTimeField(default=datetime.now)
