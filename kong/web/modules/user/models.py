import mongoengine as me
import datetime

from flask_login import UserMixin


class User(me.Document, UserMixin):
    meta = {"collection": "users"}

    username = me.StringField(min_length=5, max_length=64)
    email = me.StringField(required=True, unique=True)
    password = me.StringField(required=True, default="")
    first_name = me.StringField(required=True, max_length=128)
    last_name = me.StringField(required=True, max_length=128)
    status = me.StringField(required=True, default="disactive")
    roles = me.ListField(me.StringField(), default=["user"])

    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )

    picture_url = me.StringField()
    resources = me.DictField()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_roles(self, roles):
        for role in roles:
            if role in self.roles:
                return True
        return False

    def get_image(self):
        if "google" in self.resources:
            return self.resources["google"].get("picture", None)
        return None
