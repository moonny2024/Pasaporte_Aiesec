// Animaciones y ripple para bottom nav y enlaces (funciona siempre, aunque el script cargue tarde)
(function () {
	const init = () => {
		if (window.__navRippleInit) return;
		window.__navRippleInit = true;

		// Bottom nav items: burbuja posicionada con CSS vars y delay de navegación
		const items = document.querySelectorAll('.mobile-bottom-nav .mobile-nav-item');
		items.forEach((item) => {
			// Crear indicador si no existe
			let indicator = item.querySelector('.tap-indicator');
			if (!indicator) {
				indicator = document.createElement('span');
				indicator.className = 'tap-indicator';
				item.appendChild(indicator);
			}

			const triggerBubble = (evt) => {
				const rect = item.getBoundingClientRect();
				const evtX = (evt.touches && evt.touches[0].clientX) ?? evt.clientX;
				const evtY = (evt.touches && evt.touches[0].clientY) ?? evt.clientY;
				const x = evtX - rect.left;
				const y = evtY - rect.top;
				item.style.setProperty('--ripple-x', `${x}px`);
				item.style.setProperty('--ripple-y', `${y}px`);
				item.classList.add('bubble');
				item.classList.add('tapped');
				setTimeout(() => item.classList.remove('bubble'), 700);
				setTimeout(() => item.classList.remove('tapped'), 250);
			};

			item.addEventListener('touchstart', (e) => { triggerBubble(e); }, { passive: true });
			item.addEventListener('click', (e) => {
				const href = item.getAttribute('href');
				// Prueba: si es # o javascript:void(0), no navegamos; solo animamos
				const shouldNavigate = href && href !== '#' && href !== 'javascript:void(0)';
				if (shouldNavigate) {
					e.preventDefault();
					triggerBubble(e);
					setTimeout(() => { window.location.href = href; }, 180);
				} else {
					e.preventDefault();
					triggerBubble(e);
				}
			});
		});

		// Ripple global: evitar duplicados usando data flag
		const rippleTargets = document.querySelectorAll('a, button, .mobile-nav-item, .nav-item a');
		rippleTargets.forEach((el) => {
			if (el.dataset.rippleBound === '1') return;
			el.dataset.rippleBound = '1';

			if (!el.classList.contains('ripple-container')) {
				el.classList.add('ripple-container');
			}

			const spawnBubble = (event) => {
				const rect = el.getBoundingClientRect();
				const bubble = document.createElement('span');
				bubble.className = 'ripple-bubble';
				const size = Math.max(rect.width, rect.height);
				bubble.style.width = bubble.style.height = `${size}px`;
				const evtX = (event.touches && event.touches[0].clientX) ?? event.clientX;
				const evtY = (event.touches && event.touches[0].clientY) ?? event.clientY;
				const x = evtX - rect.left - size / 2;
				const y = evtY - rect.top - size / 2;
				bubble.style.left = `${x}px`;
				bubble.style.top = `${y}px`;
				el.appendChild(bubble);
				bubble.addEventListener('animationend', () => bubble.remove());
			};

			el.addEventListener('click', spawnBubble);
			el.addEventListener('touchstart', (e) => { spawnBubble(e); }, { passive: true });
		});
	};

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
