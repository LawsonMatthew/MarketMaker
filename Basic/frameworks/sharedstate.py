import numpy as np
import asyncio
from numpy_ringbuffer import RingBuffer
from frameworks.tools.orderbook import OrderBookHyperLiquid
from frameworks.hyperliquid.websockets.streams import HyperLiquidDataStreams
from frameworks.hyperliquid.websockets.feeds.WSClient import HyperWebSocketClient

"""
Class holding all market data. Updated via websocket handlers.
"""
class SharedState:

    def __init__(self) :
        self.symbol = "BTC"

        self.market = {}
        self.private = {}

        self._initialize_market_data(OrderBookHyperLiquid())
        self._initialize_private_data()

        self.public_ws = HyperLiquidDataStreams(self.symbol)

        self.ws_req, self.ws_topics = self.public_ws.multi_stream_request(
            topics=["trades", "l2Book", "userEvents"], interval="1m")

    def _initialize_market_data(self, orderbook):
        """
        Outline for exchange market data in dict format.
        """
        self.market[self.symbol] = {
            "trades": RingBuffer(capacity=1000, dtype=(float, 4)), #Trade Handler
            "candles": RingBuffer(capacity=1000, dtype=(float, 8)), #Candle Handler
            "BBA": orderbook.BBA, # Format: [Ask[px, sz], Bid[px, sz]]
            "book": orderbook,

            "mark_price": 0, # Binance feed?
            "index_price": 0, # Binance feed?
            "last_price": 0,
            "mid_price": 0,
            "wmid_price": 0,
            "funding_rate": 0,
            "volume_24h": 0,

            "tick_size": 0,
            "lot_size": 0
        }
    
    def _initialize_private_data(self): 
        """
        Create dict to store private data for user address.
        """
        self.private["API"] = {
                "key": None,
                "secret": None,
                "rate_limits": {}, # TODO: Populated by OMS
                "taker_fees": None, # TODO: Initialized by OMS
                "maker_fees": None, # TODO: Initialized by OMS
            }
        
        self.private[self.symbol] = {
            "accountValue": None,
            "open_orders": [],
            "executions": [],

            "assetPostions": None,
            "currentUPNL": None,
            "totalMarginUsed": None
        }
    
    """
    Method to start ws feeds asynchronously.
    """
    async def stream(self):
        try:
            tasks = []
            for request in self.ws_req:
                task = asyncio.create_task(HyperWebSocketClient(request, self).start_stream())
                tasks.append(task)
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass