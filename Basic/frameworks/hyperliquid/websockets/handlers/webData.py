import numpy as np

class HyperLiquidWebDataHandler:

    def __init__(self, sharedstate, symbol: str) -> None:
        self.symbol = symbol
        self.hlq = sharedstate.private[self.symbol]

    def update(self, recv) -> None:
        self.hlq["accountValue"] = recv["data"]["clearinghouseState"]["marginSummary"]["accountValue"]
        self.hlq["totalMarginUsed"] = recv["data"]["clearinghouseState"]["marginSummary"]["totalMarginUsed"]
        self.hlq["open_orders"] = recv["data"]["openOrders"]
        self.hlq["assetPostions"] = recv["data"]["clearinghouseState"]["assetPositions"]
        #EXECUTIONS (MAYBE HANDLED BY USERFILLS?)
            #Updates currentUPNL too

        for row in recv["data"]:
            print(row)