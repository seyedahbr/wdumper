import os

basedir = os.path.abspath(os.path.dirname(__file__))

DB_URI = os.getenv("WDUMPER_DB_URI", "mysql+mysqlconnector://root@localhost/wdumper")
DUMPS_PATH = os.getenv("DUMPS_PATH", os.path.join(basedir, "dumpfiles/generated"))
ZENODO_SANDBOX_TOKEN = os.getenv("ZENODO_SANDBOX_TOKEN", "")
ZENODO_TOKEN = os.getenv("ZENODO_TOKEN", "")
