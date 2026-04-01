document.addEventListener('DOMContentLoaded', () => {

    const btnUsuario         = document.getElementById('btn-usuario');
    const btnModificarContra = document.getElementById('btn-cambiar-contra');
    const btnVenderBoletos   = document.getElementById('btn-venderBoletos');
    const btnSalir           = document.getElementById('btn-salir');
    const btnContinuar       = document.querySelector('.dialog-buscar-btn');

    const dialogoUsuario  = document.getElementById('dialogo-perfil');
    const dialogoContra   = document.getElementById('dialogo-contrasena');
    const dialogoBusqueda = document.getElementById('dialogo-buscar');

    // Abrir diálogo de perfil
    btnUsuario.addEventListener('click', () => {
        dialogoUsuario.showModal();
    });

    // Abrir diálogo de modificar contraseña
    btnModificarContra.addEventListener('click', () => {
        dialogoUsuario.close();
        dialogoContra.showModal();
    });

    // Abrir diálogo de búsqueda de viaje
    btnVenderBoletos.addEventListener('click', () => {
        dialogoBusqueda.showModal();
    });

    // Botón Continuar — validar y navegar
    btnContinuar.addEventListener('click', () => {
        const selects   = dialogoBusqueda.querySelectorAll('select');
        const fecha     = dialogoBusqueda.querySelector('input[type="date"]');
        const pasajeros = dialogoBusqueda.querySelector('.dialog-buscar-pasajeros');

        const origen   = selects[0].value;
        const destino  = selects[1].value;
        const fechaVal = fecha.value;
        const pasVal   = pasajeros.value;

        if (!origen)  { alert('Selecciona el origen.'); return; }
        if (!destino) { alert('Selecciona el destino.'); return; }
        if (origen === destino) { alert('El origen y el destino no pueden ser iguales.'); return; }
        if (!fechaVal) { alert('Selecciona una fecha.'); return; }
        if (!pasVal || parseInt(pasVal) < 1) { alert('Ingresa el número de pasajeros.'); return; }

        const params = new URLSearchParams({
            origen:    origen,
            destino:   destino,
            fecha:     fechaVal,
            pasajeros: pasVal,
        });

        window.location.href = `${window.__urlBoletos}?${params.toString()}`;
    });

    // Cerrar sesión
    btnSalir.addEventListener('click', () => {
        dialogoUsuario.close();
        createToast('error', 'fa-solid fa-right-from-bracket', 'Cerrando sesión...', 'Hasta pronto');
        setTimeout(() => {
            window.location.href = window.__urlLogin;
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