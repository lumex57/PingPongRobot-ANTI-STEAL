# PingPongRobot ANTI-STEAL  
핑퐁 도난 방지기 (2025 청소년 SW동행 프로젝트)

## 개요  
적외선 센서와 모터를 활용하여 결제 없이 물건을 가져가면 Discord 알림을 보내는 키오스크 시스템,
Flask로 웹 서버를 구성하고, PingPongThread를 통해 센서 데이터를 실시간 수신함

---

## 코드 설명

```py
from pingpongthread import PingPongThread
```
- 핑퐁 로봇 연결에 필요한 모듈 불러오기

```py
PingPong = PingPongThread(number=4)
PingPong.start()
PingPong.wait_until_full_connect()
```
- 핑퐁 로봇 4개 연결 (1~3번: 센서, 4번: 모터)

```py
PingPong.receive_sensor_data(1, method="periodic", period=0.1)
PingPong.receive_sensor_data(2, method="periodic", period=0.1)
PingPong.receive_sensor_data(3, method="periodic", period=0.1)
```
- 1~3번 핑퐁을 센서로 사용  
- 0.1초 간격으로 센서값 수신

```py
def send_discord_webhook(sensor_id, value):
    ...
```
- 결제 없이 물건이 감지되면 디코로로 경고 메시지 전송

```py
@app.route('/reset')
def reset():
    ...
```
- 결제 상태 초기화 API

```py
@app.route('/success/<id>')
def success(id):
    ...
```
- 특정 상품 결제 완료 처리 후 성공 페이지로 이동

```py
@app.route('/api/items')
def itemsAPI():
    ...
```
- 현재 모든 상품 정보(JSON) 제공

```py
def sensor_loop():
    ...
```
- 센서 루프 실행  
- 값이 70 이하로 떨어지고 결제가 안 되어 있으면  
  -> 모터 작동 (경고)  
  -> 알림 전송

---

## 물품 데이터

```py
itemss = [
    {"name": "샌드위치", "price": 1600, "sensor": 1, "paid": False},
    {"name": "샌드위치", "price": 1600, "sensor": 2, "paid": False},
    {"name": "빵", "price": 2200, "sensor": 3, "paid": False},
]
```

- `name`: 물품 이름  
- `price`: 가격 (원)  
- `sensor`: 연결된 센서 번호  
- `paid`: 결제 여부 (`True`면 결제 완료)



## 페이지 안내

- `/` → 메인 화면  
- `/kiosk` → 키오스크 UI  
- `/iteminfo/<id>` → 개별 상품 정보  
- `/success/<id>` → 결제 완료 화면  
- `/reset` → 모든 상품 결제 상태 초기화  

---

## 기타

- 디코 웹훅 전송은은 코드 상단 `webhook = "api_key"` 부분에 본인의 웹훅 URL을 입력해야 작동함
- 센서값 기준은 70으로 설정되어 있으며, 상황에 따라 조정 가능함

## Special Thanks 
- [@Requax27](https://github.com/Requax27/)
