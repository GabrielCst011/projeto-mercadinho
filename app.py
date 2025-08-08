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

@app.route("/carrinho")
def carrinho():
    return render_template("carrinho.html")

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
