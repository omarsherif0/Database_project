from flask import Flask,Blueprint,render_template, request, redirect, url_for

app_blueprint = Blueprint('app_blueprint',__name__)
#Variables
checkBoxes=3
tours = [
    {'Tour_operator':'Tiger Nixon', 'Date':'Jan 15, 2023, 10:00AM', 'Location':'Pyramids', 'Duration':'6 hours', 'Cost':'$50 per person','Availability':'7 spots'},
    {'Tour_operator':'Yawan Kalidas', 'Date':'February 19, 2023, 8:00AM', 'Location':'Cairo', 'Duration':'3 hours', 'Cost':'$20 per person','Availability':'2 spots'}
]

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
        return redirect(url_for('app_blueprint.index'))

if __name__ == "__main__":
    app_blueprint.run(debug=True)
