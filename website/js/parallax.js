const image = document.querySelector('.parallax-image');

// Función para actualizar el parallax
function updateParallax() {
  if (window.innerWidth >= 768 && image) {
    const scrollOffset = window.scrollY * -0.3;
    image.style.transform = `translateY(${scrollOffset}px)`;
  }
}

// Escuchar scroll con inercia ligera
let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    window.requestAnimationFrame(() => {
      updateParallax();
      ticking = false;
    });
    ticking = true;
  }
});

// ✅ Aplicar desplazamiento inicial en cuanto carga el sitio
window.addEventListener('load', () => {
  updateParallax();
});
