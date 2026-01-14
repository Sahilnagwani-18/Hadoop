from pyhive import hive

def get_hive_conn():
    return hive.Connection(
        host="master",
        port=10000,
        username="user",
        auth="NONE",           # no password needed
        database="default"
    )

