const agregar = document.getElementById('agregar');
const abrirAgregar = document.getElementById('abrirAgregar');
const aceptarAgregar = document.getElementById('aceptarAgregar');
const cancelarAgregar = document.getElementById('cancelarAgregar');

abrirAgregar.addEventListener('click', e => {
    agregar.showModal( );
})

aceptarAgregar.addEventListener('click', e => {
    agregar.close( );
})

cancelarAgregar.addEventListener('click', e => {
    agregar.close( );
})