import sqlite3

conn =  sqlite3.connect("Sugar.db")
cursor = conn.cursor()


cursor.execute("""CREATE TABLE seq_no (seq)""")
conn.commit()
cursor.execute("""CREATE TABLE blood_stat (seq, user_id, date, time, sugar, insulin, he)""")
conn.commit()


sql = "insert into seq_no values ('0')"
cursor.execute(sql)
conn.commit()

