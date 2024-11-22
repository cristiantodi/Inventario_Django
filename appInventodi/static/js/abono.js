document.getElementById("crear-btn").addEventListener("click", function() {
    // Mostrar el modal de creacion
    const modalCrearAbono = new bootstrap.Modal(document.getElementById('iinfoModal'));
    console.log("Aqui abono")
    modalCrearAbono.show();
});