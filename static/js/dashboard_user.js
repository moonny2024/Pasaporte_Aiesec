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
});