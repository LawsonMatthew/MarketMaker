from frameworks.sharedstate import SharedState

#Features class will help generate skew which when passed to quote generator will help generate quote prices/quantites
#NOT NECESSARY YET FOR 1 quote/side basic implementation
#class Features:

class BasicAdding:

    def __init__(self,ss: SharedState) -> None:
        self.ss = ss
    
    def generate_prices(self): 
        bid_price = 
        ask_price = 

    def generate_sizes(self):
        bid_size = 
        ask_size = 

    def generate_quotes(self):
        print("Pass quotes to order management system.")