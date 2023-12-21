from flask import Blueprint,render_template, request,jsonify
from bson import json_util
from db import Database
from db_operations_ import Operations

app_blueprint = Blueprint('app_blueprint',__name__)
#Variables
db = Database()
operations = Operations()
checkBoxes=3

@app_blueprint.route("/")
def index():
    return render_template("login.html")


@app_blueprint.route("/signup")
def signup():
    return render_template("signup.html")

@app_blueprint.route("/index")
def dashboard():
    return render_template("index.html")

@app_blueprint.route("/posts")
def posts():
    collection = db.get_collection('Tour')
    tours = operations.Read(collection)
    return render_template("posts.html",tours=tours)

@app_blueprint.route("/edit")
def edit():
    return render_template("edit.html",checkBoxes=checkBoxes)

@app_blueprint.route("/new")
def new():
    return render_template("new.html",checkBoxes=checkBoxes)

@app_blueprint.route('/process_form', methods=['POST'])
def process_input():
    if request.method == "POST":
        return request.form

if __name__ == "__main__":
    app_blueprint.run(debug=True)
