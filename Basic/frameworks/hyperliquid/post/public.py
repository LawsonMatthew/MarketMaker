from frameworks.hyperliquid.endpoints import INFO_ENDPOINT
import requests

"""
Class handling get requests to info endpoint for market data.
Used to initilize items in sharedstate not present in websocket feeds.
"""
class HyperLiquidPublicPost:

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.funding = None
        self.mark_px = None
        self.mid_px = None
        self.day_ntl_vlm = None
        self.sz_decimals = None
        self.parse_info_data()

def fetch_info_data(self):
        endpoint = INFO_ENDPOINT
        headers = {"Content-Type": "application/json"}
        data = {"type": "metaAndAsset" + self.symbol}

        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch info data. Status code: {response.status_code}")
        
def parse_info_data(self):
    info_data = self.fetch_info_data()

    # Implement logic to parse and set class attributes with specific data elements
    self.funding = info_data[1][0]["funding"]
    self.mark_px = info_data[1][0]["markPx"]
    self.mid_px = info_data[1][0]["midPx"]
    self.day_ntl_vlm = info_data[1][0]["dayNtlVlm"]
    self.sz_decimals = info_data[0][0]["szDecimals"]