// Frontend-only rendering of "Miembros del mes por área"
// Edita este arreglo para actualizar la lista sin backend
const membersByArea = [
  // Ejemplos (edítalos o déjalos vacíos)
  { area: 'Marketing', fullname: 'Ana Pérez', attendances: 5, image: '/static/img/users/profile3.png' },
  { area: 'Finanzas', fullname: 'Luis Gómez', attendances: 4, image: '/static/img/users/profile3.png' },
  { area: 'Talento', fullname: 'María López', attendances: 6, image: '/static/img/users/profile3.png' },
  { area: 'Ventas', fullname: 'Carlos Ruiz', attendances: 3, image: '/static/img/users/profile3.png' }
];

function renderMembersByArea(list) {
  const grid = document.getElementById('members-grid');
  const emptyMsg = document.getElementById('members-empty');
  if (!grid || !emptyMsg) return;

  grid.innerHTML = '';
  if (!Array.isArray(list) || list.length === 0) {
    emptyMsg.style.display = 'block';
    return;
  }
  emptyMsg.style.display = 'none';

  list
    .slice() // copia
    .sort((a, b) => (a.area || '').localeCompare(b.area || ''))
    .forEach(m => {
      const card = document.createElement('div');
      card.className = 'member-card';

      const avatar = document.createElement('div');
      avatar.className = 'member-avatar';
      const img = document.createElement('img');
      img.alt = m.fullname || 'Miembro';
      img.src = m.image && m.image.trim() !== '' ? m.image : '/static/img/users/profile3.png';
      avatar.appendChild(img);

      const info = document.createElement('div');
      info.className = 'member-info';

      const area = document.createElement('div');
      area.className = 'member-area';
      area.textContent = m.area || 'Área';

      const name = document.createElement('div');
      name.className = 'member-name';
      name.textContent = m.fullname || 'Nombre';

      const attendance = document.createElement('div');
      attendance.className = 'member-attendance';
      const icon = document.createElement('i');
      icon.className = 'fas fa-user-check';
      attendance.appendChild(icon);
      const span = document.createElement('span');
      span.textContent = ` ${Number(m.attendances || 0)} asistencias este mes`;
      attendance.appendChild(span);

      info.appendChild(area);
      info.appendChild(name);
      info.appendChild(attendance);

      card.appendChild(avatar);
      card.appendChild(info);

      grid.appendChild(card);
    });
}

// Init
window.addEventListener('DOMContentLoaded', () => {
  try {
    renderMembersByArea(membersByArea);
  } catch (e) {
    console.error('No se pudo renderizar miembros del mes:', e);
  }
});
