from configparser import ConfigParser
from importlib.resources import  files
from urllib.parse import quote_plus
import logging
import os

logger = logging.getLogger('lat2db')


def config(mod_name):
    parser = ConfigParser()
    # check that it read a a file
    _, = parser.read(files(mod_name).joinpath("config.cfg"))
    return parser

def mongodb_url_from_config(mod_name):
    cfg = config(mod_name)
    mongodb = cfg["default"]["mongodb"]
    dbsec = cfg[mongodb]
    server = dbsec['server']
    port = dbsec['port']
    try:
        username = dbsec['username']
    except KeyError:
        username = None   # Add username from config
    try:
        password = dbsec['password']
    except KeyError:
        password = None
    db_name = dbsec['database_name']
    if(username):
        # Encode username and password for inclusion in URL
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)
        return f"mongodb://{encoded_username}:{encoded_password}@{server}:{port}/{db_name}"
    else: return f"mongodb://{server}:{port}/{db_name}"

def mongodb_url(mod_name):
    default_url = mongodb_url_from_config(mod_name)
    try:
        return os.environ["MONGODB_URL"]
    except KeyError:
        txt = f'Environment variable MONGODB_URL is not defined, using default: {default_url}'
        print(txt)
        logger.info(txt)
