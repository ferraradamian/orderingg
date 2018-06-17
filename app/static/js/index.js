import * as API from  "\app\static\js\api.js";
/**    6:19  error  'API' is not defined          no-undef E.1
  *    9:16  error  'API' is not defined          no-undef E.2 **/
(function () {
	//    5:48  error  Strings must use doublequote      quotes E.3
	const $totalPrice = document.querySelector("#total-price");

	// Estado de la aplicacion
	const state = {
		products: API.getProducts(),
		selectedProduct: null,
		quantity: 0,
		order: API.getOrder()
		//   13:6   error  Missing semicolon                 semi E.4
	};

	const refs = {}; 		//   17:8   error  Missing semicolon                 semi E.5

	/**
     * Actualiza el valor del precio total
     **/
	function updateTotalPrice() {
		try {
			const totalPrice = state.selectedProduct.price * state.quantity;
			$totalPrice.innerHTML = `Precio total: $ ${totalPrice}`;
		} catch (e) {
			$totalPrice.innerHTML = ""; //27:37  error  Strings must use doublequote      quotes E.6
		}
	}

	/**
     * Dispara la actualizacion del precio total del producto
     * al cambiar el producto seleccionado
     **/
	function onProductSelect(selectedProduct) {
		state.selectedProduct = selectedProduct;
		updateTotalPrice();
	}

	/**
     * Dispara la actualizacion del precio total del producto
     * al cambiar la cantidad del producto
     **/
	function onChangeQunatity(quantity) {
		state.quantity = quantity;
		updateTotalPrice();
	}

	function onEditProduct() {
		API.editProduct(1, state.selectedProduct.id, state.quantity)
		// 47:28 warning  'r' is defined but never used. Pablo7
			.then(function () {
				API.getOrder().then(function (data) {
					refs.table.update(data);
				});

				refs.modal.close();
			});
	}

	/**
     * Agrega un producto a una orden
     *
     **/
	function onAddProduct() {
		return API.addProduct(1, state.selectedProduct, state.quantity)
			.then(function (r) {
				if (r.error) {
					return Promise.reject({
						msg: "No puede existir 2 productos iguales en una orden"
					});
				}

				API.getOrder().then(function (data) {
					refs.table.update(data);
				});

				refs.modal.close();
			})
			.catch(function (err) {
				if (err.msg) {
					return Promise.reject(err);
				}
				return Promise.reject({
					msg: "Seleccione un producto"
				});
			});
	}

	function onDeleteProduct(productId) {
		API.deleteProduct(1, productId)
			.then(function (r) {
				if (r.error) {
					alert(r.error);
					//  console.error(r.error); 94:21  error  Unexpected console statement      no-console E.7
					//    96:1   error  Expected indentation of 4 tabs but found 16 spaces  indent E.8 con eslint index.js --fix se soluciono todos los errores de esta regla				
				} else {
					API.getOrder().then(function (data) {
						refs.table.update(data);
					});
				}
			});
	}

	/**
     * Inicializa la aplicacion
     **/
	function init() {
		refs.modal = Modal.init({
			el: "#modal",
			products: state.products,
			onProductSelect: onProductSelect,
			onChangeQunatity: onChangeQunatity,
			onAddProduct: onAddProduct,
			onEditProduct: onEditProduct
		});

		// Inicializamos la tabla
		refs.table = Table.init({
			el: "#orders",
			data: state.order
		});

		refs.global = {
			onDeleteProduct
		};
	}

	init();
	window.refs = refs;
})();

