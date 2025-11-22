document.addEventListener('DOMContentLoaded', () => {
    // 1. Selecciona el botón por su ID
    const continueBtn = document.getElementById('continueBtn');

    // 2. Agrega un 'event listener' para detectar el clic
    continueBtn.addEventListener('click', () => {
        // El formulario ahora envía al servidor y el servidor redirige.
        // No mostramos alerta para no interrumpir la navegación.
    });
});