/* ================= FUNCION PARA CREAR TOAST ================= */
function createToast(type, icon, title, text){
    const notificaciones = document.getElementById('notificaciones');
    if (!notificaciones) return;

    let newToast = document.createElement('div');
    newToast.innerHTML =`
        <div class="toast ${type}">
            <i class="${icon}"></i>
            <div class="content">
                <div class="title">${title}</div>
                <span>${text}</span>
            </div>
            <i class="fa-solid fa-xmark" style="cursor:pointer; opacity:0.6;" onclick="(this.parentElement).parentElement.remove() "></i>
        </div>`;
    notificaciones.appendChild(newToast);
    
    // Auto-eliminar después de 4 segundos
    setTimeout(() => {
        if (newToast) newToast.remove();
    }, 4000);
}

/* ================= AGREGAR RUTA ================= */
const agregarRuta = document.getElementById('agregarRuta');
const abrirAgregar = document.getElementById('abrirAgregar');
const cancelarAgregarRuta = document.getElementById('cancelarAgregarRuta');

if (abrirAgregar) {
    abrirAgregar.addEventListener('click', () => agregarRuta.showModal());
}
if (cancelarAgregarRuta) {
    cancelarAgregarRuta.addEventListener('click', () => agregarRuta.close());
}

/* ================= EDITAR RUTA ================= */
const editarRuta = document.getElementById('editarRuta');
const abrirEditar = document.getElementById('abrirEditar');
const cancelarEditarRuta = document.getElementById('cancelarEditarRuta');
let selectedRow = null;

document.querySelectorAll('.ruta-row').forEach(row => {
    row.addEventListener('click', () => {
        document.querySelectorAll('.ruta-row').forEach(r => r.classList.remove('selected'));
        row.classList.add('selected');
        selectedRow = row;
    });
});

if (abrirEditar) {
    abrirEditar.addEventListener('click', () => {
        if (!selectedRow) {
            // Usamos un Toast de error en lugar de alert
            createToast("error", "fa-solid fa-circle-exclamation", "Atención", "Por favor, seleccione una ruta de la tabla para editar.");
            return;
        }
        document.getElementById('editCodigo').value = selectedRow.dataset.codigo;
        document.getElementById('editOrigen').value = selectedRow.dataset.origenNombre;
        document.getElementById('editDestino').value = selectedRow.dataset.destinoNombre;
        document.getElementById('editDistancia').value = selectedRow.dataset.distancia;
        editarRuta.showModal();
    });
}
if (cancelarEditarRuta) {
    cancelarEditarRuta.addEventListener('click', () => editarRuta.close());
}

/* ================= ADMINISTRAR CIUDAD ================= */
const agregarCiudad = document.getElementById('agregarCiudad');
const abrirCiudad = document.getElementById('abrirCiudad');
const cancelarCiudad = document.getElementById('cancelarCiudad');
const btnEditarCiudad = document.getElementById('btnEditarCiudad');
const btnGuardarCiudad = document.getElementById('btnGuardarCiudad');
const formCiudad = document.getElementById('formCiudad');

const inputCodigoCiudad = document.getElementById('inputCodigoCiudad');
const inputNombreCiudad = document.getElementById('inputNombreCiudad');
const hiddenOriginalCodigo = document.getElementById('original_codigo');

if (abrirCiudad) {
    abrirCiudad.addEventListener('click', () => {
        if (formCiudad) formCiudad.action = "/transportes-cuervo-negro/agregar-ciudad/";
        if (inputCodigoCiudad) inputCodigoCiudad.value = "";
        if (inputNombreCiudad) inputNombreCiudad.value = "";
        if (btnEditarCiudad) btnEditarCiudad.style.display = "none";
        if (btnGuardarCiudad) btnGuardarCiudad.style.display = "block";
        agregarCiudad.showModal();
    });
}

if (cancelarCiudad) {
    cancelarCiudad.addEventListener('click', () => {
        agregarCiudad.close();
    });
}

// Seleccionar ciudad de la tabla dentro del diálogo
document.querySelectorAll('.ciudad-row').forEach(row => {
    row.addEventListener('click', () => {
        if (inputCodigoCiudad) inputCodigoCiudad.value = row.dataset.codigo;
        if (inputNombreCiudad) inputNombreCiudad.value = row.dataset.nombre;
        if (hiddenOriginalCodigo) hiddenOriginalCodigo.value = row.dataset.codigo;

        if (btnEditarCiudad) btnEditarCiudad.style.display = "block";
        if (btnGuardarCiudad) btnGuardarCiudad.style.display = "none";

        document.querySelectorAll('.ciudad-row').forEach(r => r.style.background = "");
        row.style.background = "#eef3ff";
    });
});

if (btnEditarCiudad) {
    btnEditarCiudad.addEventListener('click', () => {
        if (formCiudad) {
            formCiudad.action = "/transportes-cuervo-negro/editar-ciudad/"; 
            formCiudad.submit();
        }
    });
}

/* ================= FILTROS EN TIEMPO REAL ================= */
function filtrarRutas() {
    const selectOrigen = document.getElementById('origen');
    const selectDestino = document.getElementById('destino');
    const allRows = document.querySelectorAll('.ruta-row');
    const filtroVacioRow = document.getElementById('filtroVacio');
    const totalCounter = document.querySelector('.card.active-card h2');

    const valOrigen = selectOrigen ? selectOrigen.value : "";
    const valDestino = selectDestino ? selectDestino.value : "";
    
    let visibleCount = 0;

    allRows.forEach(row => {
        const rowOrigen = row.getAttribute('data-origen');
        const rowDestino = row.getAttribute('data-destino');

        const matchOrigen = (valOrigen === "" || rowOrigen === valOrigen);
        const matchDestino = (valDestino === "" || rowDestino === valDestino);

        if (matchOrigen && matchDestino) {
            row.style.display = "";
            visibleCount++;
        } else {
            row.style.display = "none";
        }
    });

    if (filtroVacioRow) {
        filtroVacioRow.style.display = (visibleCount === 0 && allRows.length > 0) ? "" : "none";
    }

    if (totalCounter) {
        totalCounter.textContent = visibleCount;
    }
}

document.addEventListener('change', (e) => {
    if (e.target.id === 'origen' || e.target.id === 'destino') {
        filtrarRutas();
    }
});

document.addEventListener('DOMContentLoaded', filtrarRutas);
