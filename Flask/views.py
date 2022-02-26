#Contains the routings and the view functions
import re
from datetime import datetime

from flask import Flask, render_template

from . import app


@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html")

#Example
@app.route("/hello/") #handles both url
@app.route("/hello/<name>") 
def hello_there(name = None): #name html same as function name
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )
#End of example


#Example of sending data straight from static files (without needing template)
@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
#End of example

@app.route("/project/")
@app.route("/project/<name>")
def project(name = None):
    
    #Make sure name is clean and can be displayed
    clean_name = None
    if not name == None:
        try:
            match_object = re.match("[a-zA-Z]+", name)

            if match_object:
                clean_name = match_object.group(0)
        except:
            pass

    return render_template(
        "project.html",
        name = clean_name
    )

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/about/")
def about():
    return render_template("about.html")