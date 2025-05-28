document.addEventListener('DOMContentLoaded', function() {
    // Obtener el nombre del producto desde el h2.product-title
    const productElement = document.querySelector('.product-title');
    if (!productElement) {
        console.error("No se encontró el elemento con clase .product-title");
        return;
    }

    const producto = productElement.textContent.trim();
    console.log(`Cargando precio para: ${producto}`);

    // Cargar el JSON de Amazon desde /data/amazon.json
    fetch('/data/amazon.json')
        .then(response => response.json())
        .then(data => {
            if (data && data[producto] !== undefined && data[producto] !== null) {
                let precioFormateado = data[producto].toLocaleString('es-MX', { style: 'currency', currency: 'MXN' });
                document.querySelector('.product-price').textContent = precioFormateado;
            } else {
                document.querySelector('.product-price').textContent = "No disponible";
            }
        })
        .catch(error => {
            console.error("Error cargando /data/amazon.json:", error);
            document.querySelector('.product-price').textContent = "Error al cargar precio";
        });
});

