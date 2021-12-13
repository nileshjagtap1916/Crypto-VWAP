
from business.webSocket.client import WebSocketClient
import business.constants
import json
import re


class Business:

    # Constructor
    def __init__(self, loop=None) -> None:
        # declare dictionary of empty list per pair
        self.datapoint_dict = {}
        for ele in business.constants.PAIR_LIST:
            self.datapoint_dict[ele] = []

        # initialize websocket client connection. loop = async await loop
        if (loop):
            websocket_client = WebSocketClient()
            self.websocket_connection = loop.run_until_complete(
                websocket_client.connect())

    # process_message method : process the incoming message from webhook
    async def process_message(self, message):
        # if message not contains product_id, size and price, then return None.
        if message and "product_id" in message and "size" in message and "price" in message:

            # validation
            try:
                float(message["size"])
                float(message["price"])
            except:
                return None
            if message["product_id"] not in self.datapoint_dict.keys():
                return None

            # get existing pair specific queue
            datapoint_list = self.datapoint_dict[message["product_id"]]

            # declare new element of the pair specific queue
            new_element = {
                "pair_id": message["product_id"],
                "qty": float(message["size"]),
                "price": float(message["price"])
            }

            # If pair specific queue reached to the configured limit
            if (len(datapoint_list) == business.constants.LIST_LIMIT):
                # get last element of the queue
                last_ele = datapoint_list[-1]

                # delete first element from the queue
                poped_ele = datapoint_list.pop(0)

                # calculate qty_sum and price_qty_sum using deleted element and last element values
                new_element["qty_sum"] = last_ele["qty_sum"] - \
                    poped_ele["qty"] + float(message["size"])

                new_element["price_qty_sum"] = last_ele["price_qty_sum"] - \
                    poped_ele["price_qty_sum"] + \
                    (float(message["price"]) * float(message["size"]))

            # if pair specific queue length between 1 to configured limit
            elif len(datapoint_list) > 0:
                # get last element of the queue
                last_ele = datapoint_list[-1]

                # calculate qty_sum and price_qty_sum using last element values
                new_element["qty_sum"] = last_ele["qty_sum"] + \
                    float(message["size"])

                new_element["price_qty_sum"] = last_ele["price_qty_sum"] + \
                    (float(message["price"]) * float(message["size"]))

            # if pair specific queue is empty
            else:
                # initialize first element of the queue
                new_element["qty_sum"] = float(message["size"])
                new_element["price_qty_sum"] = float(
                    message["price"]) * float(message["size"])

            # avoid divide by zero error. Calculate VWAP and return
            if new_element["qty_sum"] != 0:
                new_element["VWAP"] = new_element["price_qty_sum"] / \
                    new_element["qty_sum"]
                datapoint_list.append(new_element)

                return new_element["VWAP"]

    # receive_message method : start receiving messages from webhook
    async def receive_message(self):
        while True:
            try:
                # reveive message
                message = await self.websocket_connection.recv()

                # process message
                VWAP = await self.process_message(json.loads(message))

                # print VWAP
                if (VWAP):
                    print('Pair : {}, VWAP : {}'.format(
                        json.loads(message)["product_id"], VWAP))

            except Exception as inst:
                print('Connection with server closed')
                break
