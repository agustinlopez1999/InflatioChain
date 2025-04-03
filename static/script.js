const select = document.getElementById('coin-select');
const resultBox = document.getElementById('result');
const lastUpdate = document.getElementById('last-update');

function formatearTiempo(diferenciaSegundos) {
  const minutos = Math.floor(diferenciaSegundos / 60);
  const segundos = Math.floor(diferenciaSegundos % 60);
  return `${minutos}m ${segundos}s`;
}

async function fetchCoinData(coinId) {
    const res = await fetch(`/api/v1/coin/${coinId}`);
    const data = await res.json();
  
    if (data.error) {
      resultBox.textContent = `⚠️ Error: ${data.error}`;
      lastUpdate.textContent = "";
      return;
    }
  
    resultBox.textContent = JSON.stringify(data, null, 2);
  
    const ahora = Date.now() / 1000;
    const actualizado = data.last_updated;
    const diferencia = ahora - actualizado;
  
    lastUpdate.textContent = `Última actualización: hace ${formatearTiempo(diferencia)}`;
  }
  

async function cargarMonedas() {
  const res = await fetch("/api/v1/coins/list");
  const coins = await res.json();

  select.innerHTML = ""; // limpiar opciones previas

  coins.forEach(coin => {
    const option = document.createElement("option");
    option.value = coin.id;
    option.textContent = `${coin.name} (${coin.symbol.toUpperCase()})`;
    select.appendChild(option);
  });

  // Cargar la primera cripto por defecto
  fetchCoinData(select.value);
}

// Escuchar cambio de selección
select.addEventListener('change', () => {
  fetchCoinData(select.value);
});

// Llamar al cargar la página
cargarMonedas();
