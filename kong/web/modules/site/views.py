from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from kong import models
from ... import forms

import datetime

module = Blueprint("site", __name__, template_folder="templates")


@module.route("/")
def index():

    return render_template(
        "site/index.html",
    )
