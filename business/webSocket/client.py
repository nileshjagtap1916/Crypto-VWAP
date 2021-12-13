import websockets
import json
import business.constants


class WebSocketClient():
    def __init__(self):
        pass

    # connect to websocket server
    async def connect(self):

        self.connection = await websockets.connect(business.constants.WEBSOCKET_SERVER)
        if self.connection.open:
            # Send subscribe message
            sub_message = {
                "type": "subscribe",
                "channels": [
                    {
                        "name": "matches",
                        "product_ids": business.constants.PAIR_LIST
                    }
                ]
            }

            await self.sendMessage(json.dumps(sub_message))
            return self.connection

    # send message to websocket server
    async def sendMessage(self, message):
        await self.connection.send(message)

    # close connection
    async def closeConnection(self, message):
        await self.connection.close()
