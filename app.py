from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/sales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), unique=True)
    price = db.Column(db.Integer)

    def __init__(self, description, price):
        self.description = description
        self.price = price


db.create_all()


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description', 'price')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/products', methods=['Post'])
def create_product():
    description = request.json['description']
    price = request.json['price']

    new_product = Product(description, price)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    description = request.json['description']
    price = request.json['price']
    product.description = description
    product.price = price

    db.session.commit()

    return product_schema.jsonify(product)


@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Api rest en Python con flask '})


if __name__ == "__main__":
    app.run(debug=True)
