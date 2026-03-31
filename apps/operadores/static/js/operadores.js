/* ================= AGREGAR OPERADOR ================= */

const agregarOperador = document.getElementById('agregarOperador');
const abrirAgregarOperador = document.getElementById('abrirAgregarOperador');
const aceptarAgregarOperador = document.getElementById('aceptarAgregarOperador');
const cancelarAgregarOperador = document.getElementById('cancelarAgregarOperador');

abrirAgregarOperador.addEventListener('click', () => {
    agregarOperador.showModal();
});

aceptarAgregarOperador.addEventListener('click', () => {
    agregarOperador.close();
});

cancelarAgregarOperador.addEventListener('click', () => {
    agregarOperador.close();
});


/* ================= EDITAR OPERADOR ================= */

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
        document.getElementById('apellPat').value = option.dataset.apellPat || '';
        document.getElementById('apellMat').value = option.dataset.apellMat || '';
        document.getElementById('telefono').value = option.dataset.telefono || '';
        document.getElementById('fechaNac').value = option.dataset.fechaNac || '';
    }
)