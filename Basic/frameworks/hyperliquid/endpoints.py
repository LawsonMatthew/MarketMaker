from dataclasses import dataclass

@dataclass
class BaseEndpoints:
    MAINNET = "https://api.hyperliquid.xyz"
    TESTNET = "https://api.hyperliquid-testnet.xyz"

@dataclass
class WSEndpoints:
    COMBINED_STREAM = "wss://api.hyperliquid.xyz/ws"

#May need to add more of these for later, although all use either /info or /exchange endpoints
@dataclass
class PrivatePostLinks:
    CREATE_ORDER = "/exchange"
    CANCEL_ORDER = "/exchange"

@dataclass 
class PublicPostLinks:
    INFO_ENDPOINT = "https://api.hyperliquid.xyz/info"