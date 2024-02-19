import asyncio
from frameworks.sharedstate import SharedState

class BasicAdding:

    def __init__(self, ss: sharedstate) -> None:
        self.ss = ss
        self.params = {
            "spread": 0.005,  # 0.5% spread
            "evaluation_interval": 1  # Evaluate every 1 second
        }
        self.current_ask_order = None
        self.current_bid_order = None

    async def run(self) -> None:
        await asyncio.sleep(5)
        print("Starting Strategy...")

        while True:
            try: 
                await self.evaluate_market_conditions()
            except Exception as e:
                print(f"Error in strategy execution: {e}")
            await asyncio.sleep(self.params['evaluation_interval'])
                            
    async def evaluate_market_conditions(self):
        bid_price, ask_price = self.calculate_order_prices(self.ss.market[self.ss.symbol])

        if self.current_bid_order == None:
            self.current_bid_order = await self.place_limit_order('buy', bid_price)
        
        if self.current_ask_order == None:
            self.current_ask_order = await self.place_limit_order('sell', ask_price)

    def calculate_order_prices(self, market_data):
        last_price = market_data['last_price']
        spread = self.params['spread']
        bid_price = last_price * (1 - spread)
        ask_price = last_price * (1 + spread)
        return bid_price, ask_price
    
    async def place_limit_order(self, side, price):
        # Replace with actual logic to place orders via an exchange's API
        print(f"Placing {side} order at {price}")
        return {'side': side, 'price': price}  # Mock return value representing the order
    

# import asyncio
# from frameworks.sharedstate import SharedState
# from stink_biddor.strategy.levels import StinkLevels
# from stink_biddor.strategy.safeties import StinkSafeties
# from stink_biddor.settings import StinkBiddorParameters


# class StinkBiddor:

#     def __init__(self, ss: SharedState, params: StinkBiddorParameters) -> None:
#         self.ss = ss
#         self.pair, self.levels = params.pair, params.levels
#         self.logging = self.ss.logging

#         self.safety = StinkSafeties(self.ss, params)
        
#     async def run(self) -> None:
#         self.logging.info("Warming up data feeds & strategy monitoring loops...")
#         asyncio.create_task(asyncio.to_thread(self.safety.monitor))
#         await asyncio.sleep(5)

#         self.logging.info(f"Starting strategy on {self.pair} with {len(self.levels) * 2} levels...")

#         while True:
#             tasks = []

#             for level in self.levels:
#                 tasks.append(StinkLevels(self.ss, level).bid())
#                 tasks.append(StinkLevels(self.ss, level).ask())

#             # Wait for tasks to complete and/or timer to expire
#             done, pending = await asyncio.wait(tasks, timeout=self.sleep_timer)

#             for task in pending:
#                 task.cancel()
#                 try:
#                     await task
#                 except asyncio.CancelledError:
#                     pass