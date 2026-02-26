/* ================= AGREGAR RUTA ================= */

const agregarRuta = document.getElementById('agregarRuta');
const abrirAgregar = document.getElementById('abrirAgregar');
const aceptarAgregarRuta = document.getElementById('aceptarAgregarRuta');
const cancelarAgregarRuta = document.getElementById('cancelarAgregarRuta');

abrirAgregar.addEventListener('click', () => {
    agregarRuta.showModal();
});

aceptarAgregarRuta.addEventListener('click', () => {
    agregarRuta.close();
});

cancelarAgregarRuta.addEventListener('click', () => {
    agregarRuta.close();
});


/* ================= EDITAR RUTA ================= */

const editarRuta = document.getElementById('editarRuta');
const abrirEditar = document.getElementById('abrirEditar');
const aceptarEditarRuta = document.getElementById('aceptarEditarRuta');
const cancelarEditarRuta = document.getElementById('cancelarEditarRuta');

abrirEditar.addEventListener('click', () => {
    editarRuta.showModal();
});

aceptarEditarRuta.addEventListener('click', () => {
    editarRuta.close();
});

cancelarEditarRuta.addEventListener('click', () => {
    editarRuta.close();
});


/* ================= AGREGAR CIUDAD ================= */

const agregarCiudad = document.getElementById('agregarCiudad');
const abrirCiudad = document.getElementById('abrirCiudad');
const aceptarCiudad = document.getElementById('aceptarCiudad');
const cancelarCiudad = document.getElementById('cancelarCiudad');

abrirCiudad.addEventListener('click', () => {
    agregarCiudad.showModal();
});

aceptarCiudad.addEventListener('click', () => {
    agregarCiudad.close();
});

cancelarCiudad.addEventListener('click', () => {
    agregarCiudad.close();
});