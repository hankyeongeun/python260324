#db1.py
import sqlite3

con = sqlite3.connect(':memory:')

cur = con.cursor()

cur.execute("create table PhoneBook (Name text, PhoneNum text);")
cur.execute("insert into PhoneBook values('홍길동','010-1234-5678');")

name="전우치"
phone="010-9876-5432"
cur.execute("insert into PhoneBook values(?,?);",(name,phone))

datalist=(('김철수','010-1111-2222'),('이영희','010-3333-4444'))
cur.executemany("insert into PhoneBook values(?,?);", datalist) 

# for row in cur.execute("select * from PhoneBook;"):
#     print(row)
cur.execute("select * from PhoneBook;")
print("---fetchone()---")
print(cur.fetchone())
print("---fetchmany(2)---")
print(cur.fetchmany(2))
print("---fechall()---")
cur.execute("select * from PhoneBook;")
print(cur.fetchall())


con.close()
