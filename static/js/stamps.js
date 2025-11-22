document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Manejar el clic en los sellos pendientes
    const pendingStamps = document.querySelectorAll('.stamp-pending');
    
    pendingStamps.forEach(stamp => {
        stamp.addEventListener('click', () => {
            const stampTitle = stamp.querySelector('.stamp-title').textContent;
            
            const confirmed = confirm(`¿Deseas completar el sello "${stampTitle}"?`);

            if (confirmed) {
                simulateStampCompletion(stamp, stampTitle);
            }
        });
    });

    /**
     * Transforma un sello pendiente en uno completado.
     */
    function simulateStampCompletion(pendingStampElement, title) {
        // Datos simulados para el sello recién completado
        const colors = ['stamp-local', 'stamp-weekly', 'stamp-active', 'stamp-voice'];
        const colorClass = colors[Math.floor(Math.random() * colors.length)];
        const iconClasses = {
            'stamp-local': 'fa-puzzle-piece',
            'stamp-weekly': 'fa-calendar-check',
            'stamp-active': 'fa-chart-line',
            'stamp-voice': 'fa-headset'
        };
        const iconClass = iconClasses[colorClass] || 'fa-star';
        const smallLabel = 'EXTRA';
        const currentMonth = 'NOV';

        // 1. Actualizar el HTML del sello
        pendingStampElement.classList.remove('stamp-pending');
        pendingStampElement.classList.add('stamp-completed');
        
        const wrapper = pendingStampElement.querySelector('.stamp-icon-wrapper');
        
        // Limpiar contenido y agregar nuevos estilos e íconos
        wrapper.innerHTML = `
            <i class="fas ${iconClass} stamp-main-icon"></i>
            <span class="stamp-label-small">${smallLabel}</span>
            <span class="stamp-tag tag-red">${currentMonth}</span>
        `;
        wrapper.classList.remove('stamp-placeholder');
        wrapper.classList.add(colorClass);

        // Actualizar la sección de detalles
        const details = pendingStampElement.querySelector('.stamp-details');
        details.innerHTML = `
            <p class="stamp-title">${title}</p>
            <div class="stamp-status status-green">
                <i class="fas fa-check"></i> ${currentMonth}
            </div>
        `;
        
        alert(`¡Sello "${title}" completado y añadido a tu Pasaporte!`);
    }


    // 2. Manejar el clic en el botón de "Crear Sello" (lápiz)
    const editIcon = document.querySelector('.edit-icon');

    if (editIcon) {
        editIcon.addEventListener('click', () => {
            const newStampTitle = prompt("Ingresa el nombre del nuevo sello que deseas añadir:");
            
            if (newStampTitle && newStampTitle.trim() !== "") {
                addNewPendingStamp(newStampTitle.trim());
            } else if (newStampTitle !== null) {
                alert("Debes ingresar un nombre válido.");
            }
        });
    }

    /**
     * Añade un nuevo elemento de sello pendiente a la cuadrícula.
     */
    function addNewPendingStamp(title) {
        const grid = document.querySelector('.stamps-grid');
        
        const newStampHTML = `
            <div class="stamp-card stamp-pending" data-stamp-type="new-custom">
                <div class="stamp-icon-wrapper stamp-placeholder">
                    <div class="dotted-circle-large">
                        <div class="dotted-circle-medium">
                            <i class="fas fa-plus stamp-plus-icon"></i>
                        </div>
                    </div>
                </div>
                <div class="stamp-details">
                    <p class="stamp-title">${title}</p>
                </div>
            </div>
        `;

        grid.insertAdjacentHTML('beforeend', newStampHTML);
        
        // Volver a añadir el event listener al nuevo elemento
        const newStampElement = grid.lastElementChild;
        newStampElement.addEventListener('click', () => {
            const confirmed = confirm(`¿Deseas completar el sello "${title}"?`);
            if (confirmed) {
                simulateStampCompletion(newStampElement, title);
            }
        });

        alert(`Nuevo sello pendiente "${title}" añadido.`);
    }
});