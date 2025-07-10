import psutil
import datetime
from influxdb import InfluxDBClient

def collect_metrics():
    uptime_seconds = (datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())).total_seconds()
    uptime_hours = round(uptime_seconds / 3600, 2)
    metrics = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "disk_used_gb": round(psutil.disk_usage('/').used / (1024**3), 2),
        "uptime_hours": uptime_hours
    }
    return metrics

def write_to_influxdb(client, data):
    json_body = [{
        "measurement": "system_metrics",
        "fields": data
    }]
    client.write_points(json_body)

if __name__ == "__main__":
    client = InfluxDBClient(host='influxdb', port=8086)
    client.switch_database('metrics')
    while True:
        data = collect_metrics()
        write_to_influxdb(client, data)
