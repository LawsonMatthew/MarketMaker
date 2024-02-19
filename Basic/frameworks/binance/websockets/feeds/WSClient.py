import orjson
import websockets
import asyncio
import time

from frameworks.hyperliquid.endpoints import WSEndpoints
from frameworks.hyperliquid.websockets.handlers.trades import HyperLiquidTradesHandler
from frameworks.hyperliquid.websockets.handlers.candles import HyperLiquidCandlesHandler
from frameworks.hyperliquid.websockets.handlers.mids import HyperLiquidMidsHandler
from frameworks.hyperliquid.websockets.handlers.webData import HyperLiquidWebDataHandler
from frameworks.hyperliquid.websockets.handlers.fills import HyperLiquidFillsHandler
from frameworks.hyperliquid.websockets.handlers.userFundings import HyperLiquidFundingsHandler
from frameworks.hyperliquid.websockets.handlers.userEvents import HyperLiquidUserEventsHandler

class WebSocketClient:

    def __init__(self, request, sharedstate):
        self.mdss = sharedstate
        self.subscription_id_counter = 0
        self.symbol = self.mdss.symbol
        self.request = request
        self.channel = orjson.loads(request)["subscription"]["type"]
        self.req = request
        self.last_received_time = time.time()
        self.heartbeat_cancelled = False

        # Handler map
        self.channel_handler = {
            "l2Book" : self.mdss.market[self.symbol]["book"].update,
            "candle" : HyperLiquidCandlesHandler(self.mdss, self.symbol).update,
            "allMids" : HyperLiquidMidsHandler(self.mdss, self.symbol).update,
            "trades" : HyperLiquidTradesHandler(self.mdss, self.symbol).update,
            "webData2" : HyperLiquidWebDataHandler(self.mdss, self.symbol).update,
            "userFills" : HyperLiquidFillsHandler(self.mdss, self.symbol).update,
            "userFundings" : HyperLiquidFundingsHandler(self.mdss, self.symbol).update,
            "userEvents" : HyperLiquidUserEventsHandler(self.mdss, self.symbol).update
        }

    async def send_heartbeat(self, websocket, channel, interval=55):
        try:
            while True:
                await asyncio.sleep(interval)
                await websocket.send('{"method": "ping"}')
                print(f"Ping sent to {channel} WebSocket")
        except asyncio.CancelledError:
            if not self.heartbeat_cancelled:
                self.heartbeat_cancelled = True
                print(f"{channel} heartbeat task closed.")

    async def start_heartbeat(self, websocket, channel):
        try:
            while not self.heartbeat_cancelled:
                await self.send_heartbeat(websocket, channel)
        except asyncio.CancelledError:
            # Handle cancellation gracefully
            if not self.heartbeat_cancelled:
                self.heartbeat_cancelled = True
                print(f"{channel} heartbeat task closed.")


    async def start_stream(self):
        async with websockets.connect(WSEndpoints.COMBINED_STREAM) as websocket:
            print(f"{self.channel} : Market Data")
            # Start the heartbeat coroutine for trades channel
            if self.channel == "trades" or "userEvents":
                heartbeat_task = asyncio.create_task(self.start_heartbeat(websocket, self.channel))

            try:
                await websocket.send(self.request)

                while True:
                    recv = orjson.loads(await websocket.recv())
                    handler = self.channel_handler.get(recv["channel"])

                    if handler:
                        handler(recv)

                    # Update the last received time
                    self.last_received_time = time.time()

            except websockets.ConnectionClosed:
                print(f"Disconnected from {self.channel} WebSocket")
            except asyncio.CancelledError:
                pass

            finally:
                # Ensure WebSocket closure
                await websocket.close()

                # Cancel the heartbeat task when exiting
                if self.heartbeat_cancelled:
                    heartbeat_task.cancel()