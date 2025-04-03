from flask import Flask, jsonify, render_template
from coin_data import build_cripto_summary
from collections import OrderedDict
import time, requests

app = Flask(__name__)

# Configuración de cache
cache = OrderedDict()
CACHE_TTL = 300 # 5 minutos de cache
CACHE_MAX_SIZE = 1000 # almacena hasta 1000 monedas (ocupa aprox 30mb)

@app.route("/api/v1/coins/list")
def get_coin_list():
    now = time.time()

    if "coin_list" in cache and now - cache["coin_list"]["time"] < 3600:
        print("✅ USANDO CACHE de lista de monedas")
        return jsonify(cache["coin_list"]["data"])

    print("🌐 LLAMANDO API para lista de monedas con market_cap_rank")

    all_coins = []
    for page in range(1, 5):  # 4 páginas x 250 = top 1000
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": page
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return {"error": "No se pudo obtener la lista de monedas"}

        coins = response.json()

        # Asegurarnos de que tengan market_cap_rank
        filtered = [
            {"id": coin["id"], "symbol": coin["symbol"], "name": coin["name"]}
            for coin in coins if coin.get("market_cap_rank")
        ]
        all_coins.extend(filtered)

    cache["coin_list"] = {"data": all_coins, "time": now}
    return jsonify(all_coins)

@app.route("/api/v1/coin/<coin_id>")
def get_coin_summary(coin_id):
    now = time.time()

    if coin_id in cache and now - cache[coin_id]["time"] < CACHE_TTL:
        print(f"✅ USANDO CACHE para {coin_id}")
        response_data = cache[coin_id]["data"].copy()
        response_data["last_updated"] = cache[coin_id]["time"]
        return jsonify(response_data)

    print(f"🌐 LLAMANDO API para {coin_id}")
    data = build_cripto_summary(coin_id) #LLAMO A COINGECKO API
    cache[coin_id] = {"data": data, "time": now}

    response_data = data.copy()
    response_data["last_updated"] = now
    return jsonify(response_data)



@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
