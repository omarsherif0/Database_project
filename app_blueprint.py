from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from flask_cors import CORS
from db import Database
from bson import Binary
import base64
from db_operations_ import Operations
import os


app_blueprint = Blueprint('app_blueprint',__name__)
CORS(app_blueprint, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})

#Variables
db = Database()
operations = Operations()
checkBoxes = 3
UPLOAD_FOLDER = 'Test'
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

@app_blueprint.route("/delete")
def delete():
    tour_operator = request.args.get('Tour_operator')
    collection.delete_one({"Tour_operator": tour_operator})
    return redirect(url_for("app_blueprint.posts"))

@app_blueprint.route("/edit", methods=["GET"])
def edit():
    tour_operator = request.args.get('Tour_operator')
    location = request.args.get('Location')

    query = {'Tour_operator': tour_operator, 'Location': location}

    document = collection.find_one(query)

    if document:
        try:
            binary_data = document['image']
            image_ = base64.b64encode(binary_data).decode('utf-8')
            return render_template("edit.html", checkBoxes=checkBoxes, image=image_)
        except KeyError as e:
            return jsonify({'error': f'Missing key in document: {str(e)}'})
    else:
        return jsonify({'error': 'Document not found'})
        

@app_blueprint.route("/new")
def new():
    return render_template("new.html",checkBoxes=checkBoxes)

@app_blueprint.route('/process_form', methods=['GET'])
def process_input():
    if request.method == 'GET':
        form_data = dict(request.args)
        return jsonify(form_data)
    return jsonify({'error': 'Invalid request method'})

@app_blueprint.route('/upload', methods=['GET'])
def upload():
    return render_template("test.html")


@app_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path) 

    with open(file_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    file_data = {
        'image': Binary(base64.b64decode(base64_image)),
        'file_name': file.filename,
    }

    collection = db.get_collection('Tour')
    result = operations.Create(collection, file_data)

    return result
    

if __name__ == "__main__":
    app_blueprint.run(debug=True, threaded=False)
