import pandas as pd # Import the pandas library

def BollingerBands(df: pd.DataFrame, n=20 , s=2): # Create a function to calculate Bollinger Bands
    typical_p = ( df.mid_c + df.mid_h + df.mid_l ) / 3  # Calculate the typical price for the period formula is (high + low + close) / 3
    stddev = typical_p.rolling(window=n).std() # Calculate the standard deviation of the typical price for the period
    df['BB_MA'] = typical_p.rolling(window=n).mean() # Calculate the moving average of the typical price for the period
    df['BB_UP'] = df['BB_MA'] + (stddev * s) # Calculate the upper Bollinger Band
    df['BB_LW'] = df['BB_MA'] - (stddev * s) # Calculate the lower Bollinger Band
    return df # Return the dataframe

def ATR(df: pd.DataFrame, n=14): # Create a function to calculate the Average True Range
    prev_c = df.mid_c.shift(1) # Shift the close price by 1
    tr = df.mid_h - df.mid_l # Calculate the True Range
    tr2 = (df.mid_h - prev_c) # Calculate the True Range
    tr3 = (prev_c - df.mid_l) # Calculate the True Range
    tr = pd.DataFrame({'tr1': tr, 'tr2': tr2, 'tr3': tr3}).max(axis=1) # Calculate the True Range
    df['ATR'] = tr.rolling(window=n).mean() # Calculate the Average True Range
    return df # Return the dataframe


def keltnerChannels(df: pd.DataFrame, n_ema=20, n_atr=10): # Create a function to calculate Keltner Channels
    df['EMA'] = df.mid_c.ewm(span=n_ema, min_periods=n_ema).mean() # Calculate the Exponential Moving Average of the close price
    df = ATR(df, n=n_atr) # Calculate the Average True Range
    df['KeUp'] = df.ATR * 2 + df.EMA # Calculate the upper Keltner Channel
    df['KeLo'] =  df.EMA - df.ATR * 2 # Calculate the lower Keltner Channel
    df.drop('ATR', axis=1, inplace=True) # Drop the ATR column
    return df # Return the dataframe