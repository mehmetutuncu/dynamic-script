from peewee import *
from playhouse.sqlite_ext import JSONField

db = SqliteDatabase('mylocal.db')


class Script(Model):
    name = CharField()
    script = TextField()
    path = CharField()
    importable_path = CharField()
    method_requirements = JSONField(default=dict)
    initialization_params = JSONField(default=dict)

    class Meta:
        database = db


