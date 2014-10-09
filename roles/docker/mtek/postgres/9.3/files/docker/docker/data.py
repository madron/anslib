import os

data = dict(
    WAL_KEEP_SEGMENTS=os.getenv('WAL_KEEP_SEGMENTS', 0),
    MASTER_SERVER = os.getenv('WAL_KEEP_SEGMENTS', None),
)
