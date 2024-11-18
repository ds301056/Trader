# Forex - Trading Bot (built using python)

**Currently depolyed at 
https://forex.devhorizon.io/ **

 v1-Dash-Deployment
# Data comes from OANDA API

# Writes data to pkl's for each currency conversion
# then consolidates all pkl's into an excel sheet for advanced data analysis
![Excell](https://github.com/user-attachments/assets/a3692d15-4493-4f38-8289-c5b2e00387c1)



# ---------------------------------------------

# to Start the backend server:

# 1. get into python venv: F:\GitHub\Trader\Code> .\venv\Scripts\Activate

# 2. Collect data if needed: python main.py

# 3. start the server we built using python server.py

# -----------------------------------------------------

# to view / create the dashboard

# 1. navigate to: F:\GitHub\Trader\Code\forex-dash>

# 2. run: npm start

# ----------------------------------------------



# check the setup.bat file 
run with .\setup.bat





 main

# ##### if data is to be changed

# check the setup.bat file

run with .\setup.bat

# The stocks and data are from Oanda

@ developer.oanda.com
# educational account - nonprofit 

    Oanda api:
    950e89e18324a1decd3d88f4cc43a085-5f59d5913e0f487ebe5eec4cb06b20c1

    account number
    101-001-27981277-001

# Requirements

- check the requirements.txt

- generate the requirements.txt from installed packages: pip freeze > requirements.txt
  -install requirements.txt: pip install -r requirements.txt

We will need python for this application
can use "python3 -V" to get version or "python3" to install
python. 3.10 + required.

Setting up the python virtual environment:

1.  "python -m venv venv" <!--create it by typing in the terminal ->
2.  "venv/scripts/activate" <!--run the script-->
3.  "pip install pillow"
4.  "venv/scripts/deactivate" <!--run the script to deactivate the virtual environment-->

in the project Code folder: <!--"cd code"--> 5. "pip install wheel" 6. "pip install pandas jupyter" 7. "pip install jupyterthemes" 8. "pip install requests" 9. "pip install plotly"
10."jt -t onedork -f roboto -cellw 95%" <!--chosen theme of jupyter, cell width 95%  -->

11."jupyter notebook" <!--run the notebook server->

**PS Pandas has changed the group by to include more than numerics,
so we will use** groupby(stuff...).sum(numeric_only=true)

1. generate the pkl's for each currency with:

   api = OandaApi()
   instrumentCollection.LoadInstruments("./data")
   run_collection(instrumentCollection, api)

2. \*\* Delete the ma res trades and ma res pkl before generating the spreadsheets with:

   run_ma_sim() # Run the moving average simulation

   (if not deleted the spreadsheets will be wack)
