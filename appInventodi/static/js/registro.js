// const ventasPorDia = JSON.parse('{{ ventas_por_dia|escapejs }}');
//     console.log(ventasPorDia); // Ahora puedes usarlo en tu código JavaScript

//     const labels = ventasPorDia.map(v => v.day);
//     const data = ventasPorDia.map(v => v.total);

//     const ctx = document.getElementById('ventasGrafico').getContext('2d');
//     new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: labels,
//             datasets: [{
//                 label: 'Ventas por día',
//                 data: data,
//                 backgroundColor: 'rgba(75, 192, 192, 0.2)',
//                 borderColor: 'rgba(75, 192, 192, 1)',
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 y: {
//                     beginAtZero: true
//                 }
//             }
//         }
//     });

document.getElementById('vender').addEventListener('click', () => {
    // Mostrar el modal de confirmación
    const modal = new bootstrap.Modal(document.getElementById('confirmarVentaModal'));
    modal.show();

    // Manejar el clic en "Confirmar" en el modal
    document.getElementById('confirmarVenta').addEventListener('click', () => {
        // Preparar datos para enviar al backend
        const ventaData = Object.keys(productosTabla).map(id => ({
            producto_id: id,
            cantidad: productosTabla[id].cantidad,
            precio_unitario: productosTabla[id].precio
        }));

        // Realizar la venta
        Promise.all([
            // Venta de productos
            fetch('/tienda/vender-productos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify(productosTabla)
            }),
            // Registro de ventas
            fetch('/registro/registrar-venta/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify(ventaData)
            })
        ])
        .then(([ventaResponse, registroResponse]) => {
            if (ventaResponse.ok && registroResponse.ok) {
                // Limpiar la tabla y los productos después de la venta
                productosTabla = {};
                actualizarTabla();
                actualizarTotalPagar();
                // Mostrar mensaje de éxito
                alert('Venta realizada con éxito');
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