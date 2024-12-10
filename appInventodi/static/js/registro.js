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