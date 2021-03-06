from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    username = fields.TextField()
    password = fields.TextField()
    building = fields.TextField()

    class Meta:
        table = "users"


class Offices(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    class Meta:
        table = "offices"


class OfficeDetails(Model):
    id = fields.IntField(pk=True)
    office = fields.ForeignKeyField('models.Offices')
    renter = fields.TextField()
    date_of_receipt = fields.DateField()
    date_of_claiming = fields.DateField()
    amount = fields.FloatField()
    notes = fields.TextField()

    class Meta:
        table = "office_details"


class Expenses(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    type = fields.TextField()
    amount = fields.FloatField()
    date = fields.DateField()

    class Meta:
        table = "expenses"


class Notifications(Model):
    id = fields.IntField(pk=True)
    office_details = fields.ForeignKeyField('models.OfficeDetails')
    seen = fields.IntField(default=0)
