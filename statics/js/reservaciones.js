document.addEventListener('DOMContentLoaded', () => {

    const btnMostrar = document.getElementById('mostrarBoleto');
    const dialogo = document.getElementById('dialogoBoleto');
    const btnCerrar = document.getElementById('btnCerrar');

    // Abrir diálogo
    btnMostrar.addEventListener('click', () => {
        dialogo.showModal();
    });

    // Cerrar diálogo
    btnCerrar.addEventListener('click', () => {
        dialogo.close();
    });

});