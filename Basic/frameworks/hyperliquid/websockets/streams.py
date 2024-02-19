import json

class HyperLiquidDataStreams:

    def __init__(self, symbol = str):
        self.symbol = symbol

    def multi_stream_request(self, topics: list, **kwargs) -> tuple:
        """
        Creates a tuple of (JSON, list) containing a websocket request and corresponding list of streams
        """
        topiclist = []

        for topic in topics:
            
            #To add orderbook subscription for ticker
            if topic == "l2Book":
                topiclist.append({ "method": "subscribe", "subscription": {"type": "l2Book", "coin": self.symbol } })

            #To add all mid price subscription (not really necessary)
            if topic == "allMids":
                topiclist.append({ "method": "subscribe", "subscription": { "type": "allMids" } })

            #To add candle data subscription for specific interval type
            if topic == "candles":
                 topiclist.append({"method": "subscribe", "subscription": {"type": "candle", "coin": self.symbol, "interval": kwargs["interval"] } })
            
            #To add trades subscription
            if topic == "trades":
                topiclist.append({ "method": "subscribe", "subscription": { "type": "trades", "coin": self.symbol } })

            #PRIVATE DATA
            #To add WebData for user address
            if topic == "webData2":
                topiclist.append({ "method": "subscribe", "subscription": { "type": "webData2", "user": "0xca0bCff78b8973A8868C367525c96ee275D3902B" } })

            #To add orderUpdates for user address
            if topic == "orderUpdates":
                topiclist.append({ "method": "subscribe", "subscription": { "type": "orderUpdates", "user": 0xca0bCff78b8973A8868C367525c96ee275D3902B} })

            #To add userFill updates
            if topic == "userFills":
                 topiclist.append({"method": "subscribe", "subscription": { "type": "userFills", "user": "0xca0bCff78b8973A8868C367525c96ee275D3902B" } })
            
            #To add userFundings updates
            if topic == "userFundings":
                topiclist.append({ "method": "subscribe", "subscription": { "type": "userFundings", "user": "0xca0bCff78b8973A8868C367525c96ee275D3902B" } })

            #To add userNonFundingLedgerUpdates updates
            if topic == "userFundings":
                topiclist.append({ "method": "subscribe", "subscription": { "type": "userNonFundingLedgerUpdates", "user": 0xca0bCff78b8973A8868C367525c96ee275D3902B} })

            #to add userEvents
            if topic == "userEvents":
                topiclist.append({ "method": "subscribe", "subscription": { "type": "userEvents", "user": "0xca0bCff78b8973A8868C367525c96ee275D3902B" } })

        #create list of request objects for websocket subscriptions
        requests = []

        for topic in topiclist:
            requests.append(json.dumps(topic))

        return requests, topics
