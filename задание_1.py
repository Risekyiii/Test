
import requests
from datetime import datetime, timedelta
import pytz

# запрос к ресурсу
def fetch_time():
    url = "https://yandex.com/time/sync.json?geo=213"
    utc = pytz.utc
    start_time = utc.localize(datetime.utcnow())  # Делает start_time aware
    response = requests.get(url)
    end_time = utc.localize(datetime.utcnow())  # Делает end_time aware


    print("Raw response:", response.text)

    # Ответ
    data = response.json()
    server_time_unix = data.get("time", None)
    timezone_name = data.get("tz_name", "UTC")  # Используем UTC как значение по умолчанию

    if server_time_unix is None:
        print("Время не получено от сервера.")
        return None, None, None

    try:
        # Преобразование времени
        server_time = datetime.utcfromtimestamp(server_time_unix / 1000.0).replace(tzinfo=utc)
        local_time = server_time.astimezone(pytz.timezone(timezone_name))
        print("дата и время:", local_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
        print("часовой пояс:", timezone_name)
    except pytz.UnknownTimeZoneError:
        print(f"неизвестный часовой пояс: {timezone_name}. Using UTC instead.")
        local_time = server_time
        timezone_name = "UTC"

    # Дельта времени
    delta = (server_time - start_time).total_seconds()
    print("Delta (seconds):", delta)

    return delta, timezone_name, local_time


if __name__ == "__main__":
    deltas = []
    for i in range(5):
        print(f"\nRequest {i + 1}:")
        delta, tz_name, human_time = fetch_time()
        if delta is not None:
            deltas.append(delta)

    if deltas:
        avg_delta = sum(deltas) / len(deltas)
        print(f"\nAverage delta over {len(deltas)} requests: {avg_delta:.2f} seconds")