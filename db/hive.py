from pyhive import hive

def hive_cursor():
    conn = hive.Connection(
        host="localhost",
        port=10000,
        username="hadoop",
        database="default"
    )
    return conn.cursor()

