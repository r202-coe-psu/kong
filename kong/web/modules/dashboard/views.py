from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from kong import models
from ... import forms

import datetime

module = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@module.route("/admin")
@login_required
def index_admin():
    return render_template(
        "/dashboard/index-admin.html",
    )


@module.route("/")
@module.route("")
@login_required
def index():
    print("Hello")
    user = current_user
    # if "admin" in user.roles:
    #     return redirect(url_for("dashboard.index_admin"))

    return render_template("/dashboard/index.html")
