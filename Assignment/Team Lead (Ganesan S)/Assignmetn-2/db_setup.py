
import sqlite3

conn =sqlite3.connect('user_base.db')
print('successfully database opened')

conn.execute(' CREATE TABLE user(firstname TEXT, lastname TEXT, email TEXT, phone TEXT, password TEXT, dob TEXT );')

print("table created")
conn.close()