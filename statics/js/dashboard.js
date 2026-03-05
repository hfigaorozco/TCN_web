document.addEventListener('DOMContentLoaded', () => {

    const btnUsuario        = document.getElementById('btn-usuario');
    const btnModificarContra = document.getElementById('btn-cambiar-contra');
    const btnVenderBoletos  = document.getElementById('btn-venderBoletos');
    const btnSalir          = document.getElementById('btn-salir');

    const dialogoUsuario  = document.getElementById('dialogo-perfil');
    const dialogoContra   = document.getElementById('dialogo-contrasena');
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

    // Cerrar sesión: cierra el dialog, muestra toast y redirige al terminar
    btnSalir.addEventListener('click', () => {
        dialogoUsuario.close();
        createToast(
            'error',
            'fa-solid fa-right-from-bracket',
            'Cerrando sesión...',
            'Hasta pronto'
        );
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 3000);
    });

});


/* ================= FUNCION PARA CREAR TOAST ================= */
function createToast(type, icon, title, text) {
    const notificaciones = document.querySelector('.notificaciones');
    const newToast = document.createElement('div');
    newToast.innerHTML = `
        <div class="toast ${type}">
            <i class="${icon}"></i>
            <div class="content">
                <div class="title">${title}</div>
                <span>${text}</span>
            </div>
            <i class="fa-solid fa-x" onclick="this.closest('.toast').parentElement.remove()"></i>
        </div>`;
    notificaciones.appendChild(newToast);
    setTimeout(() => { newToast.remove(); }, 3000);
}