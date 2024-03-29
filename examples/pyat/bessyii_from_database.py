import at
from lat2db.tools.factories.pyat import factory
from pymongo import MongoClient

# get database
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["bessyii"]
collection = db["machines"]
lattice_in_json_format = collection.find_one()

seq = factory(lattice_in_json_format)

ring = at.Lattice(seq, name='bessy2', periodicity=1, energy=1.7e9)
if True:
    # set up of calculation choice
    ring.enable_6d()  # Should 6D be default?
    # Set main cavity phases
    ring.set_cavity_phase(cavpts='CAV*')
orbit = ring.find_orbit(at.All)
twiss = ring.get_optics(at.All)
