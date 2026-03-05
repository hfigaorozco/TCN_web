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

});
