// ── AUTOBUSES.JS ──

document.addEventListener('DOMContentLoaded', () => {

    // Dialogos

    document.getElementById('abrirAgregar').addEventListener('click', () => {
        document.getElementById('dialogo-agregar-bus').showModal();
    });

    document.getElementById('abrirEliminar').addEventListener('click', () => {
        document.getElementById('dialogo-eliminar-bus').showModal();
    });

    document.getElementById('abrirAgregarMarca').addEventListener('click', () => {
        document.getElementById('dialogo-agregar-marca').showModal();
    });

    document.getElementById('abrirAgregarModelo').addEventListener('click', () => {
        document.getElementById('dialogo-agregar-modelo').showModal();
    });

    // Filtros

    const marcaSelect = document.getElementById('bus-marca');
    const modeloSelect = document.getElementById('bus-modelo');
    const todasLasOpciones = Array.from(modeloSelect.options).filter(opt => opt.value !== '');

    marcaSelect.addEventListener('change', function () {
        const marcaSeleccionada = this.value;

        modeloSelect.innerHTML = '<option value="" disabled selected>Seleccionar modelo</option>';

        todasLasOpciones.forEach(option => {
            if (option.dataset.marca === marcaSeleccionada) {
                modeloSelect.appendChild(option.cloneNode(true));
            }
        });
    });

    const inputNumero = document.getElementById('numero_bus');
    const selectTipo = document.getElementById('tipo_servicio');

    function filtrarTabla() {
        const numeroBuscado = inputNumero.value.trim();
        const tipoSeleccionado = selectTipo.value;
        const filas = document.querySelectorAll('.content-box table tbody tr');

        filas.forEach(fila => {
            const celdaNumero = fila.cells[0]?.textContent.trim();
            const tipoFila = fila.dataset.tipo;

            const coincideNumero = numeroBuscado === '' || celdaNumero.includes(numeroBuscado);
            const coincideTipo = tipoSeleccionado === 'todos' || tipoFila === tipoSeleccionado;

            fila.style.display = (coincideNumero && coincideTipo) ? '' : 'none';
        });
    }

    inputNumero.addEventListener('input', filtrarTabla);
    selectTipo.addEventListener('change', filtrarTabla);


    // ================= TOASTS =================

    const notificaciones = document.querySelector('.notificaciones');

    function createToast(type, icon, title, text) {
        let newToast = document.createElement('div');
        newToast.innerHTML = `
            <div class="toast ${type}">
                <i class="${icon}"></i>
                <div class="content">
                    <div class="title">${title}</div>
                    <span>${text}</span>
                </div>
                <i class="fa-solid fa-x" onclick="(this.parentElement).remove()"></i>
            </div>`;
        notificaciones.appendChild(newToast);
        setTimeout(() => { newToast.remove(); }, 3000);
    }

    // ================= MOSTRAR ERROR DEL SERVIDOR =================

    if (window.__errorServidor) {
        document.getElementById('dialogo-agregar-bus').showModal();
        createToast('error', 'fa-solid fa-exclamation', 'Error', window.__errorServidor);
    }

    if (window.__exitoServidor) {
        createToast('exito', 'fa-solid fa-check', 'Operación exitosa', window.__exitoServidor);
    }

});