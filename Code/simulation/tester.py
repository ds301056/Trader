# Import the pandas library to handle data in a DataFrame format.
import pandas as pd

# Import the timer function from the timeit module to measure the execution time.
from timeit import default_timer as timer


# in example video: 
    #Total Rows 446362
    #df.iterrows() -> 22.1982s
    #iloc[index]   -> 8.0820s
    #ar1[index]    -> 0.5846s
    #items[index]    -> 0.5948s


# Load a DataFrame from a pickle file, which is a binary file format for storing Python objects.
df = pd.read_pickle("./data/GBP_JPY_M5.pkl")



# Print the total number of rows in the DataFrame to understand its size.
print(f"Total Rows:{df.shape[0]}")

# Start timing the operation using iterrows(), a method to iterate over DataFrame rows as (index, Series) pairs.
start = timer()
for index, row in df.iterrows():
    # Perform a calculation on the 'mid_c' column, multiplying by 12.
    val1 = row.mid_c * 12
    # Subtract 14 from the 'mid_h' column.
    val2 = row.mid_h - 14
# Stop the timer and print the time taken for the iterrows() method.
print(f"df.iterrows() -> {(timer()-start):.4f}s")



# Start timing another method using iloc, which allows for integer-location based indexing.
start = timer()
for index in range(df.shape[0]):
    # Access and compute using the iloc indexer for 'mid_c' and 'mid_h'.
    val1 = df.mid_c.iloc[index] * 12
    val2 = df.mid_h.iloc[index] - 14
# Stop the timer and print the time taken for accessing data with iloc[index].
print(f"iloc[index]   -> {(timer()-start):.4f}s")



# Start timing a method using direct access to the underlying arrays of the DataFrame.
start = timer()
# Get the arrays directly from the DataFrame columns.
ar1 = df.mid_c.array
ar2 = df.mid_h.array
for index in range(ar1.shape[0]):
    # Perform operations directly on the arrays.
    val1 = ar1[index] * 12
    val2 = ar2[index] - 14
# Stop the timer and print the time taken for array-based access.
print(f"ar1[index]    -> {(timer()-start):.4f}s")



# Start timing using a list of arrays derived from the DataFrame.
start = timer()
# Create a list containing arrays from two DataFrame columns.
items = [df.mid_c.array, df.mid_h.array]
for index in range(ar1.shape[0]):
    # Access and compute using the list of arrays.
    val1 = items[0][index] * 12
    val2 = items[1][index] - 14
# Stop the timer and print the time taken for the list of arrays method.
print(f"items[index]    -> {(timer()-start):.4f}s")
