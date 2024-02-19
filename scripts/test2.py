from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["bessyii"]  # Replace with your actual database name
collection = db["student"]  # Replace with your actual collection name


@app.route('/insert_record', methods=['POST'])
def insert_record():
    if request.method == 'POST':
        # Check Content-Type header
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({"error": "Unsupported Media Type. Please set Content-Type to 'application/json'"}), 415

        try:
            data = request.get_json()
            inserted_record = collection.insert_one(data)
            return jsonify({"message": "Record inserted successfully", "inserted_id": str(inserted_record.inserted_id)}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"message": "This endpoint supports only POST requests"}), 405

if __name__ == '__main__':
    app.run(debug=True)