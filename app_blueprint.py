from flask import Blueprint, render_template, request, jsonify
from db import Database
import base64
from db_operations_ import Operations
from PIL import Image
from io import BytesIO

app_blueprint = Blueprint('app_blueprint',__name__)

#Variables
db = Database()
operations = Operations()
checkBoxes = 3

# images = []
collection = db.get_collection('Tour')
tours = operations.Read(collection)
# for tour in tours:
#     image_attribute = tour.get('image')
#     image = Image.open(BytesIO(image_attribute))
#     images.append(image)  


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
    return render_template("posts.html", tours=tours)

@app_blueprint.route("/edit")
def edit():
    tour_operater = "Tigen"
    location = "Giza"
    query = {'Tour_operator': tour_operater, "Location": location}
    doc = collection.find_one(query)
    binary_data = doc['image']
    image2 = base64.b64encode(binary_data).decode('utf-8')
    return render_template("edit.html", checkBoxes=checkBoxes, image2=image2)

@app_blueprint.route("/new")
def new():
    return render_template("new.html",checkBoxes=checkBoxes)

@app_blueprint.route('/process_form', methods=['GET'])
def process_input():
    if request.method == 'GET':
        form_data = dict(request.args)
        return jsonify(form_data)
    return jsonify({'error': 'Invalid request method'})

if __name__ == "__main__":
    app_blueprint.run(debug=True)
