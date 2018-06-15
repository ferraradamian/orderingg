const Table = (function () {
    //2:44  error    Strings must use doublequote.Damian1
    const source = document.getElementById("table-template").innerHTML;
    const template = Handlebars.compile(source);

    /*
     * Inicializa la tabla.
     *
     * @param {Object} config configuracion de la tabla
     *  Es un objecto con los siguientes atributos:
     *
     *  - `el` selector css que indica donde se va a renderizar la tabla
     *  - `data` Objecto con los datos de la tabla.
     */
    function init(config) {
        const $el = document.querySelector(config.el);
        let data = config.data;

        // Si es una promise nos pasaron datos desde una api
        // cuando la promise se resuelve, renderizamos nuevamente
        // la tabla
        if (config.data instanceof Promise) {
            config.data.then(function (data) {
                //24:34  error    Missing semicolon. Damian2
                render($el, data);
            });
        } else {
            data = {};
        }

        render($el, data);

        return {
            update: render.bind(null, $el)
        //35:10  error    Missing semicolon. Damian3
        };
    }

    /**
     * Renderiza la tabla en `$el`;
     *
     * @param {HTMLElement} $el elemento donde se va a renderizar la tabla
     * @param {Object} data datos de la tabla
     */
    function render($el, data) {
        $el.innerHTML = template(data);
    }

    return {
        init
    };
})()
