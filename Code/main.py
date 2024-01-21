from api.oanda_api import OandaApi

if __name__ == "__main__":
  api = OandaApi()
  
  data = api.get_account_summary()
  print(data)  

  