import numpy as np

class OrderBookHyperLiquid:

    def __init__(self) -> None:
        self.BBA = np.ones((2,2))

    def initialize(self, asks, bids) -> None:
        self.asks = np.array(asks, float)
        self.bids = np.array(bids, float)
        self.sort_book()

    """
    Sorts bids and asks. Highest bid at top of bids, lowest ask at top of ask.
    """
    def sort_book(self):
        self.asks = self.asks[self.asks[:,0].argsort()]
        self.bids = self.bids[self.bids[:,0].argsort()[::-1]]
        
    
    """
    Handles websocket response, parses level information and generates bid/ask arrays.
    """
    def update(self, recv):
        data = recv["data"].get("levels")
        asks = []
        bids = []
        #loop through each sublist and add level data to corresponding 
        for level in data[0]:
            asks.append([float(level["px"]), float(level["sz"])])

        for level in data[1]:
            bids.append([float(level["px"]), float(level["sz"])])

        self.initialize(asks, bids)
        self.calculateBBA()

    def calculateBBA(self):
        #BBA update under L2Book Handler beacuse of being calculated from L2Book response
        best_bid = self.bids[0]
        best_ask = self.asks[0]
        self.BBA[0] = best_ask # [Ask[], Bid[]]
        self.BBA[1] = best_bid
