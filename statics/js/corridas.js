/* ================= BOTON Y DIALOGO AGREGAR ================= */
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
})

cancelarEditar.addEventListener('click', e => {
    editar.close( );
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
