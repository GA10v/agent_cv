import sqlite3 as sq
from peewee import *


db = SqliteDatabase('base.db')


class BaseModel(Model):    
    class Meta:
        database = db
        

class Base(BaseModel):
    class Meta:
        db_table = 'vacansies'
        order_by = ('time',)

    name = CharField()
    link = CharField()
    company = CharField()
    area = CharField()
    experience = TextField()
    salary = CharField()
    skills = TextField()
    time = TextField()


class User(BaseModel):
    class Meta:
        db_table = 'users'

    user_id = CharField(unique=True)

        
class View(BaseModel):
    class Meta:
        indexes = ((('user_id', 'link'), True),)

    user_id = ForeignKeyField(User, backref='users')
    link = ForeignKeyField(Base.link, backref='views')


class Like(BaseModel):
    class Meta:
        indexes = ((('user_id', 'link'), True),)

    user_id = ForeignKeyField(User, backref='users')
    link = ForeignKeyField(Base.link, backref='likes')