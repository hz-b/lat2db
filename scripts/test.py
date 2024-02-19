from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string

# Select a database
db_name = "test_db"  # Replace with your actual database name
db = client[db_name]

# Select a collection
collection_name = "student"  # Replace with your actual collection name
collection = db[collection_name]

# Insert a document
document_to_insert = {"name": "John Doe", "age": 30, "city": "New York"}

# Ensure the collection exists (creates it if it doesn't)
db.list_collection_names()
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)

result = collection.insert_one(document_to_insert)
print(f"Inserted document with ID: {result.inserted_id}")

# Query the collection
cursor = collection.find({"age": {"$gte": 25}})
for document in cursor:
    print(document)

# Close the MongoDB connection
client.close()
