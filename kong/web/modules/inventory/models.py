import mongoengine as me
import datetime


class Inventory(me.Document):
    meta = {"collection": "inventories"}

    name = me.StringField(min_length=5, max_length=64)
