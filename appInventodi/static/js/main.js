// -------------------------------------TIENDA-------------------------------------------------------
let productosTabla = {};  // Objeto para guardar productos y sus cantidades en la tabla

function buscarProducto() {
    const productoId = document.getElementById('buscar').value;
    
    fetch(`obtener-producto/?buscar=${productoId}`)
        .then(response => response.json())
        .then(data => {
            agregarProductoATabla(data);
            actualizarTotalPagar();
        })
        .catch(error => console.error('Error:', error));
}

function agregarProductoATabla(producto) {
    // Verificar si el producto ya está en la tabla
    if (productosTabla[producto.id]) {
        // Incrementar cantidad si el producto ya está
        productosTabla[producto.id].cantidad++;
    } else {
        // Agregar el producto a la tabla si es nuevo
        productosTabla[producto.id] = {
            ...producto,
            cantidad: 1,
        };
    }
    
    actualizarTabla();
}

function actualizarTabla() {
    const tbody = document.querySelector('table tbody');
    tbody.innerHTML = '';  // Limpiar la tabla

    // Recorrer productosTabla y renderizar cada producto
    for (const id in productosTabla) {
        const producto = productosTabla[id];
        const total = producto.precio * producto.cantidad;

        tbody.innerHTML += `
            <tr>
                <td class="text-center">${producto.id}</td>
                <td><img src="${producto.imagen_url}" width="50"></td>
                <td>${producto.nombre}</td>
                <td>${producto.contenido}</td>
                <td class="text-center">${producto.stock}</td>
                <td class="text-center">${producto.cantidad}</td>
                <td class="text-center">${producto.precio}</td>
                <td class="text-center total-display">${total}</td>
            </tr>
        `;
    }
}

function actualizarTotalPagar() {
    let totalPagar = 0;

    for (const id in productosTabla) {
        const producto = productosTabla[id];
        totalPagar += producto.precio * producto.cantidad;
    }

    document.getElementById('total-pagar').innerText = `$ ${totalPagar}`;
}

// ---------------------------------------------------------------------------------
document.getElementById('vender').addEventListener('click', () => {
    fetch('/tienda/vender-productos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(productosTabla)
    })
    .then(response => {
        if (response.ok) {
            // Limpiar la tabla y los productos después de la venta
            productosTabla = {};
            actualizarTabla();
            actualizarTotalPagar();
            alert('Venta realizada con éxito');
        } else {
            alert('Error en la venta');
        }
    })
    .catch(error => console.error('Error:', error));
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