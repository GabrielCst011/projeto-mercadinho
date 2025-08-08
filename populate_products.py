from app import app, db
from models import Product

with app.app_context():
    db.create_all()

    if not Product.query.first():
        p1 = Product(name="Pão De Mel", description="Doce De Leite", price=7.50)
        p2 = Product(name="Bolacha", description="Maria", price=3.50)
        p3 = Product(name="Trufa", description="Morango", price=5.75)
        db.session.add_all([p1, p2, p3])
        db.session.commit()
        print("Produtos criados com sucesso!")
    else:
        print("Produtos já existem.")