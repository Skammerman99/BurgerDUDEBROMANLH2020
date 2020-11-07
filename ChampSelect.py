import requests
import json
from lcu_driver import Connector

connector = Connector()

@connector.ready
async def connect(connection):
    print("LCU API Successfully connected")
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    print(await summoner.json())
"""
@connector.ws.register('/lol-summoner/v1/current-summoner', event_types=('UPDATE',))
async def icon_changed(connection, event):
    print(f'The summoner {event.data["displayName"]} was updated.')
"""

@connector.close
async def disconnect(connection):
    print("Connection closed - Task Finished")

connector.start()