from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from config import Config
from db import db
from models import Product, User
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

app = Flask(__name__)

# Carrega configurações da sua classe Config
app.config.from_object(Config)

# Garante que a SECRET_KEY esteja definida
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("A variável de ambiente SECRET_KEY não está definida! Defina antes de rodar o app.")
app.secret_key = secret_key

# Admin CPF (para permissões administrativas)
ADMIN_CPF = os.getenv("ADMIN_CPF", "")

# Inicializa o banco com a app
db.init_app(app)

# Decorator para rotas que precisam de admin
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Acesso negado.', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        password = request.form.get('password')
        user = User.query.filter_by(cpf=cpf).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_cpf'] = user.cpf
            session['is_admin'] = (user.cpf == ADMIN_CPF)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('CPF ou senha incorretos.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sessão.', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        password = request.form.get('password')

        if not cpf or not password:
            flash('CPF e senha são obrigatórios.', 'error')
            return redirect(url_for('register'))

        if len(cpf) != 11 or not cpf.isdigit():
            flash('CPF deve conter exatamente 11 números.', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado.', 'error')
            return redirect(url_for('register'))

        try:
            password_hash = generate_password_hash(password)
            novo_usuario = User(cpf=cpf, password_hash=password_hash, is_admin=False)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
            flash('Erro interno. Tente novamente.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/api/products")
def get_products():
    products = Product.query.all()
    return jsonify([p.serialize() for p in products])

@app.route("/carrinho")
def carrinho():
    return render_template("carrinho.html")

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
