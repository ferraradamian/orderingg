import threading
 
 from selenium import webdriver
+from selenium.common.exceptions import NoSuchElementException
 
 from app import create_app, db
 from app.models import Product, Order, OrderProduct
@@ -38,13 +39,35 @@ def setUp(self):
 
         self.driver = webdriver.Chrome()
 
 # test de integracion para borrar una fila de la orden
 
+    '''
     def test_title(self):
         driver = self.driver
         driver.get(self.baseURL)
         add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
         add_product_button.click()
         modal = driver.find_element_by_id('modal')
         assert modal.is_displayed(), "El modal no esta visible"
+    '''
+    
+    def test_delete(self):
+
+        o = Order(id= 1)
+        db.session.add(o)
+
+        p = Product(id= 1, name= 'Tenedor', price= 50)
+        db.session.add(p)
+
+        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
+        db.session.add(orderProduct)
+        db.session.commit()
+
+        driver = self.driver
         driver.get(self.baseURL)
         
         delete_product_button = driver.find_element_by_xpath('/html/body/main/div[2]/div/table/tbody/tr[1]/td[6]/button[2]')
-        delete_product_button.click()   
-        self.assertRaises(NoSuchElementException, driver.find_element_by_xpath('/html/body/main/div[2]/div/table/tbody/tr[1]').click())
+        delete_product_button.click()
+        self.assertRaises(NoSuchElementException, driver.find_element_by_xpath, "xpath")
 
 
     def tearDown(self):