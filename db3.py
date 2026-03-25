import sqlite3
import random

class ProductDB:
    def __init__(self, db_name='MyProduct.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
            productID INTEGER PRIMARY KEY,
            productName TEXT,
            productPrice INTEGER
        )''')
        self.conn.commit()

    def insert(self, productID, productName, productPrice):
        self.cursor.execute('INSERT INTO Products VALUES (?, ?, ?)', (productID, productName, productPrice))
        self.conn.commit()

    def update(self, productID, productName=None, productPrice=None):
        if productName is not None:
            self.cursor.execute('UPDATE Products SET productName = ? WHERE productID = ?', (productName, productID))
        if productPrice is not None:
            self.cursor.execute('UPDATE Products SET productPrice = ? WHERE productID = ?', (productPrice, productID))
        self.conn.commit()

    def delete(self, productID):
        self.cursor.execute('DELETE FROM Products WHERE productID = ?', (productID,))
        self.conn.commit()

    def select(self, productID=None):
        if productID is not None:
            self.cursor.execute('SELECT * FROM Products WHERE productID = ?', (productID,))
            return self.cursor.fetchone()
        else:
            self.cursor.execute('SELECT * FROM Products')
            return self.cursor.fetchall()

    def close(self):
        self.conn.close()

def generate_sample_data(num=100000):
    products = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Monitor', 'Keyboard', 'Mouse', 'Printer', 'Router', 'Camera']
    data = []
    for i in range(1, num + 1):
        name = random.choice(products) + f' Model {i}'
        price = random.randint(100, 10000)
        data.append((i, name, price))
    return data

if __name__ == '__main__':
    db = ProductDB()
    sample_data = generate_sample_data()
    for item in sample_data:
        db.insert(*item)
    print("10만 개의 샘플 데이터가 삽입되었습니다.")
    db.close()