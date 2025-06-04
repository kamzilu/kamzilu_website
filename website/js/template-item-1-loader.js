fetch('/data/consolas.json')
  .then(res => res.json())
  .then(data => {
    const path = window.location.pathname.split('/')[3];
    const product = data[path];

    if (product) {
      document.getElementById('breadcrumb-product').textContent = product.name;
      document.getElementById('product-name').textContent = product.name;
      document.getElementById('product-image-src').src = product.image;
      document.getElementById('product-description').textContent = product.description;

      // --- Ajuste de fecha ---
      const scrapeDate = new Date(product.lastUpdated);
      const now = new Date();

      const diffMs = now - scrapeDate;
      const diffMins = Math.floor(diffMs / (1000 * 60));
      const diffHours = Math.floor(diffMins / 60);
      const diffDays = Math.floor(diffHours / 24);

      let timeAgo = "";
      if (diffDays > 0) {
        timeAgo = `hace ${diffDays} día${diffDays > 1 ? "s" : ""}`;
      } else if (diffHours > 0) {
        timeAgo = `hace ${diffHours} hora${diffHours > 1 ? "s" : ""}`;
      } else if (diffMins > 0) {
        timeAgo = `hace ${diffMins} minuto${diffMins > 1 ? "s" : ""}`;
      } else {
        timeAgo = "hace unos segundos";
      }

      const options = { day: "2-digit", month: "2-digit", year: "2-digit", hour: "numeric", minute: "2-digit" };
      const formattedDate = scrapeDate.toLocaleDateString("es-MX", options);

      document.getElementById('last-updated').textContent = `Actualizado ${timeAgo}: ${formattedDate}`;
      // --- Fin ajuste de fecha ---

      const priceCards = document.getElementById('price-cards');
      product.prices.forEach((price, index) => {
        const card = document.createElement('div');
        const cardClass = index === 0 ? 'price-card lowest-card' : 'price-card';
        const priceClass = index === 0 ? 'price-value lowest-price' : 'price-value';
        card.className = cardClass;
        card.innerHTML = `
          <div class="price-left">
            <img src="${product.image}" alt="${product.name}">
            <p>${product.name}</p>
          </div>
          <a href="${price.link}" target="_blank" class="price-right-link">
            <div class="price-inner-box">
              <img src="${price.logo}" alt="${price.store}">
              <span class="${priceClass}">$${price.price}${index === 0 ? ' ✅' : ''}</span>
              <span class="view-button">Ver ></span>
            </div>
          </a>
        `;
        priceCards.appendChild(card);
      });

    } else {
      document.getElementById('product-name').textContent = 'Producto no encontrado';
    }
  });
