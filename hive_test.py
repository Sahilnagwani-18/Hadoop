from pyhive import hive

conn = hive.Connection(
    host="localhost",
    port=10000,
    username="user",
    database="default",
    auth="NONE"
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES")
rows = cursor.fetchall()

print("Tables:")
for row in rows:
    print(row)

cursor.close()
conn.close()

