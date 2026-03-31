document.addEventListener("DOMContentLoaded", () => {

    const dialogo = document.getElementById("dialogo-pasajero");

    const asientos = document.querySelectorAll(".asiento.disponible");

    asientos.forEach(asiento => {

        asiento.addEventListener("click", () => {

            const numeroAsiento = asiento.dataset.asiento;
            dialogo.showModal();

        });

    });

});