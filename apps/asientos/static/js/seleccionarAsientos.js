document.addEventListener('DOMContentLoaded', () => {

    const totalPasajeros  = window.__totalPasajeros;
    const estadoAsientos  = window.__estadoAsientos;
    const dialogo         = document.getElementById('dialogo-pasajero');
    const formPasajero    = document.getElementById('form-pasajero');
    // ← se eliminan: contador, pasajeroActual, asientoActual, btnTexto
    const pasajeroActual  = document.getElementById('pasajero-actual');
    const asientoActual   = document.getElementById('asiento-actual');
    const btnTexto        = document.getElementById('btn-texto-continuar');

    let seleccionados  = [];
    let asientoEnCurso = null;

    // ── Calcula tipo de pasajero según edad ───────────────────────────────────
    function calcularTipo(edad) {
        if (edad <= 12)  return 'NINO';
        if (edad >= 60)  return '3DAD';
        return 'REGU';
    }

    // ── Aplicar estado inicial ────────────────────────────────────────────────
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

            if (btn.classList.contains('seleccionado')) {
                btn.classList.remove('seleccionado');
                btn.classList.add('disponible');
                seleccionados = seleccionados.filter(s => s.asiento !== num);
                return;
            }

            if (seleccionados.length >= totalPasajeros) {
                alert(`Solo puedes seleccionar ${totalPasajeros} asiento(s).`);
                return;
            }

            btn.classList.remove('disponible');
            btn.classList.add('seleccionado');
            asientoEnCurso = num;

            const turno = seleccionados.length + 1;
            pasajeroActual.textContent = turno;
            asientoActual.textContent  = num;
            btnTexto.textContent       = turno < totalPasajeros ? 'Siguiente pasajero' : 'Continuar';

            formPasajero.reset();
            dialogo.showModal();
        });
    });

    // ── Submit del diálogo ────────────────────────────────────────────────────
    formPasajero.addEventListener('submit', (e) => {
        e.preventDefault();

        const nombre    = document.getElementById('nombrePasajero').value.trim();
        const apellidos = document.getElementById('apellidosPasajero').value.trim();
        const edad      = parseInt(document.getElementById('edadPasajero').value.trim());

        if (!nombre || !apellidos || !edad) {
            alert('Por favor completa todos los campos.');
            return;
        }

        // ← tipo se calcula automáticamente, ya no viene del select
        const tipo = calcularTipo(edad);

        seleccionados.push({
            asiento:       asientoEnCurso,
            nombre:        nombre,
            apellidos:     apellidos,
            edad:          edad,
            tipo_pasajero: tipo,
        });

        dialogo.close();

        if (seleccionados.length === totalPasajeros) {
            document.getElementById('input-pasajeros-data').value = JSON.stringify(seleccionados);
            document.getElementById('form-confirmacion').submit();
        }
    });

});