from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['bessyii']
collection = db['machines']


@app.route('/api/get_parsed_machine_data', methods=['GET'])
def get_elements():
    elements = list(collection.find({}, {'_id': 0}))  # Exclude _id field
    return jsonify(elements)

if __name__ == '__main__':
    mongodb_uri = "mongodb://localhost:27017/"  
    database_name = "newDb"  
    collection_name = "lattice_collection"  
    
    #for inserting the database uncomment this
    
    app.run(debug=True)
