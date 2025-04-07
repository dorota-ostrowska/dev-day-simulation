from flask import Blueprint, render_template


home = Blueprint("home", __name__)


@home.route("/")
@home.route("/home")
def display_home():
    return render_template("home.html")
