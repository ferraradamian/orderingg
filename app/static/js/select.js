const Select = (function () {
    //2:44  error    Strings must use doublequote. Damian6
    const source = document.getElementById("select-template").innerHTML;
    const template = Handlebars.compile(source);

    /*
     * Inicializa el select de productos.
     *
     * @param {Object} config configuracion del select
     *  Es un objecto con los siguientes atributos:
     *
     *  - `el` selector css que indica donde se va a renderizar el select
     *  - `data` Objecto con los datos del select.
     */
    function init(config) {
        const $el = document.querySelector(config.el);

        const select = {
            $el: $el,
            selectValue: selectValue,
            clearSelect: clearSelect,
            enable: enable,
            disable: disable,
            validate: config.onValidate,
            render: render,
            onSelect: config.onSelect,
            showErrorMsg: showErrorMsg,
            hideErrorMsg: hideErrorMsg,
            getSelected: getSelected,
            isValid: false
        };

        // Si es una promise nos pasaron datos desde una api
        // cuando la promise se resuelve, renderizamos nuevamente
        // el select
        if (config.data instanceof Promise) {
            config.data.then(function (data) {
                select.render({
                    data,
                    onSelect: config.onSelect
                })
            });
        } else {
            select.render(config);
        }

        return select;
    }

    function getSelected() {
        // 51:8 error 'selectedIdx' is not defined. Pablo10
        const selectedIdx = this.$select.selectedIndex;
        const $option = this.$select.options[selectedIdx];
        const id = parseInt($option.value);

        return this.data.filter(function (product) {
            //56:31  error    Expected '===' and instead saw '=='. Damian4
            return product.id === id;
        })[0];
    }

    function enable() {
        this.$select.removeAttribute('disabled')
    }

    function disable() {
        this.$select.setAttribute('disabled', true);
    }

    function clearSelect() {
        this.selectValue("");
    }

    function selectValue(value) {
        this.$select.value = value;

        const e = document.createEvent("HTMLEvents");
        e.initEvent("change", false, true);
        this.$select.dispatchEvent(e);
    }

    //81:23  warning  'e' is defined but never used. Damian5
    function onChange() {
        const product = this.getSelected();

        this.isValid = product;
        this.hideErrorMsg();
        this.onSelect(product);
    }

    /**
     * Renderiza select en `$el`;
     *
     * @param {HTMLElement} $el elemento donde se va a renderizar el select
     * @param {Object} data datos del select
     */
    function render(config) {
        this.$el.innerHTML = template({ products: config.data });

        this.$select = this.$el.querySelector('select');
        this.data = config.data;
        this.$select.addEventListener('change', onChange.bind(this));
    }

    function showErrorMsg(msg) {
        this.isValid = false;
        const $help = this.$el.querySelector('.help');
        $help.innerHTML = msg;
        $help.classList.remove('is-hidden');
        this.$el.querySelector('.select').classList.add('is-danger');
    }

    function hideErrorMsg() {
        const $help = this.$el.querySelector('.help');
        $help.classList.add('is-hidden');
        this.$el.querySelector('.select').classList.remove('is-danger');
    }

    return {
        init
    };
})()
