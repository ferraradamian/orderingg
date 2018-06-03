import unittest
import os
import time
import threading

from selenium import webdriver

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

class Ordering(unittest.TestCase):
    #     # Creamos la base de datos de test
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.baseURL = 'http://localhost:5000'

        db.session.commit()
        db.drop_all()
        db.create_all()

        # start the Flask server in a thread
        threading.Thread(target=self.app.run).start()

        # give the server a second to ensure it is up
        time.sleep(1)

        self.driver = webdriver.Chrome()

    # def test_title(self):
    #     driver = self.driver
    #     driver.get(self.baseURL)
    #     add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
    #     add_product_button.click()
    #     modal = driver.find_element_by_id('modal')
    #     assert modal.is_displayed(), "El modal no esta visible"

    def test_cantidadNegativa(self):
        produc = Product(name="Sillita", price=120)
        db.session.add(produc)
        Orden = Order(id= 1)
        db.session.add(Orden)
        db.session.commit() 
        driver = self.driver
        driver.get(self.baseURL)
        botonAgregar = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        botonAgregar.click()
        producto = driver.find_element_by_id('select-prod')
        producto.click()
        time.sleep(1)
        seleccionar = driver.find_element_by_xpath('//*[@id="select-prod"]/option[2]')
        seleccionar.click()
        time.sleep(2)
        cantidad = driver.find_element_by_id('quantity')
        cantidad.send_keys("-1")
        time.sleep(2)
        guardar = driver.find_element_by_id('save-button')
        guardar.click()
        time.sleep(1)
        pro = Product.query.all()
        self.assertEqual(len(pro), 0, "Permitio carga negativa")

    #Hacer un test de integración con Selenium para probar que se elimine la fila correspondiente al producto que se borra al utilizar el botón de borrado.
		
    def test_delete(self):
	
        #Creacion de  los productos
        prod1 = Product(id= 1, name= 'Armario', price= 50)
        db.session.add(prod1)
        prod2 = Product(id= 2, name= 'Cajon', price= 30)
        db.session.add(prod2)
        prod3 = Product(id= 3, name= 'Silla', price= 10)
        db.session.add(prod3)		

        #Creo una orden
        Orden = Order(id= 1)
        db.session.add(Orden)

        #Añado los productos a la orden
        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= prod1)
        db.session.add(orderProduct)
        orderProduct = OrderProduct(order_id= 1, product_id= 2, quantity= 1, product= prod2)
        db.session.add(orderProduct)
        orderProduct = OrderProduct(order_id= 1, product_id= 3, quantity= 1, product= prod3)
        db.session.add(orderProduct)		
        db.session.commit()

        driver = self.driver
        driver.get(self.baseURL)

        time.sleep(2)

        delete_product_button = driver.find_element_by_xpath('//*[@id="orders"]/table/tbody/tr[3]/td[6]/button[2]')
        delete_product_button.click()
        
        time.sleep(2)

        op = OrderProduct.query.all()

        # Verifica que se haya borrado el producto de la lista de productos
        self.assertEqual(len(op), 2, "No se pudo borrar el producto")


        #Verifica que se haya borrado el producto correcto
        self.assertEqual(op[0].product, prod1, "No se borró el producto correcto")
        self.assertEqual(op[1].product, prod2, "No se borró el producto correcto")

 		 
    #Hacer un test de integración con Selenium para verificar que se haya solucionado el bug
    # no mostraba el nombre del producto en la tabla, arreglado en la Actividad 2.
    def test_nomb_produc(self):
        p = Product(name="Taza", price=210)
        db.session.add(p)
        db.session.commit()

        order = Order(id=1)
        orderProduct = OrderProduct(order_id=1, product_id=1, quantity=1, product=p)
        order.products.append(orderProduct)
        db.session.add(order)
        db.session.commit()

        driver = self.driver
        driver.get(self.baseURL)

        nom_produc = driver.find_element_by_xpath("// html // tbody / tr[1] / td[2]")
        time.sleep(6)
        assert nom_produc.text == "Taza", "El nombre del producto no existe en la tabla"

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
