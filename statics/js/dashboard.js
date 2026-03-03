document.addEventListener('DOMContentLoaded', () => {

    const btnUsuario = document.getElementById('btn-usuario');
    const btnModificarContra = document.getElementById('btn-cambiar-contra');
    const btnVenderBoletos = document.getElementById('btn-venderBoletos');

    const dialogoUsuario = document.getElementById('dialogo-perfil');
    const dialogoContra = document.getElementById('dialogo-contrasena');
    const dialogoBusqueda = document.getElementById('dialogo-buscar');


    // Abrir diálogo de perfil
    btnUsuario.addEventListener('click', () => {
        dialogoUsuario.showModal();
    });

    // Abrir diálogo de modificar contraseña
    btnModificarContra.addEventListener('click', () => {
        dialogoContra.showModal();
    });

    // Abrir diálogo de búsqueda de viaje
    btnVenderBoletos.addEventListener('click', () => {
        dialogoBusqueda.showModal();
    });


});