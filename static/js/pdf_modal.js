document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pdfForm');
    const modal = new bootstrap.Modal(document.getElementById('pdfModal'));
    const pdfIframe = document.getElementById('pdfIframe');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Crea FormData con todos los datos del formulario
        const formData = new FormData(form);

        // Muestra un loader o desactiva el botón si quieres
        // ...

        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error('Error generando PDF');
            return response.blob();
        })
        .then(blob => {
            // Crea una URL temporal para el blob PDF
            const url = URL.createObjectURL(blob);
            pdfIframe.src = url;
            modal.show();

            // Cuando se cierra el modal, libera el blob
            document.getElementById('pdfModal').addEventListener('hidden.bs.modal', function () {
                pdfIframe.src = '';
                URL.revokeObjectURL(url);
            }, { once: true });
        })
        .catch(error => {
            alert("No se pudo generar el PDF. Intenta de nuevo.");
        });
    });
});
