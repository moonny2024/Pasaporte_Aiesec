// Seleccionamos todos los elementos de la lista (li) que tienen la clase 'list-item'
const list = document.querySelectorAll('.list-item');

// Función para activar el link
function activeLink() {
    // 1. Recorremos todos los elementos y removemos la clase 'active'
    list.forEach((item) =>
        item.classList.remove('active')
    );
    
    // 2. Añadimos la clase 'active' SOLAMENTE al elemento clickeado (this)
    this.classList.add('active');
    
    // Opcional: Cambiar icono de outline a filled
    // (Esto requiere lógica extra si los nombres de iconos no siguen patrón estándar)
    updateIcons();
}

// Función auxiliar para gestionar el estilo de los iconos (relleno vs contorno)
function updateIcons() {
    list.forEach((item) => {
        const icon = item.querySelector('ion-icon');
        const iconName = icon.getAttribute('name');
        
        // Si es el activo y es outline, quita el outline
        if (item.classList.contains('active')) {
             if(iconName.includes('-outline')) {
                 icon.setAttribute('name', iconName.replace('-outline', ''));
             }
             // Caso especial para el icono 'location' que no tiene outline en el nombre original
             if(iconName === 'location-outline') icon.setAttribute('name', 'location');
        } else {
            // Si no es activo y no tiene outline, pónselo
            if(!iconName.includes('-outline') && iconName !== 'location') { // location suele ser base
                 icon.setAttribute('name', iconName + '-outline');
            }
        }
    });
}

// Añadimos el "escuchador" de eventos 'click' a cada elemento
list.forEach((item) => {
    item.addEventListener('click', (e) => {
        // transición suave antes de navegar
        const link = item.querySelector('a');
        const href = link && link.getAttribute('href');
        e.preventDefault();
        activeLink.call(item);
        document.body.classList.remove('fade-enter-active');
        document.body.classList.add('fade-leave');
        document.body.classList.add('fade-leave-active');
        setTimeout(() => {
            if (href && href !== '#' && href !== 'javascript:void(0)') {
                window.location.href = href;
            } else {
                // si es demo, revertimos la clase tras la salida
                document.body.classList.remove('fade-leave');
                document.body.classList.remove('fade-leave-active');
            }
        }, 180);
    });
});

// Al cargar, aplicar fade-in
document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('fade-enter');
    requestAnimationFrame(() => {
        document.body.classList.add('fade-enter-active');
        // limpiar clases de entrada tras completar
        setTimeout(() => {
            document.body.classList.remove('fade-enter');
            // mantenemos fade-enter-active para estado normal
        }, 320);
    });
});