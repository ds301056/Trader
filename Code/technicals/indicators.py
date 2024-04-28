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
    df[f"ATR_{n}"] = tr.rolling(window=n).mean() # Calculate the Average True Range
    return df # Return the dataframe


def KeltnerChannels(df: pd.DataFrame, n_ema=20, n_atr=10): # Create a function to calculate Keltner Channels
    df['EMA'] = df.mid_c.ewm(span=n_ema, min_periods=n_ema).mean() # Calculate the Exponential Moving Average of the close price
    df = ATR(df, n=n_atr) # Calculate the Average True Range
    c_atr = f"ATR_{n_atr}" # Get the ATR column
    df['KeUp'] = df[c_atr] * 2 + df.EMA # Calculate the upper Keltner Channel
    df['KeLo'] =  df.EMA - df[c_atr] * 2 # Calculate the lower Keltner Channel
    df.drop(c_atr, axis=1, inplace=True) # Drop the ATR column
    return df # Return the dataframe

def RSI(df: pd.DataFrame, n=14): # Create a function to calculate the Relative Strength Index
    alpha = 1.0 / n # Calculate the alpha value
    gains = df.mid_c.diff() # Calculate the gains

    wins = pd.Series([ x if x >= 0 else 0.0 for x in gains], name="wins") # Calculate the wins
    losses =pd.Series([ x * -1 if x < 0 else 0.0 for x in gains], name="losses") # Calculate the losses

    wins_rma = wins.ewm(min_periods=n, alpha=alpha).mean() # Calculate the wins RMA
    losses_rma = losses.ewm(min_periods=n, alpha=alpha).mean() # Calculate the losses RMA

    rs = wins_rma / losses_rma # Calculate the Relative Strength

    df[f"RSI_{n}"] = 100 - (100 / (1.0 + rs)) # Calculate the Relative Strength Index
    return df # Return the dataframe

def MACD(df: pd.DataFrame, n_slow = 26, n_fast = 12, n_signal = 9): # Create a function to calculate the Moving Average Convergence Divergence
    ema_long = df.mid_c.ewm(min_periods=n_slow, span=n_slow).mean() # Calculate the long term Exponential Moving Average
    ema_short = df.mid_c.ewm(min_periods=n_fast, span=n_fast).mean() # Calculate the short term Exponential Moving Average

    df['MACD'] = ema_short - ema_long # Calculate the Moving Average Convergence Divergence
    df['SIGNAL'] = df['MACD'].ewm(min_periods=n_signal, span=n_signal).mean() # Calculate the Signal Line
    df['HIST'] = df.MACD - df.SIGNAL # Calculate the HistogramSS

    return df # Return the dataframe







