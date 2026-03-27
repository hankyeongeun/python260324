import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class BikeProductManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_database()
        self.init_ui()
        self.apply_stylesheet()
        
    def init_database(self):
        """데이터베이스 초기화"""
        try:
            self.conn = sqlite3.connect('bike_products.db')
            self.cursor = self.conn.cursor()
            
            # MyProduct 테이블 생성
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS MyProduct (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f'데이터베이스 초기화 오류: {str(e)}')
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('🚴 자전거용품 관리 시스템')
        self.setGeometry(100, 100, 950, 700)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃 (여백 추가)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)
        
        # ===== 상단: 제목 =====
        title_label = QLabel('📋 자전거용품 정보')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # ===== 입력 영역 =====
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        # 이름 입력
        name_label = QLabel('상품명:')
        name_label.setMinimumWidth(70)
        input_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('상품명을 입력하세요')
        self.name_input.setMinimumHeight(35)
        input_layout.addWidget(self.name_input)
        
        # 가격 입력
        price_label = QLabel('가격:')
        price_label.setMinimumWidth(50)
        input_layout.addWidget(price_label)
        self.price_input = QSpinBox()
        self.price_input.setMaximum(10000000)
        self.price_input.setMinimumHeight(35)
        self.price_input.setMinimumWidth(120)
        input_layout.addWidget(self.price_input)
        
        # 검색 입력
        search_label = QLabel('검색:')
        search_label.setMinimumWidth(50)
        input_layout.addWidget(search_label)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('상품명으로 검색')
        self.search_input.setMinimumHeight(35)
        input_layout.addWidget(self.search_input)
        
        main_layout.addLayout(input_layout)
        
        # ===== 버튼 영역 =====
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        self.insert_btn = QPushButton('➕ 입력')
        self.insert_btn.setMinimumHeight(40)
        self.insert_btn.setMinimumWidth(100)
        self.insert_btn.clicked.connect(self.insert_product)
        button_layout.addWidget(self.insert_btn)
        
        self.update_btn = QPushButton('✏️ 수정')
        self.update_btn.setMinimumHeight(40)
        self.update_btn.setMinimumWidth(100)
        self.update_btn.clicked.connect(self.update_product)
        button_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton('🗑️ 삭제')
        self.delete_btn.setObjectName("delete")
        self.delete_btn.setMinimumHeight(40)
        self.delete_btn.setMinimumWidth(100)
        self.delete_btn.clicked.connect(self.delete_product)
        button_layout.addWidget(self.delete_btn)
        
        self.search_btn = QPushButton('🔍 검색')
        self.search_btn.setMinimumHeight(40)
        self.search_btn.setMinimumWidth(100)
        self.search_btn.clicked.connect(self.search_product)
        button_layout.addWidget(self.search_btn)
        
        self.clear_btn = QPushButton('🔄 초기화')
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.setMinimumWidth(100)
        self.clear_btn.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(button_layout)
        
        # ===== 하단: 테이블 =====
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', '상품명', '가격'])
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(350)
        main_layout.addWidget(self.table)
        
        # 초기 데이터 로드
        self.load_all_products()
    
    def insert_product(self):
        """상품 입력"""
        name = self.name_input.text().strip()
        price = self.price_input.value()
        
        if not name:
            QMessageBox.warning(self, '경고', '상품명을 입력해주세요.')
            return
        
        try:
            self.cursor.execute(
                'INSERT INTO MyProduct (name, price) VALUES (?, ?)',
                (name, price)
            )
            self.conn.commit()
            QMessageBox.information(self, '성공', '상품이 추가되었습니다.')
            self.clear_fields()
            self.load_all_products()
        except sqlite3.Error as e:
            QMessageBox.critical(self, '오류', f'데이터베이스 오류: {str(e)}')
    
    def update_product(self):
        """상품 수정"""
        current_row = self.table.currentRow()
        
        if current_row < 0:
            QMessageBox.warning(self, '경고', '수정할 상품을 선택해주세요.')
            return
        
        product_id = int(self.table.item(current_row, 0).text())
        name = self.name_input.text().strip()
        price = self.price_input.value()
        
        if not name:
            QMessageBox.warning(self, '경고', '상품명을 입력해주세요.')
            return
        
        try:
            self.cursor.execute(
                'UPDATE MyProduct SET name = ?, price = ? WHERE id = ?',
                (name, price, product_id)
            )
            self.conn.commit()
            QMessageBox.information(self, '성공', '상품이 수정되었습니다.')
            self.clear_fields()
            self.load_all_products()
        except sqlite3.Error as e:
            QMessageBox.critical(self, '오류', f'데이터베이스 오류: {str(e)}')
    
    def delete_product(self):
        """상품 삭제"""
        current_row = self.table.currentRow()
        
        if current_row < 0:
            QMessageBox.warning(self, '경고', '삭제할 상품을 선택해주세요.')
            return
        
        product_id = int(self.table.item(current_row, 0).text())
        product_name = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, '확인',
            f'"{product_name}"을(를) 삭제하시겠습니까?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.cursor.execute('DELETE FROM MyProduct WHERE id = ?', (product_id,))
                self.conn.commit()
                QMessageBox.information(self, '성공', '상품이 삭제되었습니다.')
                self.clear_fields()
                self.load_all_products()
            except sqlite3.Error as e:
                QMessageBox.critical(self, '오류', f'데이터베이스 오류: {str(e)}')
    
    def search_product(self):
        """상품 검색"""
        search_term = self.search_input.text().strip()
        
        if not search_term:
            self.load_all_products()
            return
        
        try:
            self.cursor.execute(
                'SELECT * FROM MyProduct WHERE name LIKE ?',
                (f'%{search_term}%',)
            )
            results = self.cursor.fetchall()
            self.display_products(results)
        except sqlite3.Error as e:
            QMessageBox.critical(self, '오류', f'데이터베이스 오류: {str(e)}')
    
    def load_all_products(self):
        """모든 상품 로드"""
        try:
            self.cursor.execute('SELECT * FROM MyProduct ORDER BY id DESC')
            products = self.cursor.fetchall()
            self.display_products(products)
        except sqlite3.Error as e:
            QMessageBox.critical(self, '오류', f'데이터베이스 오류: {str(e)}')
    
    def display_products(self, products):
        """테이블에 상품 표시"""
        self.table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            id_item = QTableWidgetItem(str(product[0]))
            name_item = QTableWidgetItem(product[1])
            price_item = QTableWidgetItem(f'{product[2]:,}원')
            
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            price_item.setFlags(price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, price_item)
        
        # 컬럼 너비 조정
        self.table.resizeColumnsToContents()
    
    def on_table_selection_changed(self):
        """테이블 행 선택 시 입력 필드 채우기"""
        current_row = self.table.currentRow()
        
        if current_row >= 0:
            product_id = int(self.table.item(current_row, 0).text())
            name = self.table.item(current_row, 1).text()
            price_text = self.table.item(current_row, 2).text().replace('원', '').replace(',', '')
            
            self.name_input.setText(name)
            self.price_input.setValue(int(price_text))
    
    def clear_fields(self):
        """입력 필드 초기화"""
        self.name_input.clear()
        self.price_input.setValue(0)
        self.search_input.clear()
        self.table.clearSelection()
    
    def apply_stylesheet(self):
        """QSS 스타일 적용"""
        stylesheet = """
        QMainWindow {
            background-color: #f0f2f5;
        }
        
        QLabel {
            color: #2c3e50;
            font-size: 11px;
            font-weight: 500;
        }
        
        QLineEdit, QSpinBox {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
            color: #2c3e50;
            font-size: 11px;
            selection-background-color: #3498db;
        }
        
        QLineEdit:focus, QSpinBox:focus {
            border: 2px solid #3498db;
            background-color: #ecf0f1;
        }
        
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-size: 11px;
            font-weight: bold;
            min-height: 30px;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
            border: 2px solid #1a5276;
        }
        
        QPushButton:pressed {
            background-color: #1a5276;
            padding: 10px 14px;
        }
        
        QPushButton#delete {
            background-color: #e74c3c;
        }
        
        QPushButton#delete:hover {
            background-color: #c0392b;
        }
        
        QPushButton#delete:pressed {
            background-color: #a93226;
        }
        
        QTableWidget {
            background-color: white;
            alternate-background-color: #ecf0f1;
            gridline-color: #bdc3c7;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
        }
        
        QTableWidget::item {
            padding: 5px;
            border: none;
        }
        
        QTableWidget::item:selected {
            background-color: #3498db;
            color: white;
        }
        
        QTableWidget::item:hover {
            background-color: #d5e8f7;
        }
        
        QHeaderView::section {
            background-color: #34495e;
            color: white;
            padding: 5px;
            border: none;
            font-weight: bold;
        }
        
        QScrollBar:vertical {
            border: 1px solid #bdc3c7;
            background-color: white;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #95a5a6;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #7f8c8d;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        
        QMessageBox {
            background-color: #f0f2f5;
        }
        
        QMessageBox QLabel {
            color: #2c3e50;
        }
        """
        self.setStyleSheet(stylesheet)
    
    def closeEvent(self, event):
        """프로그램 종료 시 DB 연결 해제"""
        self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BikeProductManager()
    window.show()
    sys.exit(app.exec())
