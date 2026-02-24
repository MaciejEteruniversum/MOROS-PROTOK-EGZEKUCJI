const terminal = document.getElementById('terminal');
const input = document.getElementById('commandInput');

function log(msg, color = 'text-zinc-400') {
    const p = document.createElement('p');
    p.className = `mb-1 ${color}`;
    p.innerText = `[${new Date().toLocaleTimeString()}]: ${msg}`;
    terminal.appendChild(p);
    terminal.scrollTop = terminal.scrollHeight;
}

function executeAction(bella) {
    const val = input.value.trim();
    if (!val) {
        log('BŁĄD: Brak danych wejściowych.', 'text-red-500');
        return;
    }
    log(`Wysłano rozkaz do ${bella}...`, 'text-white');
    log(`Przetwarzanie ładunku: ${val.substring(0, 40)}...`);
    setTimeout(() => {
        log(`${bella} potwierdza odbiór. Rozpoczynam workflow.`, 'text-red-700');
        input.value = '';
        // TODO: integrate with API / webhook
    }, 800 + Math.random() * 800);
}

// attach handlers
document.querySelectorAll('.action-btn').forEach(btn => {
    btn.addEventListener('click', () => executeAction(btn.dataset.bella));
});

// expose for console
window.moros = { executeAction, log };
