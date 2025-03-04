from app.utils.firestore import fetch_history_data, fetch_history_data_by_devicesIds
import pandas as pd
from app.utils.firestore import update_history_data

def get_history() -> list:
    df = fetch_history_data()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.loc[df["cooling"] > 0, "cooling"] = 1
    return restructure_df(df)


def get_resampled_history():
    df = fetch_history_data()
    df.loc[df["cooling"] > 0, "cooling"] = 1
    return resample_df(df, "15min")

def get_history_by_devicesIds(deviceIds: list) -> list:
    df = fetch_history_data_by_devicesIds(deviceIds)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.loc[df["cooling"] > 0, "cooling"] = 1
    return resample_df(df)

def get_resampled_history_by_devicesIds(deviceIds: list):
    print(deviceIds)
    df = fetch_history_data_by_devicesIds(deviceIds)
    return resample_df(df, "15min")

def restructure_df(df: pd.DataFrame) -> list:
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

def resample_df(df: pd.DataFrame, rule: str = '15min') -> list:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    numeric_cols = df.select_dtypes(include='number').columns
    df_resampled = df[numeric_cols].groupby(df["deviceId"]).resample(rule, label="left", closed="left").mean().reset_index()
    return restructure_df(df_resampled)

def update_history(deviceId):
    df = pd.read_csv('simulated_temperature_data_15min_2.csv', index_col='timestamp', parse_dates=True)
    df['deviceId'] = deviceId
    df["timestamp"] = pd.to_datetime(df.index)
    records = df.to_dict(orient='records')
    
    for record in records:
        update_history_data(deviceId, record)

    return {'message': 'History updated successfully'}