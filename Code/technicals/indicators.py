import pandas as pd # Import the pandas library

def BollingerBands(df: pd.DataFrame, n=20 , s=2): # Create a function to calculate Bollinger Bands
    typical_p = ( df.mid_c + df.mid_h + df.mid_l ) / 3  # Calculate the typical price for the period formula is (high + low + close) / 3
    stddev = typical_p.rolling(window=n).std() # Calculate the standard deviation of the typical price for the period
    df['BB_MA'] = typical_p.rolling(window=n).mean() # Calculate the moving average of the typical price for the period
    df['BB_UP'] = df['BB_MA'] + (stddev * s) # Calculate the upper Bollinger Band
    df['BB_LW'] = df['BB_MA'] - (stddev * s) # Calculate the lower Bollinger Band
    return df # Return the dataframe

    