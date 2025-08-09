from app import app
from models import db, Product

produtos = [
    {
        "name": "Pão De Mel",
        "description": "Doce De Leite",
        "price": 7.50,
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDoyUWkYEi-IeTrkzX7C35YwmCZaIvwIQNdg&s"
    },
    {
        "name": "Bolacha",
        "description": "Maria",
        "price": 3.50,
        "image_url": "https://w7.pngwing.com/pngs/333/997/png-transparent-cracker-biscuits-marie-biscuit-flourless-chocolate-cake-biscoito-baked-goods-food-nutrition-thumbnail.png"
    },
    {
        "name": "Trufa",
        "description": "Morango",
        "price": 5.75,
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRV5AWG-c9Mpk1ndjT29QE3GaNFrrtxduJRqw&s"
    }
]

with app.app_context():
    for data in produtos:
        produto = Product.query.filter_by(name=data["name"]).first()
        if not produto:
            produto = Product(**data)
            db.session.add(produto)
    db.session.commit()

print("Produtos adicionados com sucesso!")
