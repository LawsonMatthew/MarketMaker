# MarketMaker

Attempting to build a simple market making model to provide liquidity for hyperliquid dex.

Inspired by @BeatzXBT and his SMM repo (https://github.com/beatzxbt/bybit-smm)

TO DO:
- Finalize Feed processing in SharedState
- Basic Trading Logic (1 side bid/ask @ set bps from mid)
- Implement OMS
- Implement signing (see hyperliquid docs)
  
COMPLETED:
- Websocket connections implemented
- Feed handlers update SharedState

Status:
Not close to finished. HL websocket data updating sharedstate via feed handlers. May need to revisit repo structure.
