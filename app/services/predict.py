import pandas as pd
import numpy as np
from app.utils.model_trained import model, gen_random_data

def predict():
    df = gen_random_data()
    save = df.copy()
    
    df = df.drop(columns=["cooling", "volume"])
    df.set_index('timestamp', inplace=True)
    df = df.asfreq('5s', method='ffill')

    train_size = int(len(df) * 0.8)
    train, test = df.iloc[:train_size], df.iloc[train_size:]


    model_ac = model.apply(test)
    forecast_ac = model_ac.forecast(steps=len(test))

    _fullTemperature = train["temperature"].values.tolist() + forecast_ac.tolist()
    output = pd.DataFrame({ "timestamp": df.index.values.tolist() , "temperature": _fullTemperature, "cooling": save["cooling"], "volume": save["volume"]})
    output['deviceId'] = "device1"
    print(output.describe())

    return restructure_df(output)

def restructure_df(df):
    grouped = df.groupby('deviceId')
    result = []

    for device_id, group in grouped:
        group_sorted = group.sort_values(by='timestamp')
        data_list = [
            {k: (None if pd.isna(v) else v) for k, v in record.items()} 
            for record in group_sorted[['timestamp', 'temperature', 'volume', 'cooling']].to_dict(orient='records')
        ]
        result.append({
            "deviceId": device_id,
            "data": data_list
        })

    return result