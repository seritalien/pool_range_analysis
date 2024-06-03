from flask import Flask, render_template, jsonify
import threading
import time
import pandas as pd
from data_fetcher import get_binance_data
from data_processor import remove_outliers, estimate_variability, optimal_volume_interval, estimate_potential_gain

app = Flask(__name__)

symbol = 'BTCUSDT'
interval = '1h'
start = int(pd.Timestamp('2023-01-01').timestamp() * 1000)
end = int(pd.Timestamp('2023-06-01').timestamp() * 1000)

df = get_binance_data(symbol, interval, start, end)
df_filtered = remove_outliers(df, 'close')
variability = estimate_variability(df_filtered, 'close')
current_price = df_filtered['close'].iloc[-1]
volume_interval = optimal_volume_interval(df_filtered, current_price)
potential_gain = estimate_potential_gain(df_filtered, current_price)

# Fonction pour mettre à jour les données
def update_data():
    global df, df_filtered, variability, volume_interval, potential_gain
    while True:
        df = get_binance_data(symbol, interval, start, end)
        df_filtered = remove_outliers(df, 'close')
        variability = estimate_variability(df_filtered, 'close')
        current_price = df_filtered['close'].iloc[-1]
        volume_interval = optimal_volume_interval(df_filtered, current_price)
        potential_gain = estimate_potential_gain(df_filtered, current_price)
        time.sleep(3600)  # Met à jour toutes les heures

# Démarrer le thread de mise à jour des données
threading.Thread(target=update_data).start()

@app.route('/')
def index():
    return render_template('index.html', variability=variability, volume_interval=volume_interval, potential_gain=potential_gain)

@app.route('/data')
def data():
    return jsonify(df.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
