#Contains the routings and the view functions
import re
from datetime import datetime

from flask import Flask, render_template

from . import app


@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/luckydraw/")
def luckydraw():
    return render_template("luckydraw.html")

@app.route("/setting/")
def setting():
    return render_template("setting.html")