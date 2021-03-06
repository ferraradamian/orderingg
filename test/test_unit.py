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
        producto1 = json.loads(respuesta.data)
        self.assertEqual(producto1['id'], producto.id, "No se borró el producto correcto")
        self.assert200(respuesta, "No esta ese producto o esa orden")

    #Hacer un test de unidad para probar el funcionamiento del método GET en el endpoint /product.
    def test_get_product(self):
        p = Product(id=11, name="termo", price=210)
        db.session.add(p)
        db.session.commit()
        resp = self.client.get('/product')
        product2 = json.loads(resp.data)
        self.assertEqual(product2[0]['id'], 11, "No se borró el producto correcto")


    #Hacer un test de unidad para verificar que no se pueda crear una instancia de la clase OrderProduct si el atributo quantity es un entero negativo.
    def test_orderProduc_negativo(self):
        #op_antes = OrderProduct.query.all()
        p = Product(name="termo", price=210)
        db.session.add(p)
        db.session.commit()
        order = Order(id=1)
        orderProduct = OrderProduct(order_id=1, product_id=1, quantity=-1, product=p)
        order.products.append(orderProduct)
        db.session.add(order)
        db.session.commit()
        resp = self.client.get('/order/1/product/1')#obtengo la tupla del producto de la orden id=1 y el producto id=1
        data = json.loads(resp.data)
        self.assertNotEqual(data['id'], 1, "Fallo, Obtuve el producto en la orden con cant negativa")
        #si el id del producto es igual al ingresado en la orden creada, se ingreso el produto con cant negativa

    # test de metodo delete
    def test_delete(self):
        o = Order(id=1)
        db.session.add(o)
        p = Product(id=1, name='Tenedor', price=50)
        db.session.add(p)
        orderProduct = OrderProduct(order_id=1, product_id=1, quantity=1, product=p)
        db.session.add(orderProduct)
        db.session.commit()
        respuesta = self.client.get('order/1')
        orden1 = json.loads(respuesta.data)
        self.assertEqual(len(orden1['products']), 1, "No hay un producto")
        resp = self.client.delete('order/1/product/1')
        self.assert200(resp, "Fallo el metodo delete")
        resp = self.client.get('order/1')
        orden1 = json.loads(resp.data)
        self.assertEqual(len(orden1['products']), 0, "Hay productos")
    
    ##No muestro mensaje porque se borro correctamente

    # test añadir productos sin nombre
    def test_name_vacio(self):
        producto = Product(id=1, name='', price=2)
        db.session.add(producto)
        db.session.commit()
        p = Product.query.get(1)
        assert p.name != '', 'Fallo el test, se creo un producto de nombre vacio'

if __name__ == '__main__':
    unittest.main()
