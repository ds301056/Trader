import pandas as pd # Import the pandas library
import xlsxwriter



WIDTHS = {
    'L:L' : 20, # Set the width of column L to 20
    'B:F' : 9 # Set the width of columns B through F to 9
}




def set_widths(pair, writer): # Set the widths of the columns in the Excel file
    worksheet = writer.sheets[pair] # Get the worksheet from the writer
    for k,v in WIDTHS.items(): # For each key-value pair in the WIDTHS dictionary
        worksheet.set_column(k, v) # Set the width of the column to the value    k is range v is value of width




def get_line_chart(book, start_row, end_row, labels_col, data_col, title, sheetname):
    chart = book.add_chart({'type': 'line'}) # Create a line chart
    chart.add_series({ # Add a series to the chart
        'categories' : [sheetname, start_row, labels_col, end_row, labels_col], # Set the categories for the series
        'values' : [sheetname, start_row, data_col, end_row, data_col], # Set the values for the series
        'line' : {'color': 'blue'} # Set the color of the line
    })
    chart.set_title({'name': title}) # Set the title of the chart
    chart.set_legend({'none' : True}) # Set the legend of the chart
    return chart # Return the chart






def add_chart(pair, cross, df,  writer): # Add a chart to the Excel file
    workbook = writer.book # Get the workbook from the writer
    worksheet = writer.sheets[pair] # Get the worksheet from the writer

    chart = get_line_chart(workbook, 1, df.shape[0], 11, 12, f"GAIN_C for {pair} {cross}", pair ) # Create a line chart

    chart.set_size({'x_scale' : 2.5, 'y_scale' : 2.5}) # Set the size of the chart
    worksheet.insert_chart('O1', chart)  # Insert the chart into the worksheet



def add_pair_charts(df_ma_res, df_ma_trades, writer): # Add the pair charts to the Excel file
    cols = ['time', 'GAIN_C'] # Create a list of columns to use for the chart
    df_temp = df_ma_res.drop_duplicates(subset="pair") # Create a temporary dataframe with the unique pairs

    for _, row in df_temp.iterrows():
        dft = df_ma_trades[(df_ma_trades.cross == row.cross)& 
                            (df_ma_trades.pair == row.pair)] # Create a temporary dataframe for the pair
        dft[cols].to_excel( # Save the temporary dataframe to the Excel file
                writer, # Use the writer object to save the dataframe to the Excel file
                sheet_name=row.pair, # Use the pair as the sheet name
                index=False, # Do not include the index in the Excel file
                startrow=0, # Start the chart at row 0
                startcol=11 # Start the chart at column 11
                ) 


        set_widths(row.pair, writer) # Set the widths of the columns in the Excel file
        add_chart(row.pair, row.cross, dft, writer) # Add a chart to the Excel file













def add_pair_sheets(df_ma_res, writer): # Add the pair sheets to the Excel file
    for p in df_ma_res.pair.unique(): # For each unique pair in the pair column of the dataframe
        tdf = df_ma_res[df_ma_res.pair == p] # Create a temporary dataframe for the pair
        tdf.to_excel(writer, sheet_name=p, index=False) # Save the temporary dataframe to the Excel file



def prepare_data(df_ma_res, df_ma_trades): # Prepare the data # pairs alphabetical order gains descending
    df_ma_res.sort_values( # Sort the dataframe by the pair and gain columns
        by=['pair', 'total_gain'],         # Sort by the pair and gain columns
        ascending=[True, False],     # Sort in ascending order by the pair column and descending order by the gain column
        inplace = True)              # Sort the dataframe in place
    df_ma_trades['time'] = [ x.replace (tzinfo=None) for x in df_ma_trades['time'] ] # Remove the timezone information from the time column

def process_data(df_ma_res, df_ma_trades, writer):
    prepare_data(df_ma_res, df_ma_trades) # Prepare the data
    add_pair_sheets(df_ma_res, writer) # Add the pair sheets to the Excel file
    add_pair_charts(df_ma_res, df_ma_trades, writer) # Add the pair charts to the Excel file



def create_excel(df_ma_res, df_ma_trades, granularity):
    filename = f"ma_sim_{granularity}.xlsx" # Create the filename
    writer = pd.ExcelWriter(filename, engine='xlsxwriter') # Create an Excel writer using the XlsxWriter engine


    process_data(
        df_ma_res[df_ma_res["granularity"] == granularity].copy(), # Filter the dataframe by granularity
        df_ma_trades[df_ma_trades["granularity"] == granularity].copy(), 
        writer) # Process the data

    writer.close() # Save the writer


def create_ma_res(granularity):
    df_ma_res = pd.read_pickle("./data/ma_res.pkl") # Load the ma_res.pkl file into a dataframe running from main.py so remove a . from the path
    df_ma_trades = pd.read_pickle("./data/ma_trades.pkl") # Load the ma_trades.pkl file into a dataframe running from main.py so remove a . from the path
    create_excel(df_ma_res, df_ma_trades, granularity) # Run the create_excel function

if __name__ == "__main__":

    df_ma_res  = pd.read_pickle("../data/ma_res.pkl") # Load the ma_res.pkl file into a dataframe
    df_ma_trades = pd.read_pickle("../data/ma_trades.pkl") # Load the ma_trades.pkl file into a dataframe



    create_excel(df_ma_res, df_ma_trades, "H1") # Run the create_excel function
    create_excel(df_ma_res, df_ma_trades, "H4") # Run the create_excel function
