from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from app.utils.model_trained import model, gen_random_data
from app.utils.firestore import fetch_history_by_devicesIds

required_data = 20
train_len = 17280 * 2
train_start = datetime(2025, 2, 28, 8, 10, 1)
train_end = datetime(2025, 3, 2, 8, 9, 56)

def predict_by_devices(deviceIds, time):
    if len(deviceIds) == 0:
        return []
    history = fetch_history_by_devicesIds(deviceIds, final_day=pd.to_datetime(time))

    if len(history) == 0:
        return []
    
    history['timestamp'] = pd.to_datetime(history['timestamp'])
    dfs_by_device = [history[history['deviceId'] == deviceId] for deviceId in history['deviceId'].unique()]
    
    result_dict = {}
    time_predict = pd.to_datetime(time)

    for deviceId in deviceIds:
        mean_predict = get_predict(time_predict)
        result_dict[deviceId] = {
            "deviceId": deviceId,
            "meanTemperature": mean_predict
        }

    for df in dfs_by_device:
        print(result_dict)
        deviceId = df['deviceId'].iloc[0]

        df = df.drop(columns=["cooling", "volume", "deviceId"])
        df["hour_minute"] = df["timestamp"].dt.hour + df["timestamp"].dt.minute / 60.0

        df = df[df["timestamp"] >= time_predict - pd.Timedelta(hours=3)]

        if (len(df) > 1):
            tendencia = df["temperature"].diff().mean()
        else:
            tendencia = 0  # Si hay una sola lectura, no hay tendencia

        mean_predict = get_predict(time_predict)
        
        mean_predict_ajusted = mean_predict + tendencia * 0.5

        if deviceId in result_dict:
            result_dict[deviceId]["meanTemperature"] = mean_predict_ajusted
        else:
            result_dict[deviceId] = {
                "deviceId": deviceId,
                "meanTemperature": mean_predict_ajusted
            }

    return list(result_dict.values())


def get_predict(time_predict):

    input_features = {
        "hour": time_predict.hour,
        "minute": time_predict.minute,
        "day": time_predict.day,
        "month": time_predict.month,
        "dayofweek": time_predict.dayofweek
    }
    
    df_input = pd.DataFrame([input_features])

    future_hours = [time_predict + timedelta(minutes=15 * i) for i in range(12)]
    future_predicts = []

    for future_hour in future_hours:
        df_input["hour"] = future_hour.hour
        df_input["minute"] = future_hour.minute
        df_input["day"] = future_hour.day
        df_input["month"] = future_hour.month
        df_input["dayofweek"] = future_hour.dayofweek

        predict = model.predict(df_input)[0]
        future_predicts.append(predict)
    
    return np.mean(future_predicts)


'''
def get_predict(d_model, df: pd.DataFrame, hours_step = 3, d_train_end = train_end, d_train_len = train_len):
    model_ac = d_model.apply(df)
    predict_start = datetime.now().replace(second=0, microsecond=0)
    predict_end = predict_start + timedelta(hours=hours_step)

    if predict_start <= d_train_end:
        predict_start = d_train_end + timedelta(seconds=5)
        predict_end = predict_start + timedelta(hours=hours_step)
    
    start_idx = train_len + int((predict_start - d_train_end).total_seconds() / 5)
    end_idx = train_len + int((predict_end - d_train_end).total_seconds() / 5)

    predcc = model_ac.predict(start=start_idx, end=end_idx)

    return { predcc.index.tolist(), predcc.tolist() }
'''

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

def restructure_prediction(df):
    grouped = df.groupby('deviceId')
    result = []

    for device_id, group in grouped:
        group_sorted = group.sort_values(by='timestamp')
        data_list = [
            {k: (None if pd.isna(v) else v) for k, v in record.items()} 
            for record in group_sorted[['timestamp', 'temperature']].to_dict(orient='records')
        ]
        result.append({
            "deviceId": device_id,
            "data": data_list
        })

    return result