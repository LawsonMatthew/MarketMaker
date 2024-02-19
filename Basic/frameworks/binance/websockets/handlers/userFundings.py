import numpy as np

class HyperLiquidFundingsHandler:

    def __init__(self, sharedstate, symbol: str) -> None:
        self.symbol = symbol
        self.hlq = sharedstate.private[self.symbol]

    def update(self, recv) -> None:
        print(recv)