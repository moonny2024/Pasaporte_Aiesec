document.addEventListener('DOMContentLoaded', () => {
    // 1. Selecciona el botón por su ID
    const continueBtn = document.getElementById('continueBtn');

    // 2. Agrega un 'event listener' para detectar el clic
    continueBtn.addEventListener('click', () => {
        // Muestra una alerta simple. En un caso real, esto te llevaría a otra página.
        alert('¡Continuar presionado! Iniciando tu viaje con AIESEC...');

        // EJEMPLO REAL: Redireccionar a la siguiente página
        // window.location.href = 'dashboard.html'; 
    });
});