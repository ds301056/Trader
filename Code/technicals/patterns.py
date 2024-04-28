import pandas as pd # The pandas library is imported

HANGING_MAN_BODY = 15.0 # 15% of the candlestick
HANGING_MAN_HEIGHT = 75.0 # 75% of the candlestick
SHOOTING_STAR_HEIGHT = 25.0 # 25% of the candlestick
SPINNING_TOP_MIN = 40.0 # 100 - 60
SPINNING_TOP_MAX = 60.0 # 100 - 40
MARUBOZU = 98.0 # 98% of the candlestick
ENGULFING_FACTOR = 1.1 # 110% of the previous candlestick

MORNING_STAR_PREV2_BODY = 90.0 # 90% of the candlestick
MORNING_STAR_PREV_BODY = 10.0 # 10% of the candlestick

TWEEZER_BODY = 15.0 # 15% of the candlestick
TWEEZER_HL = 0.01 # 1% of the candlestick
TWEEZER_TOP_BODY = 40.0 # 100 - 60 
TWEEZER_BOTTOM_BODY = 60.0 # 100 - 40

apply_marubozu = lambda x: x.body_perc > MARUBOZU # Marubozu is a candlestick with no shadow, meaning the open and close are the high and low of the candlestick

def apply_hanging_man(row): 
    if row.body_bottom_perc > HANGING_MAN_HEIGHT: # The bottom of the body is the open or close, depending on the direction of the candlestick
        if row.body_perc < HANGING_MAN_BODY: # The body is the difference between the open and close
            return True # If the body is less than 15% of the candlestick and the bottom is 75% of the candlestick, then it is a hanging man
    return False # is not a hanging man

def apply_shooting_star(row): # The shooting star is the opposite
    if row.body_top_perc < SHOOTING_STAR_HEIGHT: # The top of the body is the open or close, depending on the direction of the candlestick
        if row.body_perc < HANGING_MAN_BODY: # The body is the difference between the open and close
            return True # If the body is less than 15% of the candlestick and the top is 25% of the candlestick, then it is a shooting star
    return False # is not a shooting star

def apply_spinning_top(row): # The spinning top is a candlestick with a small body and long shadows
    if row.body_top_perc < SPINNING_TOP_MAX: # The top of the body is the open or close, depending on the direction of the candlestick
        if row.body_bottom_perc > SPINNING_TOP_MIN: # The bottom of the body is the open or close, depending on the direction of the candlestick
            if row.body_perc < HANGING_MAN_BODY: # The body is the difference between the open and close    
                return True # If the body is less than 15% of the candlestick and the top is 40% and the bottom is 60% of the candlestick, then it is a spinning top
    return False # is not a spinning top

def apply_engulfing(row): # The engulfing pattern is a two candlestick pattern
    if row.direction != row.direction_prev: # The direction of the candlestick is the difference between the open and close
        if row.body_size > row.body_size_prev * ENGULFING_FACTOR: # The body is the difference between the open and close
            return True # If the body is 110% of the previous candlestick, then it is an engulfing pattern
    return False # is not an engulfing pattern

def apply_tweezer_top(row): # The tweezer top is a two candlestick pattern
    if abs(row.body_size_change) < TWEEZER_BODY: # The body is the difference between the open and close
        if row.direction == -1 and row.direction != row.direction_prev: # The direction of the candlestick is the difference between the open and close
            if abs(row.low_change) < TWEEZER_HL and abs(row.high_change) < TWEEZER_HL: # The low and high change are the difference between the low and high
                if row.body_top_perc < TWEEZER_TOP_BODY: # The top of the body is the open or close, depending on the direction of the candlestick
                    return True # If the body is less than 40% of the candlestick, then it is a tweezer top
    return False # is not a tweezer top                

def apply_tweezer_bottom(row): # The tweezer bottom is a two candlestick pattern
    if abs(row.body_size_change) < TWEEZER_BODY: # The body is the difference between the open and close
        if row.direction == 1 and row.direction != row.direction_prev: # The direction of the candlestick is the difference between the open and close
            if abs(row.low_change) < TWEEZER_HL and abs(row.high_change) < TWEEZER_HL: # The low and high change are the difference between the low and high
                if row.body_bottom_perc > TWEEZER_BOTTOM_BODY: # The bottom of the body is the open or close, depending on the direction of the candlestick
                    return True # If the body is less than 60% of the candlestick, then it is a tweezer bottom
    return False # is not a tweezer bottom     


def apply_morning_star(row, direction=1): # The morning star is a three candlestick pattern
    if row.body_perc_prev_2 > MORNING_STAR_PREV2_BODY: # The body is the difference between the open and close
        if row.body_perc_prev < MORNING_STAR_PREV_BODY: # The body is the difference between the open and close
            if row.direction == direction and row.direction_prev_2 != direction: # The direction of the candlestick is the difference between the open and close
                if direction == 1: # The direction of the candlestick is the difference between the open and close
                    if row.mid_c > row.mid_point_prev_2: # The mid point is the middle of the candlestick
                        return True # If the mid point is greater than the previous mid point, then it is a morning star
                else: # The direction of the candlestick is the difference between the open and close
                    if row.mid_c < row.mid_point_prev_2: # The mid point is the middle of the candlestick
                        return True # If the mid point is less than the previous mid point, then it is a morning star
    return False # is not a morning star

