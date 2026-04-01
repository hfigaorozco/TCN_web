document.addEventListener('DOMContentLoaded', () => {

    // Abrir diálogo si no hay resultados
    if (window.__sinResultados) {
        document.getElementById('dialogo-sin-resultados').showModal();
    }

});