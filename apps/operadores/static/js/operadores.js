// Agregar operador

const agregarOperador = document.getElementById('agregarOperador');
const abrirAgregarOperador = document.getElementById('abrirAgregarOperador');
const aceptarAgregarOperador = document.getElementById('aceptarAgregarOperador');
const cancelarAgregarOperador = document.getElementById('cancelarAgregarOperador');

abrirAgregarOperador.addEventListener('click', () => {
    agregarOperador.showModal();
});

cancelarAgregarOperador.addEventListener('click', () => {
    agregarOperador.close();
});


// Editar operador

const editarOperador = document.getElementById('editarOperador');
const abrirEditarOperador = document.getElementById('abrirEditarOperador');
const aceptarEditarOperador = document.getElementById('aceptarEditarOperador');
const cancelarEditarOperador = document.getElementById('cancelarEditarOperador');

abrirEditarOperador.addEventListener('click', () => {
    editarOperador.showModal();
});

aceptarEditarOperador.addEventListener('click', () => {
    editarOperador.close();
});

cancelarEditarOperador.addEventListener('click', () => {
    editarOperador.close();
});


document.getElementById('operador').addEventListener(
    'change', 
    function(){
        const option = this.options[this.selectedIndex];
        document.getElementById('nombre').value = option.dataset.nombre || '';
        document.getElementById('apellPat').value = option.dataset.apellpat || '';
        document.getElementById('apellMat').value = option.dataset.apellmat || '';
        document.getElementById('telefono').value = option.dataset.telefono || '';
        document.getElementById('fechaNac').value = option.dataset.fechanac || '';
    }
)


// Toasts
function createToast(type, icon, title, text){
    let notificaciones = document.querySelector('.notificaciones')
    let newToast = document.createElement('div');
    newToast.innerHTML =`
        <div class="toast ${type}">
            <i class="${icon}"></i>
            <div class="content">
                <div class="title">${title}</div>
                <span>${text}</span>
            </div>
            <i class="fa-solid fa-x" onclick="(this.parentElement).remove() "></i>
        </div>`;
    notificaciones.appendChild(newToast);
    newToast.setTimeout = setTimeout(()=>{
        newToast.remove();
    }, 3000);
}

function crearTipoToast(tipoMensaje, textoMensaje){
    const tipo = tipoMensaje === 'success' ? 'exito' : 'error';
    const icono = tipoMensaje === 'success' ? "fa-solid fa-circle-check" : "fa-solid fa-circle-exclamation";
    const titulo = tipoMensaje === 'success'? '¡Éxito!' : '¡Atención!'
    createToast(tipo, icono, titulo, textoMensaje);
}