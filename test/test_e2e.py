import unittest
import os
import time
import threading

from selenium import webdriver
from selenium.webdriver.support.ui import Select

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
        driver = self.driver
        driver.get(self.baseURL)
        botonAgregar = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        botonAgregar.click()
        cantidad = driver.find_element_by_id('quantity')
        cantidad.send_keys("-1")
        producto = driver.find_element_by_id('select-prod')
        producto.click()
        seleccionar = driver.find_element_by_xpath('//*[@id="select-prod"]/option[2]')
        seleccionar.click()
        time.sleep(1)
        guardar = driver.find_element_by_id('save-button')
        guardar.click()
        time.sleep(1)
        pro = Product.query.all()
        self.assertEqual(len(pro), 0, "Permitio carga negativa")

    # def test_delete(self):
    #     driver = self.driver
    #     driver.get(self.baseURL)
    #     delete_product_button = driver.find_element_by_xpath("//button[@class='button is-small is-danger']")
    #     delete_product_button.click()
    #     self.assertRaises(NoSuchElementException, driver.find_element_by_xpath, "xpath")

    def test_nomb_produc(self):
        driver = self.driver
        driver.get(self.baseURL)
        botonAgregar = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        botonAgregar.click()
        select_producto = Select(driver.find_element_by_id('select-prod'))
        select_producto.select_by_visible_text("Silla")
        time.sleep(2)
        guardar_button = driver.find_element_by_id('save-button')
        guardar_button.click()
        time.sleep(5)
        nom_produc = driver.find_element_by_xpath("// html // tbody / tr[1] / td[2]")
        assert nom_produc.text == "Silla", "El nombre del producto no existe"


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.driver.close()

if __name__ == "__main__":
    unittest.main()