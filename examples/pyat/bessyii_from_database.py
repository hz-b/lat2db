from lat2db.tools.importers.from_json import factory
import at

from pymongo import MongoClient

# get database
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["bessyii"]
collection = db["machines"]
lattice_in_json_format = collection.find_one(dict(id="8e38b3a9-7833-4594-a5dc-79578bddb385"))

assert lattice_in_json_format
seq = factory(lattice_in_json_format)


acc = at.Lattice(seq)