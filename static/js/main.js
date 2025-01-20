// Fecha modais quando clica no X ou fora do modal
document.addEventListener('DOMContentLoaded', function() {
    const modais = document.getElementsByClassName('modal');
    const closes = document.getElementsByClassName('close');

    // Fecha modal ao clicar no X
    Array.from(closes).forEach(close => {
        close.onclick = function() {
            Array.from(modais).forEach(modal => {
                modal.style.display = "none";
            });
        }
    });

    // Fecha modal ao clicar fora dele
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = "none";
        }
    }
}); 