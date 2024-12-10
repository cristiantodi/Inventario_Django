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
        
    // Limpiar el campo de búsqueda después de registrar el producto
    document.getElementById('buscar').value = '';
}

// Escuchar la tecla Enter en el input de búsqueda
document.getElementById('buscar').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevenir el comportamiento predeterminado de recargar la página
        buscarProducto(); // Llamar a la función para buscar el producto
    }
});

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
                <td class="text-center"><img class="img-table" src="${producto.imagen_url}" width="40"></td> 
                <td>${producto.nombre}</td>
                <td>${producto.contenido}</td>
                <td class="text-center">${producto.stock}</td>
                <td class="text-center">${producto.cantidad}</td>
                <td class="text-center">$ ${producto.precio.toLocaleString('es-ES')}</td>
                <td class="text-center total-display">$ ${total.toLocaleString('es-ES')}</td>
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

// -----------------------Modal y Confirmar Venta-----------------------------------------------
document.getElementById('vender').addEventListener('click', () => {
    // Mostrar el modal de confirmación
    const modal = new bootstrap.Modal(document.getElementById('confirmarVentaModal'));
    modal.show();

    // Manejar el clic en "Confirmar" en el modal
    document.getElementById('confirmarVenta').addEventListener('click', () => {
        // Realizar la venta
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
                // alert('Venta realizada con éxito');
            } else {
                alert('Error en la venta');
            }
            // Cerrar el modal después de la venta
            modal.hide();
        })
        .catch(error => {
            console.error('Error:', error);
            // Cerrar el modal si hay un error
            modal.hide();
        });
    });
});
//---------------------------------Eliminar producto de la tabla/tienda----------
document.querySelector('table tbody').addEventListener('contextmenu', function(event) {
    event.preventDefault(); // Prevenir el menú contextual predeterminado

    // Eliminar cualquier cuadro de confirmación anterior
    const existingConfirmationBox = document.querySelector('.custom-confirmation-box');
    if (existingConfirmationBox) {
        existingConfirmationBox.remove();
    }

    // Crear un cuadro de confirmación personalizado
    const confirmationBox = document.createElement('div');
    confirmationBox.classList.add('custom-confirmation-box');

    // Agregar contenido al cuadro de confirmación
    confirmationBox.innerHTML = `
        <p>¿Estás seguro de que deseas eliminar este producto?</p>
        <button id="confirmar">Confirmar</button>
        <button id="cancelar">Cancelar</button>
    `;

    document.body.appendChild(confirmationBox);

    // Manejar el clic en "Confirmar"
    document.getElementById('confirmar').addEventListener('click', function() {
        const row = event.target.closest('tr');
        const productoId = row.querySelector('td').innerText; // El primer <td> contiene el id

        // Eliminar el producto del objeto productosTabla
        delete productosTabla[productoId];

        // Actualizar la tabla y el total a pagar
        actualizarTabla();
        actualizarTotalPagar();

        // alert('Producto eliminado de la tabla');

        // Eliminar el cuadro de confirmación
        confirmationBox.remove();
    });

    // Manejar el clic en "Cancelar"
    document.getElementById('cancelar').addEventListener('click', function() {
        // Eliminar el cuadro de confirmación
        confirmationBox.remove();
    });
});


// -----------------------------------------------Registro----------------------------------
const ventasPorDia = JSON.parse('{{ ventas_por_dia|escapejs }}');
    console.log(ventasPorDia); // Ahora puedes usarlo en tu código JavaScript

    const labels = ventasPorDia.map(v => v.day);
    const data = ventasPorDia.map(v => v.total);

    const ctx = document.getElementById('ventasGrafico').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ventas por día',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });