from json import loads
from time import sleep
from json import dumps
from websocket import WebSocket
from concurrent.futures import ThreadPoolExecutor

guild_id = input("Guild ID: ")
chid = input("Channel ID: ")
tokenlist = open("tokens.txt").read().splitlines()
executor = ThreadPoolExecutor(max_workers=int(1000000))
mute = False
deaf = False
def run(token) :
    ws = WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    hello = loads(ws.recv())
    heartbeat_interval = hello['d']['heartbeat_interval']
    ws.send(dumps({"op": 2,"d": {"token": token,"properties": {"$os": "windows","$browser": "Discord","$device": "desktop"}}}))
    ws.send(dumps({"op": 4,"d": {"guild_id": guild_id,"channel_id": chid,"self_mute": mute,"self_deaf": deaf}}))
    ws.send(dumps({"op": 18,"d": {"type": "guild","guild_id": guild_id,"channel_id": chid,"preferred_region": "singapore"}}))
    while True:
        sleep(heartbeat_interval/1000)
        try:
            ws.send(dumps({"op": 1,"d": None}))
        except Exception:
            break

i = 0
for token in tokenlist:
    executor.submit(run, token)
    i+=1
    print("WebSocket Connected : {}".format(i))
