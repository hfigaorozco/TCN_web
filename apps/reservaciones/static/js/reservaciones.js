document.addEventListener('DOMContentLoaded', () => {
    const filtroFecha = document.getElementById('filtro-fecha');
    const filtroNumero = document.getElementById('filtro-numero');
    const filtroPasajero = document.getElementById('filtro-pasajero');

    // Función para actualizar la URL con los filtros
    const aplicarFiltros = () => {
        const params = new URLSearchParams(window.location.search);

        if (filtroFecha.value) params.set('fecha', filtroFecha.value);
        else params.delete('fecha');

        if (filtroNumero.value) params.set('numero', filtroNumero.value);
        else params.delete('numero');

        if (filtroPasajero.value) params.set('pasajero', filtroPasajero.value);
        else params.delete('pasajero');

        // Redirigir con los nuevos parámetros
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    };

    // Escuchar el cambio en los inputs (puedes usar 'change' o 'input' con un debounce)
    filtroFecha.addEventListener('change', aplicarFiltros);
    
    // Para los campos de texto/número, es mejor esperar a que el usuario presione Enter
    filtroNumero.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') aplicarFiltros();
    });

    filtroPasajero.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') aplicarFiltros();
    });

    // Mantener los valores en los inputs después de recargar
    const urlParams = new URLSearchParams(window.location.search);
    filtroFecha.value = urlParams.get('fecha') || '';
    filtroNumero.value = urlParams.get('numero') || '';
    filtroPasajero.value = urlParams.get('pasajero') || '';
});