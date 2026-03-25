#db2.py
import sqlite3
#r: row string notating
con = sqlite3.connect(r"c:\work\sample2.db")

cur = con.cursor()

cur.execute("create table PhoneBook (Name text, PhoneNum text);")
cur.execute("insert into PhoneBook values('홍길동','010-1234-5678');")

name="전우치"
phone="010-9876-5432"
cur.execute("insert into PhoneBook values(?,?);",(name,phone))

#다중데이터 입력
datalist=(('김철수','010-1111-2222'),('이영희','010-3333-4444'))
cur.executemany("insert into PhoneBook values(?,?);", datalist) 

for row in cur.execute("select * from PhoneBook;"):
    print(row)

#작업완료
con.commit()

#연결종료
con.close()
