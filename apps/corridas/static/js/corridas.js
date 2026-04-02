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

/* ================= FUNCION PARA CREAR TOAST ================= */
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

/* ================= FUNCION PARA CREAR TOAST DE EXITO Y CERRAR DIALOG ================= */
aceptarAgregar.onclick =  function(){
    agregar.close()
    let type = 'exito';
    let icon = "fa-solid fa-check";
    let title = 'Operación exitosa';
    let text = 'El registro ha sido exitoso';
    createToast(type, icon, title, text);
}

/* ================= FUNCION PARA CREAR TOAST DE ERROR Y CERRAR DIALOG ================= */
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




console.log('Fecha:', selectedRow.dataset.fechaSalida);
console.log('Hora salida:', selectedRow.dataset.horaSalida);
console.log('Hora llegada:', selectedRow.dataset.horaLlegada);