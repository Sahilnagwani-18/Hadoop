from pyhive import hive

conn = hive.Connection(
    host="localhost",
    port=10000,
    username="user",
    auth="NONE"
)

cursor = conn.cursor()
cursor.execute("SHOW DATABASES")
print(cursor.fetchall())

