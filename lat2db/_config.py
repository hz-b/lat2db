from configparser import ConfigParser
from importlib.resources import  files

def config(mod_name):
    parser = ConfigParser()
    # check that it read a a file
    _, = parser.read(files(mod_name).joinpath("config.cfg"))
    return parser

def mongodb_url(mod_name):
    cfg = config(mod_name)
    mongodb = cfg["default"]["mongodb"]
    dbsec = cfg[mongodb]
    server = dbsec['server']
    port = dbsec['port']
    return f"mongodb://{server}:{port}"