import wfdb
import os

DATA_DIR = "data/drivedb"
os.makedirs(DATA_DIR, exist_ok=True)

wfdb.dl_database(
    "drivedb",
    dl_dir=DATA_DIR
)
