// Función para obtener el token CSRF
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

document.addEventListener('DOMContentLoaded', () => {
    const addButtons = document.querySelectorAll('.add-button');
    const subtractButtons = document.querySelectorAll('.subtract-button');
    const sellButton = document.getElementById('sell-button');

    addButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-product-id');
            const cantidadElement = document.getElementById(`cantidad-${productId}`);
            let cantidad = parseInt(cantidadElement.innerText);
            cantidad += 1;
            cantidadElement.innerText = cantidad;

            updateTotal(productId, cantidad, button);
        });
    });

    subtractButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-product-id');
            const cantidadElement = document.getElementById(`cantidad-${productId}`);
            let cantidad = parseInt(cantidadElement.innerText);
            if (cantidad > 0) {
                cantidad -= 1;
                cantidadElement.innerText = cantidad;

                updateTotal(productId, cantidad, button);
            }
        });
    });

    sellButton.addEventListener('click', () => {
        const products = Array.from(document.querySelectorAll('.add-button')).map(button => {
            const productId = button.getAttribute('data-product-id');
            const cantidad = parseInt(document.getElementById(`cantidad-${productId}`).innerText);
            return { id: productId, cantidad: cantidad };
        });
    
        // Enviar la información al servidor para actualizar la base de datos
        fetch('/tienda', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ products: products })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                alert('Venta realizada con éxito');
                location.reload();
            } else {
                alert('Error al vender productos');
            }
        });
    });

    function updateTotal(productId, cantidad, button) {
        const precio = parseFloat(button.getAttribute('data-precio'));
        const totalElement = document.getElementById(`total-${productId}`);
        const total = precio * cantidad;
        totalElement.innerText = total;

        updateTotalPagar();
    }

    function updateTotalPagar() {
        let totalPagar = 0;
        document.querySelectorAll('td[id^="total-"]').forEach(totalElement => {
            totalPagar += parseFloat(totalElement.innerText) || 0;
        });
        document.getElementById('total-pagar').innerText = `$${totalPagar}`;
    }
});

// --------------------------SUMAR / RESTAR----------------------------------------------------
function updateQuantity(button, delta) {
    const quantityDisplay = delta === "increase" ? button.nextElementSibling : button.previousElementSibling;
    let newQuantity = parseInt(quantityDisplay.innerText) + delta;
  
    if (newQuantity >= 0) {
      quantityDisplay.innerText = newQuantity;
      actualizarCantidad(button, newQuantity, delta);
    }
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(event) {
      if (event.target.classList.contains('add-button'))   
   {
        updateQuantity(event.target, "increase");
      } else if (event.target.classList.contains('subtract-button')) {
        updateQuantity(event.target, "decrease");
      }
    });
  });

function actualizarCantidad(button, nuevaCantidad, action) {
    fetch("{% url 'buscar_producto' %}", {
        method: "POST",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ action: action, quantity_change: 1 })
    });
}