def apply_candle_props(df: pd.DataFrame): # The candlestick properties are calculated

    df_an = df.copy() # A copy of the dataframe is created
    direction = df_an.mid_c - df_an.mid_o # The direction of the candlestick is the difference between the open and close
    body_size = abs(direction) # The body is the difference between the open and close
    direction = [1 if x >= 0 else -1 for x in direction] # The direction of the candlestick is the difference between the open and close
    full_range = df_an.mid_h - df_an.mid_l # The full range is the difference between the high and low
    body_perc = (body_size / full_range) * 100 # The body percentage is the body size divided by the full range
    body_lower = df_an[['mid_c','mid_o']].min(axis=1) # The lower part of the body is the open or close, depending on the direction of the candlestick
    body_upper = df_an[['mid_c','mid_o']].max(axis=1) # The upper part of the body is the open or close, depending on the direction of the candlestick
    body_bottom_perc = ((body_lower - df_an.mid_l) / full_range) * 100 # The bottom of the body is the open or close, depending on the direction of the candlestick
    body_top_perc = 100 - ((( df_an.mid_h - body_upper) / full_range) * 100) # The top of the body is the open or close, depending on the direction of the candlestick

    mid_point = full_range / 2 + df_an.mid_l # The mid point is the middle of the candlestick

    low_change = df_an.mid_l.pct_change() * 100 # The low change is the difference between the low and the previous low
    high_change = df_an.mid_h.pct_change() * 100 # The high change is the difference between the high and the previous high
    body_size_change = body_size.pct_change() * 100 # The body size change is the difference between the body size and the previous body size

    df_an['body_lower'] = body_lower # The lower part of the body is the open or close, depending on the direction of the candlestick
    df_an['body_upper'] = body_upper # The upper part of the body is the open or close, depending on the direction of the candlestick
    df_an['body_bottom_perc'] = body_bottom_perc # The bottom of the body is the open or close, depending on the direction of the candlestick
    df_an['body_top_perc'] = body_top_perc # The top of the body is the open or close, depending on the direction of the candlestick
    df_an['body_perc'] = body_perc # The body percentage is the body size divided by the full range
    df_an['direction'] = direction # The direction of the candlestick is the difference between the open and close
    df_an['body_size'] = body_size # The body is the difference between the open and close
    df_an['low_change'] = low_change # The low change is the difference between the low and the previous low
    df_an['high_change'] = high_change # The high change is the difference between the high and the previous high
    df_an['body_size_change'] = body_size_change # The body size change is the difference between the body size and the previous body size
    df_an['mid_point'] = mid_point # The mid point is the middle of the candlestick
    df_an['mid_point_prev_2'] = mid_point.shift(2) # The mid point is the middle of the candlestick
    df_an['body_size_prev'] = df_an.body_size.shift(1) # The body is the difference between the open and close
    df_an['direction_prev'] = df_an.direction.shift(1) # The direction of the candlestick is the difference between the open and close
    df_an['direction_prev_2'] = df_an.direction.shift(2) # The direction of the candlestick is the difference between the open and close
    df_an['body_perc_prev'] = df_an.body_perc.shift(1) # The body percentage is the body size divided by the full range
    df_an['body_perc_prev_2'] = df_an.body_perc.shift(2) # The body percentage is the body size divided by the full range

    return df_an # The dataframe with the candlestick properties is returned

# The candlestick patterns are calculated and added to the dataframe
def set_candle_patterns(df_an: pd.DataFrame): # The candlestick patterns are calculated
    df_an['HANGING_MAN'] = df_an.apply(apply_hanging_man, axis=1) # The hanging man
    df_an['SHOOTING_STAR'] = df_an.apply(apply_shooting_star, axis=1) # The shooting star
    df_an['SPINNING_TOP'] = df_an.apply(apply_spinning_top, axis=1) # The spinning top
    df_an['MARUBOZU'] = df_an.apply(apply_marubozu, axis=1) # The marubozu
    df_an['ENGULFING'] = df_an.apply(apply_engulfing, axis=1) # The engulfing pattern
    df_an['TWEEZER_TOP'] = df_an.apply(apply_tweezer_top, axis=1) # The tweezer top
    df_an['TWEEZER_BOTTOM'] = df_an.apply(apply_tweezer_bottom, axis=1) # The tweezer bottom
    df_an['MORNING_STAR'] = df_an.apply(apply_morning_star, axis=1) # The morning star
    df_an['EVENING_STAR'] = df_an.apply(apply_morning_star, axis=1, direction=-1) # The evening star

def apply_patterns(df: pd.DataFrame): # The candlestick properties and patterns are calculated
    df_an = apply_candle_props(df) # The candlestick properties are calculated
    set_candle_patterns(df_an) # The candlestick patterns are calculated and added to the dataframe
    return df_an # The dataframe with the candlestick properties and patterns is returned