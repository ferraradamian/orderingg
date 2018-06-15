const API = (function () {
    /**
     * Obtiene una orden desde el backend
     *
     * @param {Number} orderId id de la orden
     */
     
    // 9:22 warning  'orderId' is defined but never used. Pablo1
    function getOrder() {
        // 11:22 error Strings must use doublequote. Pablo2
        return fetch("/order/1")
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Obtiene todos los productos desde el backend
     *
     */
    function getProducts() {
        return fetch('/product')
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Obtiene todos los productos pertenecientes a una orden desde el backend
     *
     */
    function getOrderProduct(orderId, productId) {
        return fetch(`/order/${ orderId }/product/${ productId }`)
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Edita un producto de una orden
     *
     */
     
    // 45:25 warning Function 'editProduct' has too many parameters (4). Maximum allowed is 3. Pablo3
    function editProduct(orderId, productId, quantity) {
        // 47:60 error Missing semicolon. Pablo4
        const data = JSON.stringify({ quantity: quantity });

        return fetch(`/order/${ orderId }/product/${ productId }`,
            {
                // 52:25 error Strings must use doublequote. Pablo5
                method: "PUT",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: data
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }

    function deleteProduct(orderId, productId) {
        return fetch(`/order/${ orderId }/product/${ productId }`,
            {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }

    /**
     * Agrega un producto a una orden
     **/
    function addProduct(orderId, product, quantity) {
        // 83:77 error Missing semicolon. Pablo6
        const data = JSON.stringify({ quantity: quantity, product: product });

        return fetch(`/order/${ orderId }/product`,
            {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: data
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }

    return {
        getOrder,
        getProducts,
        getOrderProduct,
        editProduct,
        deleteProduct,
        addProduct
    }
})()
