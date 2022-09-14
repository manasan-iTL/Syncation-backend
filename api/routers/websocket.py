import socketio

sio = socketio.AsyncServer(async_mode = "asgi", cors_allowed_origins=[])

async def checkhander():
    print("イベントを受信しました。") 

@sio.event
async def connect(sid, environ):
    """socketioのconnectイベント
    """
    print('connect ', sid)
    await sio.emit("enter", {"user": sid})
    print("実行されました。")

@sio.event
async def join_room(sid, data):
    """socketioのconnectイベント
    """
    print(data["roomId"] + "ユーザ名：" + data["username"] + "がルームに入室しました。")
    # ルームIDが存在するのかを判定する（DBにルームIDが存在しているか）
    print(data["roomId"])
    sio.enter_room(sid, data["roomId"])
    await sio.emit("joined_room", {"id": sid, "username": data["username"]}, room=data["roomId"])
    return {"result": "Success"}

@sio.event
async def send_time(sid, data):
    print(data["type"] + "の時間：" + data["time"])
    await sio.emit("receive_time", {"type": data["type"], "time": data["time"]}, room=data["roomId"])

# @sio.event
# async def entered_room(sid, data):
#     """socketioのconnectイベント
#     """
#     print("ユーザ名：" + sid, data["username"] + "がルームに入室しました。")

@sio.event
async def python_test(sid):
    """socketioのdisconnectイベント
    """
    await sio.emit("python_test", "Backend recieved")

@sio.event
async def test_send(sid, data):
    """socketioのdisconnectイベント
    """
    print(data)

@sio.event
async def disconnect(sid):
    """socketioのdisconnectイベント
    """
    print('disconnect ', sid)