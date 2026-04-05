document.addEventListener('DOMContentLoaded', () => {

    const btnUsuario         = document.getElementById('btn-usuario');
    const btnModificarContra = document.getElementById('btn-cambiar-contra');
    const btnVenderBoletos   = document.getElementById('btn-venderBoletos');
    const btnSalir           = document.getElementById('btn-salir');
    const btnContinuar       = document.querySelector('.dialog-buscar-btn');

    const dialogoUsuario  = document.getElementById('dialogo-perfil');
    const dialogoContra   = document.getElementById('dialogo-contrasena');
    const dialogoBusqueda = document.getElementById('dialogo-buscar');

    // Abrir diálogo de perfil
    btnUsuario.addEventListener('click', () => {
        dialogoUsuario.showModal();
    });

    // Abrir diálogo de modificar contraseña
    btnModificarContra.addEventListener('click', () => {
        dialogoUsuario.close();
        dialogoContra.showModal();
    });

    // Abrir diálogo de búsqueda de viaje
    btnVenderBoletos.addEventListener('click', () => {
        dialogoBusqueda.showModal();
    });

    // Botón Continuar — validar y navegar
    btnContinuar.addEventListener('click', () => {
        const selects   = dialogoBusqueda.querySelectorAll('select');
        const fecha     = dialogoBusqueda.querySelector('input[type="date"]');
        const pasajeros = dialogoBusqueda.querySelector('.dialog-buscar-pasajeros');

        const origen   = selects[0].value;
        const destino  = selects[1].value;
        const fechaVal = fecha.value;
        const pasVal   = pasajeros.value;

        if (!origen)  { alert('Selecciona el origen.'); return; }
        if (!destino) { alert('Selecciona el destino.'); return; }
        if (origen === destino) { alert('El origen y el destino no pueden ser iguales.'); return; }
        if (!fechaVal) { alert('Selecciona una fecha.'); return; }
        if (!pasVal || parseInt(pasVal) < 1) { alert('Ingresa el número de pasajeros.'); return; }

        const params = new URLSearchParams({
            origen:    origen,
            destino:   destino,
            fecha:     fechaVal,
            pasajeros: pasVal,
        });

        window.location.href = `${window.__urlBoletos}?${params.toString()}`;
    });

    // --- NUEVO: Manejo de clic en filas de corrida ---
    const corridaRows = document.querySelectorAll('.corrida-row');
    const pasajerosBody = document.getElementById('pasajeros-body');
    const detalleBox = document.getElementById('detalle-corrida-box');
    const filterMes = document.getElementById('filter-mes');

    // Filtrado de meses
    if (filterMes) {
        filterMes.addEventListener('change', () => {
            const selectedMes = filterMes.value; // Formato YYYY-MM o "todos"
            console.log('Filtrando por mes:', selectedMes);
            
            let firstVisible = null;

            corridaRows.forEach(row => {
                const rowFecha = row.getAttribute('data-fecha'); // YYYY-MM-DD
                console.log('Fila fecha:', rowFecha);
                
                let visible = false;
                if (selectedMes === 'todos') {
                    visible = true;
                } else if (rowFecha && rowFecha === selectedMes) {
                    visible = true;
                }

                if (visible) {
                    row.style.display = '';
                    if (!firstVisible) firstVisible = row;
                } else {
                    row.style.display = 'none';
                    row.classList.remove('selected-row');
                }
            });

            // Si hay una primera fila visible, simular click para cargar sus detalles
            if (firstVisible) {
                firstVisible.click();
            } else {
                // Si no hay nada, limpiar detalles y pasajeros
                if (pasajerosBody) pasajerosBody.innerHTML = '<tr><td colspan="4">Sin pasajeros</td></tr>';
                if (detalleBox) detalleBox.innerHTML = '<div class="card-title">Detalles de la Corrida</div><div style="text-align: center; padding: 20px 0"><p style="color: #888; font-style: italic; font-size: 14px">Seleccione una corrida para ver información</p></div>';
            }
        });
    }

    // Resaltar la primera fila por defecto si existe
    if (corridaRows.length > 0) {
        corridaRows[0].classList.add('selected-row');
    }

    corridaRows.forEach(row => {
        row.addEventListener('click', () => {
            const corridaId = row.getAttribute('data-id');
            if (!corridaId) return;

            // Resaltar la fila seleccionada
            corridaRows.forEach(r => r.classList.remove('selected-row'));
            row.classList.add('selected-row');

            fetch(`${window.__urlGetCorridaDetails}${corridaId}/`)
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.json();
                })
                .then(data => {
                    console.log('Datos recibidos:', data); // Debugging
                    updatePasajerosTable(data.pasajeros);
                    updateDetalleCorrida(data.detalle);
                })
                .catch(error => {
                    console.error('Error fetching corrida details:', error);
                    createToast('error', 'fa-solid fa-circle-exclamation', 'Error', 'No se pudieron cargar los detalles');
                });
        });
    });

    function updatePasajerosTable(pasajeros) {
        if (!pasajerosBody) return;
        
        pasajerosBody.innerHTML = ''; // Limpiar tabla actual

        if (!pasajeros || pasajeros.length === 0) {
            pasajerosBody.innerHTML = '<tr><td colspan="4">Sin pasajeros</td></tr>';
            return;
        }

        pasajeros.forEach(p => {
            const row = `
                <tr>
                    <td>${p.asiento}</td>
                    <td>${p.nombre}</td>
                    <td>${p.tipo}</td>
                    <td><span class="status ${p.estado.toLowerCase()}">${p.estado}</span></td>
                </tr>
            `;
            pasajerosBody.insertAdjacentHTML('beforeend', row);
        });
    }

    function updateDetalleCorrida(detalle) {
        if (!detalleBox) return;

        detalleBox.innerHTML = `
            <div class="card-title">Detalles de la Corrida</div>
            <div class="detail-content">
                <div class="detail-info-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 10px;">
                    <p><strong><i class="fa-solid fa-bus"></i> Autobús:</strong> <span>Número ${detalle.autobus} - ${detalle.tipo}</span></p>
                    <p><strong><i class="fa-solid fa-user-tie"></i> Operador:</strong> <span>${detalle.operador}</span></p>
                    <p><strong><i class="fa-solid fa-route"></i> Ruta:</strong> <span>${detalle.ruta}</span></p>
                    <p><strong><i class="fa-solid fa-clock"></i> Hora de salida:</strong> <span>${detalle.salida}</span></p>
                    <p><strong><i class="fa-solid fa-users"></i> Capacidad:</strong> <span>${detalle.ocupados} / ${detalle.capacidad} asientos</span></p>
                </div>
                <div class="progress-container" style="margin-top: 20px">
                    <label style="font-weight: 600; color: #555; font-size: 13px">Ocupación del autobús</label>
                    <div class="progress-bar" style="width: 100%; height: 10px; background: #eee; border-radius: 20px; margin: 8px 0; overflow: hidden;">
                        <div class="progress" style="width: ${detalle.porcentaje}%; height: 100%; background: #2f6fed; transition: 0.5s;"></div>
                    </div>
                    <span class="progress-text" style="font-size: 12px; color: #666">${detalle.porcentaje}% de capacidad completada</span>
                </div>
            </div>
        `;
    }

    // Cerrar sesión
    btnSalir.addEventListener('click', () => {
        dialogoUsuario.close();
        createToast('error', 'fa-solid fa-right-from-bracket', 'Cerrando sesión...', 'Hasta pronto');
        setTimeout(() => {
            window.location.href = window.__urlLogin;
        }, 3000);
    });

});


/* ================= FUNCION PARA CREAR TOAST ================= */
function createToast(type, icon, title, text) {
    const notificaciones = document.querySelector('.notificaciones');
    const newToast = document.createElement('div');
    newToast.innerHTML = `
        <div class="toast ${type}">
            <i class="${icon}"></i>
            <div class="content">
                <div class="title">${title}</div>
                <span>${text}</span>
            </div>
            <i class="fa-solid fa-x" onclick="this.closest('.toast').parentElement.remove()"></i>
        </div>`;
    notificaciones.appendChild(newToast);
    setTimeout(() => { newToast.remove(); }, 3000);
}