# Solucionado tipo D100 Missing docstring in public module. Pablo

"""Encontre que haciendo esto se solucionaba."""

from app.models import Product, Order, OrderProduct
from app import create_app, db

app = create_app()
app.app_context().push()
# Solucionado tipo E302 expected 2 blank lines, found 1. Pablo


def addOrders():
    """Agrega una orden."""
    # Solucionado tipo D103 Missing docstring in public function. Pablo.
    orders = Order.query.all()

    if not orders:
        orders = [
            {
                "products": [
                    {
                        "id": 1,
                        "quantity": 6
                    },
                    {
                        "id": 2,
                        "quantity": 1
                    }
                ]
            },
            {
                "products": [
                    {
                        "id": 3,
                        "quantity": 6
                    },
                    {
                        "id": 4,
                        "quantity": 6
                    }
                ]
            }
        ]

        for order_data in orders:
            order = Order()

            for product in order_data['products']:
                orderProduct = OrderProduct(quantity=product['quantity'])
                orderProduct.product = Product.query.get(product['id'])
                order.products.append(orderProduct)

            db.session.add(order)

        db.session.commit()
# Solucionado tipo E302 expected 2 blank lines, found 1. Pablo


def addProducts():
    """Agrega un producto."""
    # Solucionado tipo D103 Missing docstring in public function. Pablo.
    products = Product.query.all()
    if not products:
        p = Product(name="Silla", price=500)
        db.session.add(p)
        p = Product(name="Mesa", price=2000)
        db.session.add(p)
        p = Product(name="Vaso", price=150)
        db.session.add(p)
        p = Product(name="Individual", price=250)
        db.session.add(p)
        db.session.commit()


# Solucionado E305 expected 2 blank lines after function definition. Pablo.
if __name__ == '__main__':
    addProducts()
    addOrders()
