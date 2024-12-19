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

    document.getElementById('total-pagar').innerText = `$ ${totalPagar.toLocaleString('es-ES')}`;
}

// -----------------------Modal y Confirmar Venta-----------------------------------------------
document.getElementById('vender').addEventListener('click', () => {
    // Mostrar el modal de confirmación
    const modal = new bootstrap.Modal(document.getElementById('confirmarVentaModal'));
    modal.show();

    // Escuchar el clic en "Confirmar" una única vez
    const confirmarVentaButton = document.getElementById('confirmarVenta');
    confirmarVentaButton.removeEventListener('click', confirmarVentaHandler); // Evitar duplicación
    confirmarVentaButton.addEventListener('click', confirmarVentaHandler);

    function confirmarVentaHandler() {
        // Preparar datos para enviar al backend
        const ventaData = Object.keys(productosTabla).map(id => ({
            producto_id: id,
            cantidad: productosTabla[id].cantidad,
            precio_unitario: productosTabla[id].precio
        }));

        const ventaPromise = fetch('/tienda/vender-productos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify(productosTabla)
        });

        const registroPromise = fetch('/registro/registrar-venta/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify(ventaData)
        });

        // Realizar las solicitudes
        Promise.all([ventaPromise, registroPromise])
            .then(async ([ventaResponse, registroResponse]) => {
                // Validar las respuestas
                const ventaResultado = ventaResponse.ok ? await ventaResponse.json() : null;
                const registroResultado = registroResponse.ok ? await registroResponse.json() : null;

                if (ventaResponse.ok && registroResponse.ok) {
                    // Limpiar la tabla y los productos después de la venta
                    productosTabla = {};
                    actualizarTabla();
                    actualizarTotalPagar();

                    // Mostrar mensaje de éxito
                    alert('Venta realizada con éxito.');
                } 
                // else {
                //     const ventaError = ventaResultado?.error || 'Error en la venta';
                //     const registroError = registroResultado?.error || 'Error en el registro de la venta';
                //     alert(`Errores:\n- ${ventaError}\n- ${registroError}`);
                // }
            })
            .catch(error => {
                console.error('Error inesperado:', error);
                alert('Ocurrió un error inesperado durante la venta.');
            })
            .finally(() => {
                // Cerrar el modal después de completar las operaciones
                modal.hide();
            });
    }
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


