document.getElementById('id_documento').addEventListener('blur', function() {
    const documento = this.value;
    const nombreField = document.getElementById('id_nombre');
    if (documento) {
        fetch(`/credito/get-nombre/?documento=${documento}`)
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