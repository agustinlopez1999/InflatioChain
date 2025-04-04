# 🧩 Resumen del Proyecto: Web para Análisis de Criptomonedas con CoinGecko + Flask

---

## 🚀 Objetivo

Crear una **página web** donde los usuarios puedan seleccionar una criptomoneda desde un listado dinámico y visualizar sus datos de mercado. Toda la información se obtiene desde la **API gratuita de CoinGecko**, con un backend en **Python + Flask**.

---

## 🔧 Etapas del desarrollo

### ✅ 1. Script base (Python)
- `main.py` consultaba CoinGecko y calculaba inflación de supply.
- Se transformó en `coin_data.py` para importar funciones desde Flask.

---

### ✅ 2. Backend Flask (`app.py`)
- Servidor con endpoints:
  - `/api/v1/coin/<coin_id>` → Datos de una cripto.
  - `/api/v1/coins/list` → Listado completo de criptomonedas (top 1000 por market cap).
- Usa `render_template()` para servir el HTML.

---

### ✅ 3. Sistema de caché en memoria
Para evitar sobrecargar la API de CoinGecko (50 req/min por IP):

- Cache implementado con `OrderedDict`
- `CACHE_TTL = 300` (5 minutos)
- `CACHE_MAX_SIZE = 1000` monedas

#### Ventajas:
- Menos llamadas a CoinGecko
- Respuestas más rápidas
- Eliminación automática de monedas viejas
- Soporta ~60–80 usuarios/min con criptos no repetidas

---

### ✅ 4. Estimación de uso de memoria
- 1 moneda: 10–30 KB
- 1000 monedas: ~10–30 MB
- Ideal para servidores chicos o medianos

---

### ✅ 5. Balance entre caché y usuarios
Con esta configuración:
- Hasta ~60–80 usuarios/min consultando criptos distintas
- Escala a cientos de usuarios si consultan monedas comunes
- El frontend nunca llama directamente a CoinGecko

---

### ✅ 6. Frontend HTML + JS
- Selector `<select>` dinámico con monedas (sólo las que tienen `market_cap_rank`)
- `fetch()` a `/api/v1/coin/<id>` al cambiar selección
- Carga inicial desde `/api/v1/coins/list`
- Muestra el tiempo desde la última actualización

---

### ✅ 7. Mejora UX: última actualización
- El backend envía `last_updated` como timestamp
- El frontend calcula "hace X minutos"
- Mejora transparencia y evita recargas innecesarias

---

### ❌ Evitado a propósito
- ❌ Llamadas directas del frontend a CoinGecko
- ❌ Botón "refrescar ahora" (para evitar abuso de la API)
- ❌ Cacheo persistente en disco (se considera innecesario para esta app)

---

### 🌐 API utilizada

CoinGecko Free API  
[https://www.coingecko.com/en/api/documentation](https://www.coingecko.com/en/api/documentation)  
📌 Límite gratuito: **50 requests por minuto por IP**

---

## 📦 Estructura del proyecto

```
/CRYPTO_INFLATION_WEB
├── app.py
├── coin_data.py
├── static/
│   └── script.js
├── templates/
│   └── index.html
├── README.md
```

---

## ✅ Estado actual

- ✔️ Funcional y estable
- ✔️ Cache eficiente y escalable
- ✔️ UX clara y robusta ante errores

---

## 📌 Próximas mejoras posibles:
- Mostrar logos y diseño visual más claro
- Permitir ordenar por ranking, nombre, etc.
- Agregar filtros (top 100, sólo activos)
- Mejor manejo de errores visuales en el frontend


---

## 📈 Consideraciones de Escalabilidad

### ¿Se cachea el 100% de las monedas?

✅ Sí. Se muestran únicamente las **top 1000 monedas con market_cap_rank**, y el valor `CACHE_MAX_SIZE = 1000` permite almacenarlas todas en memoria.

---

### ¿Se evita completamente llamar a la API?

❌ No. Aunque se pueden cachear todas, los datos:
- Se llenan progresivamente a medida que los usuarios las consultan
- Se renuevan cada 5 minutos (`CACHE_TTL = 300`)

---

### ¿Qué pasa si muchos usuarios hacen requests al mismo tiempo?

Si, por ejemplo, 20 usuarios piden 10 monedas no cacheadas en el mismo minuto:

→ 20 × 10 = 200 requests

🔴 Esto supera el límite gratuito de CoinGecko (50 req/min por IP).

---

### Estrategias para mitigar el problema:

- ✅ Usar caché con TTL de 5 minutos
- ✅ Evitar llamadas automáticas o botones de refresh
- ✅ Mostrar "última actualización" al usuario
- ✅ Precachear las monedas más comunes si es necesario
- ✅ Mantener control total desde el backend

Con estas prácticas, la app puede escalar con seguridad y eficiencia sin romper los límites de la API gratuita.

---

### ⚠️ Limitaciones de la API gratuita de CoinGecko

Aunque la API gratuita de CoinGecko permite hasta **50 requests por minuto**, se ha observado que:

- Algunas respuestas tienen `status 200 OK`, pero **faltan datos clave** como `market_data`, `current_price` o `market_cap`.
- Esto ocurre de forma intermitente, incluso con monedas muy conocidas como **Ethereum**, **Tether** o **Ripple**.
- Cuando eso sucede, la app devuelve:  
  `⚠️ Error: No se encontraron datos de mercado para esta moneda.`
- Gracias al manejo del backend, **no se cachean errores**, y el usuario puede volver a intentar más tarde.

🧠 Recomendación: evitar hacer múltiples llamados seguidos a monedas distintas para reducir la probabilidad de recibir respuestas incompletas.
