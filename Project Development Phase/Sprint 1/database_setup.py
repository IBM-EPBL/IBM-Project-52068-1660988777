import sqlite3

conn =sqlite3.connect('inventorymanagement')
print('successfully database opened')

conn.execute("CREATE TABLE register(username varchar(20) NOT NULL,first_name varchar(30) NOT NULL,last_name varchar(30) NOT NULL,mobile int NOT NULL, email varchar(30) NOT NULL,password_1 varchar(50) NOT NULL);")
conn.commit()

print("table created")
conn.close()