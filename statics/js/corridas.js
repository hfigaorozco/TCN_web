/* ================= BOTON Y DIALOGO AGREGAR ================= */
const abrirAgregar = document.getElementById('abrirAgregar');
const aceptarAgregar = document.getElementById('aceptarAgregar');
const cancelarAgregar = document.getElementById('cancelarAgregar');
let toastBox = document.getElementById('toast-box')
let successMsg = '<i class="fa-solid fa-check"></i> Operacion exitosa'
let errorMsg= '<i class="fa-solid fa-xmark"></i> Operacion fallida'


abrirAgregar.addEventListener('click', e => {
    agregar.showModal();
})
/*
aceptarAgregar.addEventListener('click', e => {
    agregar.close()
    let toast = document.createElement('div');
    toast.classList.add('toast');
    toast.innerHTML = msg;
    toastBox.appendChild(toast);
})
*/
/* ----------------------------------PRUEBA DE TOAST---------------------------------- */
function showToast(msg){
    agregar.close()
    let toast = document.createElement('div');
    toast.classList.add('toast');
    toast.innerHTML = msg;
    toastBox.appendChild(toast);

    if(msg.includes('fallida')){
        toast.classList.add('error');
    }

    setTimeout(()=>{toast.remove();}, 3000);
}

cancelarAgregar.addEventListener('click', e => {
    agregar.close( );
})

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

