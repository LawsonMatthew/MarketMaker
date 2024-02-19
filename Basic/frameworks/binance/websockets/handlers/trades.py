import numpy as np

class HyperLiquidTradesHandler:

    def __init__(self, sharedstate, symbol: str) -> None:
        self.symbol = symbol
        self.hlq = sharedstate.market[self.symbol]

    def update(self, recv) -> None:
        for row in recv["data"]:
            if not row["coin"] == self.symbol:
                continue
            side = 0 if row["side"] == "B" else 1
            trade = np.array([row["time"], side, row["px"], row["sz"]])
            self.hlq["trades"].append(trade)
            self.hlq["last_price"] = float(trade[2])
            #print(trade)