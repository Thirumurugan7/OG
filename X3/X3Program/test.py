from pymongo import MongoClient

# Define the data to be stored
data_list = [
    {"address": "Address 1", "text": "Text 1"},
    {"address": "Address 2", "text": "Text 2"},
]

# Connect to MongoDB
client = MongoClient('mongodb+srv://nagi:nagi@cluster0.ohv5gsc.mongodb.net/nagidb')

# Select the database and collection
db = client['mydatabase']  # Replace 'mydatabase' with your database name
collection = db['mycollection']  # Replace 'mycollection' with your collection name

# Insert the data into the collection
result = collection.insert_many(data_list)

# Print the result (optional)
print(f"Data inserted with ids {result.inserted_ids}")

# Close the connection
client.close()
