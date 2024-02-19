import json

class BinanceDataStreams:

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

        #create list of request objects for websocket subscriptions
        requests = []

        for topic in topiclist:
            requests.append(json.dumps(topic))

        return requests, topics
