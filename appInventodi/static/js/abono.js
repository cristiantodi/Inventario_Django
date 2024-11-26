// document.getElementById("crear-btn").addEventListener("click", function() {
//     // Mostrar el modal de creacion
//     const modalCrearAbono = new bootstrap.Modal(document.getElementById('iinfoModal'));
//     console.log("Aqui abono")
//     modalCrearAbono.show();
// });

// document.getElementById('id_documento').addEventListener('input', function() {
//     const documento = this.value;
//     if (documento) {
//         fetch(`/abonos/buscar-nombre/?documento=${documento}`)
//             .then(response => response.json())
//             .then(data => {
//                 if (data.nombre) {
//                     document.getElementById('id_nombre').value = data.nombre;
//                 } else {
//                     console.error(data.error);
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//     }
// });

document.getElementById('id_documento').addEventListener('blur', function() {
    const documento = this.value;
    const nombreField = document.getElementById('id_nombre');
    if (documento) {
        fetch(`/abonos/get-nombre/?documento=${documento}`)
            .then(response => response.json())
            .then(data => {
                if (data.nombre) {
                    nombreField.value = data.nombre;
                } else {
                    nombreField.value = '';
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        nombreField.value = '';
    }
});