"""
Creating a database using peewee orm
"""
from peewee import Model, SqliteDatabase
from peewee import CharField, IntegerField, DateField, ForeignKeyField, TextField

db = SqliteDatabase('ElCount_db.db')


class BaseModel(Model):
    class Meta:
        database = db


class Employees(BaseModel):
    first_name = CharField(max_length=60)
    last_name = CharField(max_length=60)
    birth_date = DateField()
    phone_number = IntegerField()
    email_address = CharField(max_length=120)
    is_active = CharField(max_length=5)
    total_income = IntegerField()
    savings = IntegerField()


class Clients(BaseModel):
    first_name = CharField(max_length=120)
    last_name = CharField(max_length=120)
    phone = IntegerField()
    email = CharField(max_length=100)
    address = TextField()


class Services(BaseModel):
    name = CharField(max_length=60)
    info = TextField()


class Projects(BaseModel):
    project_name = CharField(max_length=60)
    client_id = ForeignKeyField(Clients, field='id', on_delete='CASCADE')
    service_id = ForeignKeyField(Services, field='id', on_delete='SET NULL')
    price = IntegerField()
    costs = IntegerField()
    start_date = DateField()
    end_date = DateField()
    manager_id = ForeignKeyField(Employees, field='id', on_delete='SET NULL')


db.connect()
db.create_tables([Employees, Clients, Services, Projects])
