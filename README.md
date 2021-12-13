# Crypto VWAP calculator
A Crypto Currency VWAP calculator which calculates the running Volume-Weighted Average Price for given cryptocurrency exchanges within given window. 

## Design
* As program is listening the messages from WebSocket, it needs to be run asynchronously to avoid miss-calculation.
* To improve the calculation performance, Queue logic has been implemented which runs the program in O(1) time complexity.
* Class Business:
  * Receive message : Continuously receives the messages from pre-configured WebSocket client
  * Process message : Process the message and calculate the VWAP withing pre-configured window
* Class WebSocket:
  * Connect : connect to the pre-configured WebSocket client.
  * Close : close the connection with WebSocket client.

## Configuration
Configurations can be change from `./business/constants.py`.
* `LIST_LIMIT`: The limit of window per crypto pair. Default is **200**
* `PAIR_LIST`: The list of crypto pairs for which VWAP will get calculated. Default is `BTC-USD,ETH-USD,ETH-BTC`
* `WEBSOCKET_SERVER`: WebSocket server URL. Default is Coinbase.

## Software Requirement
Python (version 3)

## How to Run
Install Pre-requisite
```
pip install -r requirements.txt
```
Run program 
```
python .\main.py
``` 
Close program
```
CTRL+C
```
Run test cases
```
python -m unittest -v
```
