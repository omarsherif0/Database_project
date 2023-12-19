from flask import Flask, render_template
from app_blueprint import app_blueprint

app = Flask(__name__, static_folder="./static")
app.register_blueprint(app_blueprint)