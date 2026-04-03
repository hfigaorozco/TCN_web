// ── SELECCION DE ASIENTOS (Plus y Platino) ──

document.addEventListener('DOMContentLoaded', () => {

    const totalPasajeros  = window.__totalPasajeros;
    const estadoAsientos  = window.__estadoAsientos; // { numero: 'DISPONIBLE'|'OCUPADO' }
    const dialogo         = document.getElementById('dialogo-pasajero');
    const formPasajero    = document.getElementById('form-pasajero');
    const contador        = document.getElementById('contador-asientos');
    const pasajeroActual  = document.getElementById('pasajero-actual');
    const asientoActual   = document.getElementById('asiento-actual');
    const btnTexto        = document.getElementById('btn-texto-continuar');

    let seleccionados     = [];  // [{ asiento, nombre, apellidos, edad, tipo_pasajero }]
    let asientoEnCurso    = null;

    // ── Aplicar estado inicial a los botones ──────────────────────────────────
    document.querySelectorAll('.asiento').forEach(btn => {
        const num    = parseInt(btn.dataset.asiento);
        const estado = estadoAsientos[num];

        if (estado === 'OCUPADO' || estado === 'RESERVADO') {
            btn.classList.add('ocupado');
            btn.disabled = true;
        } else {
            btn.classList.add('disponible');
        }
    });

    // ── Clic en asiento ───────────────────────────────────────────────────────
    document.querySelectorAll('.asiento').forEach(btn => {
        btn.addEventListener('click', () => {
            if (btn.disabled) return;

            const num = parseInt(btn.dataset.asiento);

            // Si ya está seleccionado, deseleccionar
            if (btn.classList.contains('seleccionado')) {
                btn.classList.remove('seleccionado');
                btn.classList.add('disponible');
                seleccionados = seleccionados.filter(s => s.asiento !== num);
                actualizarContador();
                return;
            }

            // No permitir más selecciones de las necesarias
            if (seleccionados.length >= totalPasajeros) {
                alert(`Solo puedes seleccionar ${totalPasajeros} asiento(s).`);
                return;
            }

            // Marcar como seleccionado y abrir diálogo
            btn.classList.remove('disponible');
            btn.classList.add('seleccionado');
            asientoEnCurso = num;

            const turno = seleccionados.length + 1;
            pasajeroActual.textContent = turno;
            asientoActual.textContent  = num;
            btnTexto.textContent       = turno < totalPasajeros ? 'Siguiente pasajero' : 'Continuar';

            // Limpiar form
            formPasajero.reset();
            dialogo.showModal();
        });
    });

    // ── Submit del diálogo ────────────────────────────────────────────────────
    formPasajero.addEventListener('submit', (e) => {
        e.preventDefault();

        const nombre    = document.getElementById('nombrePasajero').value.trim();
        const apellidos = document.getElementById('apellidosPasajero').value.trim();
        const edad      = document.getElementById('edadPasajero').value.trim();
        const tipo      = document.getElementById('tipoPasajero').value;

        if (!nombre || !apellidos || !edad || !tipo) {
            alert('Por favor completa todos los campos.');
            return;
        }

        seleccionados.push({
            asiento:       asientoEnCurso,
            nombre:        nombre,
            apellidos:     apellidos,
            edad:          parseInt(edad),
            tipo_pasajero: tipo,
        });

        actualizarContador();
        dialogo.close();

        // Si ya se registraron todos los pasajeros, enviar al resumen
        if (seleccionados.length === totalPasajeros) {
            document.getElementById('input-pasajeros-data').value = JSON.stringify(seleccionados);
            document.getElementById('form-confirmacion').submit();
        }
    });

    function actualizarContador() {
        contador.textContent = `${seleccionados.length} / ${totalPasajeros}`;
    }

});