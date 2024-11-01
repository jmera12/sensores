// Función para obtener datos de sensores
async function fetchSensorData() {
    const response = await fetch('/api/sensores');
    const data = await response.json();
    const container = document.getElementById('data-container');
    container.innerHTML = data.map(item => `
        <p>Temperatura: ${item.temperature}°C | Humedad: ${item.humidity}% | Fecha: ${item.timestamp}</p>
    `).join('');
}

// Función para obtener imágenes
async function fetchImages() {
    const response = await fetch('/api/images');
    const images = await response.json();
    const container = document.getElementById('image-container');
    container.innerHTML = images.map(img => `
        <img src="/api/images/${img.image_path}" alt="Sensor Image">
        <p>${img.timestamp}</p>
    `).join('');
}

// Actualizar cada 10 segundos
setInterval(() => {
    fetchSensorData();
    fetchImages();
}, 10000);

document.addEventListener('DOMContentLoaded', () => {
    fetchSensorData();
    fetchImages();
});
