class HyperLiquidMidsHandler:

    def __init__(self, sharedstate, symbol:str) -> None:
        self.mdss = sharedstate
        self.symbol = symbol
        self.hlq = self.mdss.market[symbol]

    def update(self, recv):
        mids = recv["data"]["mids"]
        midprice = mids[self.symbol]
        self.hlq["mid_price"] = midprice
        # print(recv)