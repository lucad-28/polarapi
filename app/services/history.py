from app.utils.firestore import fetch_history_data
import pandas as pd

def get_history():
    df = fetch_history_data()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return restructure_df(df)

def restructure_df(df):
    grouped = df.groupby('deviceId')
    result = []

    for device_id, group in grouped:
        group_sorted = group.sort_values(by='timestamp')
        data_list = group_sorted[['timestamp', 'temperature', 'volume', 'cooling']].to_dict(orient='records')
        result.append({
            "deviceId": device_id,
            "data": data_list
        })

    return result

def get_resampled_history():
    df = fetch_history_data()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    numeric_cols = df.select_dtypes(include='number').columns
    df_resampled = df[numeric_cols].groupby(df["deviceId"]).resample('15min', label="left", closed="left").mean().reset_index()
    return restructure_df(df_resampled)