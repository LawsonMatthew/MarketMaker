import numpy as np

class HyperLiquidCandlesHandler:

    def __init__(self, sharedstate, symobl: str) -> None:
        self.mdss = sharedstate
        self.symbol = symobl
        self.hlq = self.mdss.market[self.symbol]

    def update(self, recv):
        """
        Update the klines array 
        """
        data = recv["data"]
        new = np.array(
            object=[
                data["t"],
                data["T"],
                data["o"],
                data["c"],
                data["h"],
                data["l"],
                data["v"],
                data["n"],
            ], 
        )

        ring_buffer = self.hlq["candles"]
        
        if not ring_buffer or ring_buffer[0][0] != float(new[0]):
            ring_buffer.appendleft(new)