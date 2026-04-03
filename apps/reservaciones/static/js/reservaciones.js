document.addEventListener('DOMContentLoaded', () => {
    const filtroFecha = document.getElementById('filtro-fecha');
    const filtroNumero = document.getElementById('filtro-numero');
    const filtroPasajero = document.getElementById('filtro-pasajero');

    // --- CONFIGURACIÓN DE FECHA MÍNIMA (HOY) ---
    const establecerFechaMinima = () => {
        const hoy = new Date();
        const anio = hoy.getFullYear();
        // Los meses en JS empiezan en 0, por eso sumamos 1
        const mes = String(hoy.getMonth() + 1).padStart(2, '0');
        const dia = String(hoy.getDate()).padStart(2, '0');
        
        const fechaHoyFormateada = `${anio}-${mes}-${dia}`;
        
        // Establece el atributo min para bloquear visualmente días pasados
        filtroFecha.setAttribute('min', fechaHoyFormateada);
    };

    // --- LÓGICA DE FILTRADO ---
    const aplicarFiltros = () => {
        const params = new URLSearchParams(window.location.search);

        // Procesar Fecha
        if (filtroFecha.value) {
            params.set('fecha', filtroFecha.value);
        } else {
            params.delete('fecha');
        }

        // Procesar Número de Corrida
        if (filtroNumero.value) {
            params.set('numero', filtroNumero.value);
        } else {
            params.delete('numero');
        }

        // Procesar Nombre de Pasajero
        if (filtroPasajero.value) {
            params.set('pasajero', filtroPasajero.value);
        } else {
            params.delete('pasajero');
        }

        // Redirigir a la URL construida
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    };

    // --- EVENT LISTENERS ---
    
    // Ejecutar restricción de fecha al cargar
    establecerFechaMinima();

    // Cambio automático al seleccionar una fecha
    filtroFecha.addEventListener('change', aplicarFiltros);
    
    // Filtros de texto/número: se activan al presionar Enter
    // Se usa 'keydown' por ser el estándar actual recomendado
    filtroNumero.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') aplicarFiltros();
    });

    filtroPasajero.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') aplicarFiltros();
    });

    // --- PERSISTENCIA DE DATOS ---
    // Mantiene los valores en los inputs después de que la página se recarga
    const urlParams = new URLSearchParams(window.location.search);
    filtroFecha.value = urlParams.get('fecha') || '';
    filtroNumero.value = urlParams.get('numero') || '';
    filtroPasajero.value = urlParams.get('pasajero') || '';
});