from pymongo import MongoClient, errors # Import the MongoClient and errors classes from the pymongo module

from constants.defs import MONGO_CONN_STR # Import the MONGO_CONN_STR constant from the defs.py file

class DataDB: # Define the DataDB class

  SAMPLE_COLL = "forex_sample" # Define the name of the sample collection
  CALENDAR_COLL = "forex_calendar" # Define the name of the calendar collection
  INSTRUMENTS_COLL = "forex_instruments" # Define the name of the instruments collection

  

  def __init__(self):
    self.client = MongoClient(MONGO_CONN_STR) # Connect to the database
    self.db = self.client["forex_learning"] # Connect to the forex_learning database



  def test_connection(self): # Test the connection to the database
    print(self.db.list_collection_names()) # Print the names of the collections in the database


  def delete_many(self, collection, **kwargs): # **kwargs is a dictionary of arguments
    try:
      _ = self.db[collection].delete_many(kwargs) # Delete the documents in the collection that match the arguments
    except errors.InvalidOperation as error: # If there is an error
      print("delete_many error", error) # Print the error




  def add_one(self, collection, ob): # ob is a dictionary
    try:
      _ = self.db[collection].insert_one(ob) # Insert the dictionary into the collection
    except errors.InvalidOperation as error: # If there is an error
      print("add_one error", error) # Print the error



  def add_many(self, collection, list_ob): # list_ob is a list of dictionaries
    try:
      _ = self.db[collection].insert_many(list_ob) # Insert the list of dictionaries into the collection
    except errors.InvalidOperation as error: # If there is an error
      print("add_many error", error) # Print the error
      

  def query_all(self, collection, **kwargs): # **kwargs is a dictionary of arguments
    try:
      data = [] # Create an empty list
      r = self.db[collection].find(kwargs, {'_id':0}) # Find all the documents in the collection
      for item in r: # For each document in the collection
        data.append(item) # Append the document to the data list
      return data # Return the data list
    except errors.InvalidOperation as error: # If there is an error
      print("query_all error", error) # Print the error


  def query_single(self, collection, **kwargs): # **kwargs is a dictionary of arguments
    try: # Try the following:
      r = self.db[collection].find_one(kwargs, {'_id':0}) # Find the first document in the collection
      return r # Return the document
    except errors.InvalidOperation as error: # If there is an error
      print("query_single error", error) # Print the error


  def query_distinct(self, collection, key): # key is a string
    try: # Try the following:
      r = self.db[collection].distinct(key) # Find the distinct values of the key in the collection
      return r # Return the values
    except errors.InvalidOperation as error: # If there is an error
      print("query_distinct error", error)