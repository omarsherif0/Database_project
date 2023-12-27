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
UPLOAD_FOLDER = 'database_images'


@app_blueprint.route("/")
def index():
    return render_template("login.html")


@app_blueprint.route("/backtologin", methods=["POST", "GET"])
def back_to_login():
    form_data = {**request.form.to_dict(), **request.args.to_dict()}
    user_data = {
        'email': form_data.get('email', 'test'),
        'password': form_data.get('password', 'test'),
        'username': form_data.get('username', 'test'),
    }
    operations.Create(db.get_collection('Users'), user_data)
    return redirect(url_for("app_blueprint.index"))

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

    max_cost = int(request.args.get('maxCost', 0))
    filtered_tours = [tour for tour in tours if int(tour.get('Cost', 0)) <= max_cost]

    return render_template("posts.html", tours=filtered_tours, maxCost=max_cost)

@app_blueprint.route("/delete")
def delete():
    collection = db.get_collection('Tour')
    tour_operator = request.args.get('Tour_operator')
    collection.delete_one({"Tour_operator": tour_operator})
    return redirect(url_for("app_blueprint.posts"))

@app_blueprint.route("/edit", methods=["GET"])
def edit():
    collection = db.get_collection('Tour')
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
 
@app_blueprint.route("/edit_form", methods=['POST'])
def update():
    property_names = ['Tour_operator', 'Duration', 'Location', 'Date', 'Cost', 'Availability']
    file_data = {}
    if 'file' in request.files:
        image = process_image(request.files['file'])
        file_data['image'] = image
    form_data = {**request.form.to_dict(), **request.args.to_dict()}
    #return jsonify(form_data)
    # Loop through the property names and include them in file_data if they have a value
    for prop_name in property_names:
        prop_value = form_data.get(prop_name)
        if prop_value:
            file_data[prop_name] = prop_value
    tour_operator = form_data['currentOperator']
    location = form_data['currentLocation']
    query = {'Tour_operator': tour_operator, 'Location': location}
    #return jsonify(query)
    newvalues = { "$set": file_data }
    collection = db.get_collection('Tour')
    try:
        collection.update_one(query, newvalues)
        return redirect(url_for("app_blueprint.posts"))
    except Exception as e:
        return f'Insertion failed with error: {e}'
    
@app_blueprint.route("/new")
def new():
    return render_template("new.html")

def process_image(file):
    if file.filename == '':
        return 'No selected file'

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path) 

    with open(file_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return Binary(base64.b64decode(base64_image))

@app_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    else:
        image = process_image(request.files['file'])

    form_data = {**request.form.to_dict(), **request.args.to_dict()}
    file_data = {
        'Tour_operator': form_data.get('Tour_operator', 'test'),
        'image': image,
        'Duration': form_data.get('duration', 'test'),
        'Location': form_data.get('location', 'test'),
        'Date': form_data.get('date', 'test'),
        'Cost': form_data.get('Cost', 'test'),
        'Availability': form_data.get('Availability', '5')
    }
    collection = db.get_collection('Tour')
    operations.Create(collection, file_data)
    return redirect(url_for("app_blueprint.posts"))
    

if __name__ == "__main__":
    app_blueprint.run(debug=True, threaded=False)
