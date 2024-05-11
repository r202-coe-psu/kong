from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from . import models
from ... import forms

import datetime

module = Blueprint(
    "inventory", __name__, url_prefix="/inventories", template_folder="templates"
)


@module.route("/")
def index():
    print("test query", models.Inventory.objects())

    return render_template(
        "inventory/index.html",
    )
