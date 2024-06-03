import numpy as np
import pandas as pd  # Ajoutez cette ligne

def remove_outliers(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    filtered_df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return filtered_df

def estimate_variability(df, column):
    return df[column].std()

def optimal_volume_interval(df, current_price):
    filtered_df = df[(df['close'] >= current_price * 0.95) & (df['close'] <= current_price * 1.05)]
    volume_interval = (filtered_df['volume'].min(), filtered_df['volume'].max())
    return volume_interval

def estimate_potential_gain(df, current_price):
    future_prices = df[df['timestamp'] > pd.Timestamp.now()]['close']
    potential_gain = (future_prices.max() - current_price) / current_price * 100
    return potential_gain
