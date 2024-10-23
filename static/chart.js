document.addEventListener('DOMContentLoaded', function() {
    // Código para crear el gráfico de torta
    const ctx = document.getElementById('graficoTorta').getContext('2d');
    const egresosData = JSON.parse(document.getElementById('egresosData').value);

    const labels = egresosData.map(item => item.categoria);
    const data = egresosData.map(item => item.monto);

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Repartición de Egresos',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });

    // Obtener el botón y el body
    const themeToggleButton = document.getElementById("theme-toggle");
    const body = document.body;

    // Al cargar la página, verifica si hay una preferencia guardada
    window.onload = () => {
        if (localStorage.getItem("theme") === "dark") {
            body.classList.add("dark-mode");
            themeToggleButton.textContent = "Modo Claro";
        }
    };

    // Función para cambiar el tema
    themeToggleButton.addEventListener("click", () => {
        body.classList.toggle("dark-mode"); // Alternar la clase dark-mode en el body
        
        // Cambiar el texto del botón según el tema activo
        if (body.classList.contains("dark-mode")) {
            themeToggleButton.textContent = "Modo Claro"; // Cambia a modo claro
            localStorage.setItem("theme", "dark"); // Guarda la preferencia en localStorage
        } else {
            themeToggleButton.textContent = "Modo Oscuro"; // Cambia a modo oscuro
            localStorage.setItem("theme", "light"); // Guarda la preferencia en localStorage
        }
    });
});

