document.addEventListener('DOMContentLoaded', () => {
    const filtroFecha = document.getElementById('filtro-fecha');
    const filtroNumero = document.getElementById('filtro-numero');
    const filtroPasajero = document.getElementById('filtro-pasajero');
    const btnMostrarBoleto = document.getElementById('mostrarBoleto');
    const tabla = document.getElementById('tabla-reservaciones'); // Asegúrate que el <table> tenga este ID
    
    let reservacionSeleccionadaId = null;

    // --- 1. SELECCIÓN DE FILA ---
    if (tabla) {
        tabla.addEventListener('click', (e) => {
            // Buscamos la fila (TR) más cercana al clic
            const fila = e.target.closest('.fila-reserva');
            
            if (fila) {
                // Quitar clase de selección a todas las demás
                document.querySelectorAll('.fila-reserva').forEach(f => f.classList.remove('selected-row'));
                
                // Seleccionar la actual
                fila.classList.add('selected-row');
                reservacionSeleccionadaId = fila.getAttribute('data-id');
                console.log("Seleccionado ID:", reservacionSeleccionadaId);
            }
        });
    }

    // --- 2. ACCIÓN DEL BOTÓN ---
    if (btnMostrarBoleto) {
        btnMostrarBoleto.addEventListener('click', () => {
            if (reservacionSeleccionadaId) {
                // USAMOS LA RUTA RELATIVA PARA EVITAR ERRORES DE PREFIJOS
                // Esto redirigirá a http://localhost:8000/transportes-cuervo-negro/ver-boletos/ID/
                window.location.href = `../ver-boletos/${reservacionSeleccionadaId}/`;
            } else {
                alert('Por favor, selecciona una reservación de la tabla primero.');
            }
        });
    }

    // --- 3. LÓGICA DE FILTRADO (Tu código original mejorado) ---
    const aplicarFiltros = () => {
        const params = new URLSearchParams(window.location.search);
        if (filtroFecha.value) params.set('fecha', filtroFecha.value); else params.delete('fecha');
        if (filtroNumero.value) params.set('numero', filtroNumero.value); else params.delete('numero');
        if (filtroPasajero.value) params.set('pasajero', filtroPasajero.value); else params.delete('pasajero');
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    };

    // Listeners para filtros
    if (filtroFecha) filtroFecha.addEventListener('change', aplicarFiltros);
    [filtroNumero, filtroPasajero].forEach(input => {
        input?.addEventListener('keydown', (e) => { if (e.key === 'Enter') aplicarFiltros(); });
    });

    // Persistencia
    const urlParams = new URLSearchParams(window.location.search);
    if (filtroFecha) filtroFecha.value = urlParams.get('fecha') || '';
    if (filtroNumero) filtroNumero.value = urlParams.get('numero') || '';
    if (filtroPasajero) filtroPasajero.value = urlParams.get('pasajero') || '';
});