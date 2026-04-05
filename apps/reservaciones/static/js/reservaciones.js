document.addEventListener('DOMContentLoaded', () => {
    const filtroFecha = document.getElementById('filtro-fecha');
    const filtroNumero = document.getElementById('filtro-numero');
    const filtroPasajero = document.getElementById('filtro-pasajero');
    const btnMostrarBoleto = document.getElementById('mostrarBoleto');
    const tabla = document.getElementById('tabla-reservaciones');
    
    let reservacionSeleccionadaId = null;

    if (tabla) {
        tabla.addEventListener('click', (e) => {
            const fila = e.target.closest('.fila-reserva');
            
            if (fila) {
                document.querySelectorAll('.fila-reserva').forEach(f => f.classList.remove('selected-row'));
                fila.classList.add('selected-row');
                reservacionSeleccionadaId = fila.getAttribute('data-id');
                console.log("Seleccionado ID:", reservacionSeleccionadaId);
            }
        });
    }

    if (btnMostrarBoleto) {
        btnMostrarBoleto.addEventListener('click', () => {
            if (reservacionSeleccionadaId) {
                window.location.href = `../ver-boletos/${reservacionSeleccionadaId}/`;
            } else {
                alert('Por favor, selecciona una reservación de la tabla primero.');
            }
        });
    }

    const aplicarFiltros = () => {
        const params = new URLSearchParams(window.location.search);
        if (filtroFecha.value) params.set('fecha', filtroFecha.value); else params.delete('fecha');
        if (filtroNumero.value) params.set('numero', filtroNumero.value); else params.delete('numero');
        if (filtroPasajero.value) params.set('pasajero', filtroPasajero.value); else params.delete('pasajero');
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    };

    if (filtroFecha) filtroFecha.addEventListener('change', aplicarFiltros);
    [filtroNumero, filtroPasajero].forEach(input => {
        input?.addEventListener('keydown', (e) => { if (e.key === 'Enter') aplicarFiltros(); });
    });

    const urlParams = new URLSearchParams(window.location.search);
    if (filtroFecha) filtroFecha.value = urlParams.get('fecha') || '';
    if (filtroNumero) filtroNumero.value = urlParams.get('numero') || '';
    if (filtroPasajero) filtroPasajero.value = urlParams.get('pasajero') || '';
});