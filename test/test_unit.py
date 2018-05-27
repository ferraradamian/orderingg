    # Verifica que en la lista de productos haya un solo producto
         self.assertEqual(len(p), 1, "No hay productos")
		 
    # test de metodo delete
	
+    def test_delete(self):
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
+        resp = self.client.delete('order/1/product/1')
+
+        self.assert200(resp, "Fallo el metodo delete")

 if __name__ == '__main__':
     unittest.main()

    # test añadir productos sin nombre
	
+    def test_name_vacio(self):
+        data = {
+            'name': '',
+            'price': 50
+        }
+
+        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')
+
+        assert resp != 200, 'Fallo el test, se creo un producto de nombre vacio'
+
 if __name__ == '__main__':
     unittest.main()