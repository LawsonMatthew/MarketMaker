import numpy as np

class HyperLiquidFillsHandler:

    def __init__(self, sharedstate, symbol: str) -> None:
        self.symbol = symbol
        self.hlq = sharedstate.private[self.symbol]

    def update(self, recv) -> None:
        #Will need to verify that "fills" websocket variables from userFills contains ALL fills
        self.hlq["exections"] = recv["data"]["fills"]
        #print(recv)