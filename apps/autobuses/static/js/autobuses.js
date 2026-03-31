// ── AUTOBUSES.JS ──

document.addEventListener('DOMContentLoaded', () => {

    // Abrir diálogo: Registrar autobús
    document.getElementById('abrirAgregar').addEventListener('click', () => {
        document.getElementById('dialogo-agregar-bus').showModal();
    });

    // Abrir diálogo: Baja de autobús
    document.getElementById('abrirEliminar').addEventListener('click', () => {
        document.getElementById('dialogo-eliminar-bus').showModal();
    });

    // Abrir diálogo: Nueva marca
    document.getElementById('abrirAgregarMarca').addEventListener('click', () => {
        document.getElementById('dialogo-agregar-marca').showModal();
    });

    // Abrir diálogo: Nuevo modelo
    document.getElementById('abrirAgregarModelo').addEventListener('click', () => {
        document.getElementById('dialogo-agregar-modelo').showModal();
    });

    // Calcular asientos automáticamente según tipo de autobús
    document.getElementById('bus-servicio').addEventListener('change', function () {
        const asientosPorTipo = {
            'PLUS': 44,
            'PLAT': 36,
        };
        const cantAsientos = asientosPorTipo[this.value] || 0;
        document.getElementById('bus-asientos-hidden').value = cantAsientos;
    });

    // Submit manual del form de agregar autobús
    document.querySelector('#dialogo-agregar-bus form').addEventListener('submit', function (e) {
        e.preventDefault();

        // Verificar que el hidden tenga el valor correcto antes de enviar
        const tipo = document.getElementById('bus-servicio').value;
        const asientosPorTipo = { 'PLUS': 44, 'PLAT': 36 };
        document.getElementById('bus-asientos-hidden').value = asientosPorTipo[tipo] || 0;

        this.submit();
    });

});