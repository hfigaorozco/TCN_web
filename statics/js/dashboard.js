document.addEventListener('DOMContentLoaded', () => {

    const btnUsuario = document.getElementById('btn-usuario');
    const btnModificarContra = document.getElementById('btn-cambiar-contra');
    const dialogoUsuario = document.getElementById('dialogo-perfil');
    const dialogoContra = document.getElementById('dialogo-contrasena');


    // Abrir diálogo de perfil
    btnUsuario.addEventListener('click', () => {
        dialogoUsuario.showModal();
    });

    // Abrir diálogo de modificar contraseña
    btnModificarContra.addEventListener('click', () => {
        dialogoContra.showModal();
    });
    

});