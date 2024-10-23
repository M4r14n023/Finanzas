const iconMode = document.getElementById('icon-mode');

// Revisa si el usuario tiene guardada la preferencia de modo oscuro
if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
    iconMode.classList.remove('fa-sun');
    iconMode.classList.add('fa-moon');
}

// Alterna el modo oscuro y guarda la preferencia en localStorage
iconMode.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');

    if (document.body.classList.contains('dark-mode')) {
        iconMode.classList.remove('fa-sun');
        iconMode.classList.add('fa-moon');
        localStorage.setItem('darkMode', 'enabled'); // Guarda la preferencia en modo oscuro
    } else {
        iconMode.classList.remove('fa-moon');
        iconMode.classList.add('fa-sun');
        localStorage.setItem('darkMode', 'disabled'); // Guarda la preferencia en modo claro
    }
});




