from flask import Flask, jsonify, render_template
from config import Config
from db import db
from models import Product

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/api/products")
def get_products():
    products = Product.query.all()
    return jsonify([p.serialize() for p in products])

@app.route("/")
def index():
    return render_template("index.html")
