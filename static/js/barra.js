// Seleccionamos todos los elementos de la lista (li) que tienen la clase 'list-item'
const list = document.querySelectorAll('.list-item');

let isNavigating = false;
let navEl = document.querySelector('.navigation');

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
        if (isNavigating) {
            e.preventDefault();
            return; // evitar múltiples navegaciones y animaciones simultáneas
        }
        // Evitar reiniciar animación si ya estamos en el mismo destino
        const link = item.querySelector('a');
        const href = link && link.getAttribute('href');
        const normalize = (p) => {
            if (!p) return '';
            return p.endsWith('/') && p.length > 1 ? p.slice(0, -1) : p;
        };
        const currentPath = normalize(window.location.pathname);
        const url = new URL(href, window.location.href);
        const targetPath = normalize(url.pathname);

        // Si el destino es el mismo, no navegar ni reiniciar animaciones
        if (targetPath === currentPath || href === '#' || href === 'javascript:void(0)') {
            e.preventDefault();
            // Asegurar que el item activo se mantiene sin re-disparar animaciones
            activeLink.call(item);
            return;
        }

        // transición suave antes de navegar
        e.preventDefault();
        isNavigating = true;
        // Desactivar interacción durante la transición para evitar jank
        if (navEl) navEl.style.pointerEvents = 'none';

        // Activar estado visual del item sin forzar reflow excesivo
        requestAnimationFrame(() => {
            activeLink.call(item);
            document.body.classList.add('fade-leave');
            requestAnimationFrame(() => {
                document.body.classList.add('fade-leave-active');
                setTimeout(() => {
                    try { sessionStorage.setItem('skipEnter', '1'); } catch (e) {}
                    window.location.href = href;
                }, 100);
            });
        });
    });
});

// Al cargar, aplicar fade-in
document.addEventListener('DOMContentLoaded', () => {
    // Marcar activo según la URL actual en el primer render
    const normalize = (p) => {
        if (!p) return '';
        return p.endsWith('/') && p.length > 1 ? p.slice(0, -1) : p;
    };
    const currentPath = normalize(window.location.pathname);
    list.forEach((item) => {
        const link = item.querySelector('a');
        if (!link) return;
        const href = link.getAttribute('href');
        if (!href || href === '#' || href === 'javascript:void(0)') return;
        const targetPath = normalize(new URL(href, window.location.href).pathname);
        if (targetPath === currentPath) {
            item.classList.add('active');
        }
    });
    updateIcons();

        // No aplicar animación de entrada al cargar la página para que solo
        // la barra mobile controle las transiciones de salida.
        isNavigating = false;
        if (navEl) navEl.style.pointerEvents = '';
});