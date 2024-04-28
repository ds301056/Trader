API_KEY = "950e89e18324a1decd3d88f4cc43a085-5f59d5913e0f487ebe5eec4cb06b20c1"
ACCOUNT_ID = "101-001-27981277-001" 
OANDA_URL = "https://api-fxpractice.oanda.com/v3"


SECURE_HEADER = {
    "Authorization": f"Bearer {API_KEY}",  # API key for authorization
    "Content-Type": "application/json"  # Data format for requests and responses
}



SELL = -1 # Constants for selling and buying
BUY = 1 
NONE = 0