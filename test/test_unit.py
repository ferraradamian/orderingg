import os
import unittest

from flask import json
from flask_testing import TestCase

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

class OrderingTestCase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app = create_app()
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )
        return app

    # Creamos la base de datos de test
    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

    # Destruimos la base de datos de test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_iniciar_sin_productos(self):
        resp = self.client.get('/product')
        data = json.loads(resp.data)

        assert len(data) == 0, "La base de datos tiene productos"

    def test_crear_producto(self):
        data = {
            'name': 'Tenedor',
            'price': 50
        }

        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')

        # Verifica que la respuesta tenga el estado 200 (OK)
        self.assert200(resp, "Falló el POST")
        p = Product.query.all()

        # Verifica que en la lista de productos haya un solo producto
        self.assertEqual(len(p), 1, "No hay productos")
        
    def test_get_orderProduct(self):
        producto = Product(id=22, name="Mantel", price=125)
        orden = Order(id=33)
        ordenProducto = OrderProduct(product_id=22, order_id=33, product=producto, quantity=8)
        db.session.add(producto)
        db.session.add(orden)
        db.session.add(ordenProducto)
        db.session.commit()
        respuesta = self.client.get('/order/33/product/22')
        self.assert200(respuesta, "No esta ese producto o esa orden")
        
    def test_get_product(self):
        p = Product(name="termo", price=210)
        db.session.add(p)
        db.session.commit()
        resp = self.client.get('/product')
        product = json.loads(resp.data)
        self.assertEqual(len(product), 1, "No obtuve el producto que cree")

    def test_orderProduc_negativo(self):
        p = Product(name="termo", price=210)
        db.session.add(p)
        db.session.commit()
        order = Order(id=1)
        orderProduct = OrderProduct(order_id=1, product_id=1, quantity=-1, product=p)
        order.products.append(orderProduct)
        db.session.add(order)
        db.session.commit()
        op = OrderProduct.query.all()
        self.assertEqual(len(op), 0, "Se creo el producto")

if __name__ == '__main__':
    unittest.main()

