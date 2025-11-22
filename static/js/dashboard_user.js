document.addEventListener('DOMContentLoaded', () => {
    // 1. Obtener referencias a los elementos
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.getElementById('sidebarMenu');
    
    // Si los elementos existen, agregar el listener
    if (menuToggle && sidebar) {
        // 2. Agregar un listener al botón del menú hamburguesa
        menuToggle.addEventListener('click', () => {
            // 3. Alternar la clase 'expanded' en el sidebar
            // Esta clase tiene el CSS que hace que el menú aparezca (left: 0)
            sidebar.classList.toggle('expanded');
            
            // Opcional: Cambiar el ícono de la hamburguesa a una 'X' al expandir
            const icon = menuToggle.querySelector('i');
            if (sidebar.classList.contains('expanded')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times'); // fa-times es el ícono de la X
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        // 4. También permitir que al hacer click en el header se muestre/oculte
        // el sidebar, pero sin activar la navegación si el click fue sobre
        // un enlace o el botón hamburguesa.
        const headerContent = document.querySelector('.header-content');
        if (headerContent) {
            headerContent.addEventListener('click', (ev) => {
                // Si el click fue sobre un enlace (<a>) o sobre el botón de menú, ignorar
                if (ev.target.closest('a') || ev.target.closest('.menu-toggle')) return;

                // Alternar el sidebar igual que el botón
                sidebar.classList.toggle('expanded');
                const icon = menuToggle.querySelector('i');
                if (sidebar.classList.contains('expanded')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            });
        }

        // Opcional: Cerrar el menú si se hace clic en un elemento de navegación (para UX móvil)
        const navLinks = document.querySelectorAll('.nav-list a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('expanded');
                    menuToggle.querySelector('i').classList.remove('fa-times');
                    menuToggle.querySelector('i').classList.add('fa-bars');
                }
            });
        });
    }

    // Navegación directa ahora (sin fetch dinámico)
});