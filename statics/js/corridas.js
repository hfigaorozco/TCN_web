const agregar = document.getElementById('agregar');
const abrirAgregar = document.getElementById('abrirAgregar');
const cerrarAgregar = document.getElementById('cerrarAgregar');

abrirAgregar.addEventListener('click', e => {
    agregar.showModal( );
})

cerrarAgregar.addEventListener('click', e => {
    agregar.close( );
})