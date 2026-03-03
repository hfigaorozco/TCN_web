/* ================= BOTON Y DIALOGO AGREGAR ================= */
let notificaciones = document.querySelector('.notificaciones')
const abrirAgregar = document.getElementById('abrirAgregar');
const aceptarAgregar = document.getElementById('aceptarAgregar');
const cancelarAgregar = document.getElementById('cancelarAgregar');
const agregar = document.getElementById('agregar')
let toastBox = document.getElementById('toast-box')

abrirAgregar.addEventListener('click', e => {
    agregar.showModal();
})

function createToast(type, icon, title, text){
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
    newToast.setTimeout = setTimeout(()=>{newToast.remove();}, 3000);
}

aceptarAgregar.onclick =  function(){
    agregar.close()
    let type = 'exito';
    let icon = "fa-solid fa-check";
    let title = 'Operación exitosa';
    let text = 'El registro ha sido exitoso';
    createToast(type, icon, title, text);
}

cancelarAgregar.onclick = function(){
    agregar.close()
    let type = 'error';
    let icon = "fa-solid fa-exclamation";
    let title = 'Ocurrió un error';
    let text = 'Hubo un error al hacer el registro';
    createToast(type, icon, title, text);
}
/* ================= BOTON Y DIALOGO EDITAR ================= */
const editar = document.getElementById('editar');
const abrirEditar = document.getElementById('abrirEditar');
const aceptarEditar = document.getElementById('aceptarEditar');
const cancelarEditar= document.getElementById('cancelarEditar');

abrirEditar.addEventListener('click', e => {
    editar.showModal( );
})

aceptarEditar.addEventListener('click', e => {
    editar.close( );
    let toast = document.createElement('div');
    toast.classList.add('toast');
    toast.innerHTML = 'Operacion Exitosa';
    toastBox.appendChild(toast);
    
})

cancelarEditar.addEventListener('click', e => {
    editar.close( );
})

/* ================= BOTON Y DIALOGO ELIMINAR ================= */
const eliminar = document.getElementById('eliminar');
const abrirEliminar = document.getElementById('abrirEliminar');
const aceptarEliminar = document.getElementById('aceptarEliminar');
const cancelarEliminar= document.getElementById('cancelarEliminar');

abrirEliminar.addEventListener('click', e => {
    eliminar.showModal( );
})

aceptarEliminar.addEventListener('click', e => {
    eliminar.close( );
})

cancelarEliminar.addEventListener('click', e => {
    eliminar.close( );
})

/* ================= BOTON Y DIALOGO VER POR FECHA Y CIUDAD ================= */
const fechaCiudad = document.getElementById('fechaCiudad');
const abrirFechaCiudad = document.getElementById('abrirFechaCiudad');
const cerrarFechaCiudad = document.getElementById('cerrarFechaCiudad');

abrirFechaCiudad.addEventListener('click', e => {
    fechaCiudad.showModal( );
})

cerrarFechaCiudad.addEventListener('click', e => {
    fechaCiudad.close( );
})

/* ================= BOTON Y DIALOGO VER BOLETOS VENDIDOS POR DIA ================= */
const boletos = document.getElementById('boletos');
const abrirBoletos = document.getElementById('abrirBoletos');
const cerrarBoletos = document.getElementById('cerrarBoletos');

abrirBoletos.addEventListener('click', e => {
    boletos.showModal( );
})

cerrarBoletos.addEventListener('click', e => {
    boletos.close( );
})

