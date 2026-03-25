import sqlite3
import random

class ProductDB:
    def __init__(self, db_name='MyProduct.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                productID INTEGER PRIMARY KEY AUTOINCREMENT,
                productName TEXT NOT NULL,
                productPrice INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_product(self, name, price):
        self.cursor.execute('INSERT INTO Products (productName, productPrice) VALUES (?, ?)', (name, price))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_product(self, id, name=None, price=None):
        if name and price:
            self.cursor.execute('UPDATE Products SET productName = ?, productPrice = ? WHERE productID = ?', (name, price, id))
        elif name:
            self.cursor.execute('UPDATE Products SET productName = ? WHERE productID = ?', (name, id))
        elif price:
            self.cursor.execute('UPDATE Products SET productPrice = ? WHERE productID = ?', (price, id))
        self.conn.commit()

    def delete_product(self, id):
        self.cursor.execute('DELETE FROM Products WHERE productID = ?', (id,))
        self.conn.commit()

    def select_products(self, limit=None):
        if limit:
            self.cursor.execute('SELECT * FROM Products LIMIT ?', (limit,))
        else:
            self.cursor.execute('SELECT * FROM Products')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# 샘플 데이터 생성
def generate_sample_data(db, num=100000):
    product_names = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Monitor', 'Keyboard', 'Mouse', 'Printer', 'Router', 'Camera']
    data = [(random.choice(product_names) + f' {i+1}', random.randint(100, 10000)) for i in range(num)]
    with db.conn:
        db.cursor.executemany('INSERT INTO Products (productName, productPrice) VALUES (?, ?)', data)

if __name__ == '__main__':
    db = ProductDB()
    generate_sample_data(db, 100000)
    print("Sample data inserted.")
    # 예시 사용
    products = db.select_products(10)
    for p in products:
        print(p)
    db.close()