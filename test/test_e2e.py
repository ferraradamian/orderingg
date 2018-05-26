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

    def test_nomb_produc(self):
        driver = self.driver
        driver.get(self.baseURL)
        #nom_produc = driver.find_element_by_xpath("//td[contains(text(),'Individual')]")
        nom_produc = driver.find_element_by_xpath("// html // tbody / tr[1] / td[2]")
        assert nom_produc.text != "", "El nombre del producto no existe"

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.driver.close()

if __name__ == "__main__":
    unittest.main()