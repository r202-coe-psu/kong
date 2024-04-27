from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from kong import models
from ... import forms

import datetime

module = Blueprint("site", __name__)


@module.route("")
def index_admin():
    return render_template(
        "index.html",
    )
