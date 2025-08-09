from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, abort, session
from config import Config
from db import db
from models import Product
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv("SECRET_KEY")
db.init_app(app)

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Acesso negado.", "error")
            return redirect(url_for("index"))
        return func(*args, **kwargs)
    return wrapper

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

@app.route("/login-admin")
def login_admin():
    session["is_admin"] = True
    flash("Logado como admin.", "success")
    return redirect(url_for("admin"))

@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        image_url = request.form.get("image_url")

        if not name or not price:
            flash("Nome e preço são obrigatórios!", "error")
            return redirect(url_for("admin"))

        try:
            price = float(price)
        except ValueError:
            flash("Preço inválido!", "error")
            return redirect(url_for("admin"))

        novo_produto = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(novo_produto)
        db.session.commit()
        flash("Produto criado com sucesso!", "success")
        return redirect(url_for("admin"))

    produtos = Product.query.all()
    return render_template("admin.html", produtos=produtos)

@app.route("/admin/delete/<int:product_id>", methods=["POST"])
@admin_required
def delete_product(product_id):
    produto = Product.query.get_or_404(product_id)
    db.session.delete(produto)
    db.session.commit()
    flash("Produto excluído com sucesso!", "success")
    return redirect(url_for("admin"))  

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
