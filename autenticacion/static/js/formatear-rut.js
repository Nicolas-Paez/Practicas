document.addEventListener('input', (e) => {
    const rut = document.getElementById('id_rut');
    if (e.target === rut) {
        // Limitar a 12 caracteres (sin contar puntos ni guion)
        let rutLimpio = rut.value.replace(/[^0-9kK]/g, '');
        if (rutLimpio.length > 9) {
            rutLimpio = rutLimpio.slice(0, 9); // Limitar a 9 caracteres
        }

        let rutFormateado = darFormatoRUT(rutLimpio);
        rut.value = rutFormateado;
    }
});

function darFormatoRUT(rut) {
    // Dejar solo números y letras 'k'
    const rutLimpio = rut.replace(/[^0-9kK]/g, '');
    // Aislar el cuerpo del dígito verificador
    const cuerpo = rutLimpio.slice(0, -1);
    const dv = rutLimpio.slice(-1).toUpperCase();

    if (rutLimpio.length < 2) return rutLimpio;
    // Colocar los separadores de miles al cuerpo
    let cuerpoFormatoMiles = cuerpo
        .toString()
        .split('')
        .reverse()
        .join('')
        .replace(/(?=\d*\.?)(\d{3})/g, '$1.');

    cuerpoFormatoMiles = cuerpoFormatoMiles
        .split('')
        .reverse()
        .join('')
        .replace(/^[\.]/, '');

    return `${cuerpoFormatoMiles}-${dv}`;
}