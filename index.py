from flask import Flask, request, jsonify
from threading import Thread
import time
import requests

from pingpongthread import PingPongThread

PingPong = PingPongThread(number=4)
PingPong.start()
PingPong.wait_until_full_connect()

PingPong.receive_sensor_data(1, method="periodic", period=0.1)
PingPong.receive_sensor_data(2, method="periodic", period=0.1)
PingPong.receive_sensor_data(3, method="periodic", period=0.1)

webhook = "api_key"

def send_discord_webhook(sensor_id, value):
    data = {
        "content": f"{sensor_id}번 센서에서 물건이 감지됨 (값: {value})",
        "username": "감지기"
    }
    response = requests.post(webhook, json=data)

    if response.status_code == 204:
        print('Message sent successfully!')
    else:
        print(f'Failed to send message: {response.status_code} - {response.text}')

app = Flask(__name__)

itemss = [
    {"name": "샌드위치", "price": 1600, "sensor": 1, "paid": False},
    {"name": "샌드위치", "price": 1600, "sensor": 2, "paid": False},
    {"name": "빵", "price": 2200, "sensor": 3, "paid": False},
]

@app.route('/reset')
def reset():
    itemss = [
        {"name": "샌드위치", "price": 1600, "sensor": 1, "paid": False},
        {"name": "샌드위치", "price": 1600, "sensor": 2, "paid": False},
        {"name": "빵", "price": 2200, "sensor": 3, "paid": False},
    ]
    return 'done'

@app.route('/')
def main():
    return htmlViewer("/html/index.html")

@app.route('/kiosk')
def kioskUI():
    return htmlViewer("/html/kiosk.html")

@app.route('/iteminfo/<id>')
def getItemInfo(id):
    return itemss[int(id)]

@app.route('/api/items')
def itemsAPI():
    return itemss

@app.route('/success/<id>')
def success(id):
    itemss[int(id)]["paid"] = True
    return htmlViewer("/html/success.html")

def sensor_loop():
    prev_values = {1: 100, 2: 100, 3: 100}

    while True:
        PingPong.clear_output()
        for sensor_id in [1, 2, 3]:
            value = PingPong.get_current_proxy(sensor_id)
            print(f"{sensor_id}: {value}", end='  ')

            if value is not None and value < 70 and prev_values[sensor_id] >= 70:
                item = next((item for item in itemss if item["sensor"] == sensor_id), None)
                if item:
                    if not item["paid"]:
                        PingPong.run_motor_step(4, 30, 90/360)
                        time.sleep(90/360/30*60)
                        send_discord_webhook(sensor_id, value)
                    else:
                        print(f"결제됨")
                else:
                    print(f"센서에 해당되는 물품 없음")
            else:
                print()

            prev_values[sensor_id] = value if value is not None else prev_values[sensor_id]

        time.sleep(0.1)

def htmlViewer(dir):
    with open(dir, "r") as f:
        return f.read()

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=5050)).start()
    Thread(target=sensor_loop).start()
