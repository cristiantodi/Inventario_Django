// -------------------------Inventario
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("guardar-btn").addEventListener("click", function() {
        const filas = document.querySelectorAll("tbody tr");
        let cambios = [];

        filas.forEach(fila => {
            const productoId = fila.getAttribute("data-producto-id");
            // Selecciona el input usando el id dinámico
            const cantidadInput = document.getElementById(`cantidad-${productoId}`);
            const cantidad = parseInt(cantidadInput.value);

            if (cantidad !== 0) {
                cambios.push({ id: productoId, cantidad: cantidad });
            }
        });

        if (cambios.length > 0) {
            fetch("/tienda/actualizar_stock/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ cambios: cambios })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert("Stock actualizado correctamente");
                    location.reload(); // Opcional
                } else {
                    alert("Hubo un error al actualizar el stock: " + (data.error || "Error desconocido"));
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        } else {
            alert("No hay cambios que guardar");
        }
    });
});
