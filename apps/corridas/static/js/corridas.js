/* ================= BOTON Y DIALOGO AGREGAR ================= */
const abrirAgregar = document.getElementById('abrirAgregar');
const aceptarAgregar = document.getElementById('aceptarAgregar');
const cancelarAgregar = document.getElementById('cancelarAgregar');
const agregar = document.getElementById('agregar')
let toastBox = document.getElementById('toast-box')
const formAgregar = document.getElementById('form-agregar')

abrirAgregar.addEventListener('click', e => {
    formAgregar.reset();
    agregar.showModal();
})

cancelarAgregar.addEventListener('click', e => {
    formAgregar.reset();
    agregar.close();
})

/* ================= FUNCION PARA CREAR TOAST ================= */
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

/* ================= FUNCION PARA CREAR TOAST ================= */
function crearTipoToast(tipoMensaje, textoMensaje){
    const tipo = tipoMensaje === 'success' ? 'exito' : 'error';
    const icono = tipoMensaje === 'success' ? "fa-solid fa-circle-check" : "fa-solid fa-circle-exclamation";
    const titulo = tipoMensaje === 'success'? '¡Éxito!' : '¡Atención!'
    createToast(tipo, icono, titulo, textoMensaje);
}

/* ================= FUNCION PARA CREAR TOAST DE ERROR Y CERRAR DIALOG ================= */
cancelarAgregar.onclick = function(){
    formAgregar.reset();
    agregar.close();
}


/* ================= BOTON Y DIALOGO EDITAR ================= */
const editar = document.getElementById('editar');
const abrirEditar = document.getElementById('abrirEditar');
const aceptarEditar = document.getElementById('aceptarEditar');
const cancelarEditar= document.getElementById('cancelarEditar');
let selectedRow = null;

document.querySelectorAll('.corrida-row').forEach(row => {
    row.addEventListener('click', () => {
        document.querySelectorAll('.corrida-row').forEach(r => r.classList.remove('selected'));
        row.classList.add('selected');
        selectedRow = row;
    });
});

if (abrirEditar) {
    abrirEditar.addEventListener('click', () => {
        if (!selectedRow) {
            // Usamos un Toast de error en lugar de alert
            createToast("error", "fa-solid fa-circle-exclamation", "Atención", "Por favor, seleccione una corrida de la tabla para editar.");
            return;
        }
        document.getElementById('editar_corrida').value = selectedRow.dataset.numero
        document.getElementById('editarOperador').value = selectedRow.dataset.operador;
        document.getElementById('editarAutobus').value = selectedRow.dataset.autobus;
        document.getElementById('editarFechaSalida').value = selectedRow.dataset.fechasalida;
        document.getElementById('editarHoraSalida').value = selectedRow.dataset.horasalida;
        document.getElementById('editarHoraLlegada').value = selectedRow.dataset.horallegada;
        editar.showModal();
    });
}
if (cancelarEditar) {
    cancelarEditar.addEventListener('click', () => editar.close());
}

// aceptarEditar.addEventListener('click', e => {
//     editar.close( );
//     let toast = document.createElement('div');
//     toast.classList.add('toast');
//     toast.innerHTML = 'Operacion Exitosa';
//     toastBox.appendChild(toast);
    
// })

cancelarEditar.addEventListener('click', e => {
    editar.close( );
})

/* ================= BOTON Y DIALOGO ELIMINAR ================= */
const eliminar = document.getElementById('eliminar');
const abrirEliminar = document.getElementById('abrirEliminar');
const aceptarEliminar = document.getElementById('aceptarEliminar');
const cancelarEliminar= document.getElementById('cancelarEliminar');

cancelarEliminar.addEventListener('click', e => {
    eliminar.close()
})

document.querySelectorAll('.corrida-row').forEach(row => {
    row.addEventListener('click', () => {
        document.querySelectorAll('.corrida-row').forEach(r => r.classList.remove('selected'));
        row.classList.add('selected');
        selectedRow = row;
    });
});

if (abrirEliminar) {
    abrirEliminar.addEventListener('click', () => {
        if (!selectedRow) {
            // Usamos un Toast de error en lugar de alert
            createToast("error", "fa-solid fa-circle-exclamation", "Atención", "Por favor, seleccione una corrida de la tabla para eliminar.");
            return;
        }
        document.getElementById('estado_corrida_numero').value = selectedRow.dataset.numero
        document.getElementById('estado_actual').value = selectedRow.dataset.estado;
        eliminar.showModal();
    });
}
if (cancelarEliminar) {
    cancelarEliminar.addEventListener('click', () => editar.close());
}

/* ================= BOTON Y DIALOGO VER POR FECHA Y CIUDAD ================= */
const fechaCiudad = document.getElementById('fechaCiudad');
const abrirFechaCiudad = document.getElementById('abrirFechaCiudad');
const cerrarFechaCiudad = document.getElementById('cerrarFechaCiudad');
const formFechaCiudad = document.getElementById('form-fecha-ciudad')

abrirFechaCiudad.addEventListener('click', e => {
    limpiarFormFechaCiudad();
    fechaCiudad.showModal();
})

function limpiarFormFechaCiudad () {
    const fechaInput = formFechaCiudad.querySelector('input[name="filtro_fecha"]');
    if (fechaInput) {
        fechaInput.value = '';
    }

    const selectCiudad = formFechaCiudad.querySelector('select[name="filtro_ciudad"]')
    if (selectCiudad) {
        selectCiudad.selectedIndex = '0';
    }
}

cerrarFechaCiudad.addEventListener('click', e => {
    limpiarFormFechaCiudad();
    fechaCiudad.close();
    window.location.href = window.location.pathname;
})

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const filtroCiudad = urlParams.get('filtro_ciudad');
    const filtroFecha = urlParams.get('filtro_fecha');
    
    if (filtroCiudad || filtroFecha) {
        if (fechaCiudad) {
            console.log('Abriendo diálogo...');
            fechaCiudad.showModal();
        }
    }
});

/* ================= BOTON Y DIALOGO VER BOLETOS VENDIDOS POR DIA ================= */
const boletos = document.getElementById('boletos');
const abrirBoletos = document.getElementById('abrirBoletos');
const cerrarBoletos = document.getElementById('cerrarBoletos');
const formBoletos = document.getElementById('form-boletos')

function limpiarFormBoletos() {
    fechaBoletos = formBoletos.querySelector('input[name=fecha_boletos]')

    if (fechaBoletos) {
        fechaBoletos.value = "";
    }
}

abrirBoletos.addEventListener('click', e => {
    limpiarFormBoletos();
    boletos.showModal();
})

cerrarBoletos.addEventListener('click', e => {
    limpiarFormBoletos();
    boletos.close();
    window.location.href = window.location.pathname;
})


document.addEventListener('DOMContentLoaded', function (){
    const urlParames = new URLSearchParams(window.location.search);
    const fecha = urlParames.get('fecha_boletos');

    if (fecha) {
        if (boletos) {
            boletos.showModal()
        }
    }
    
});

