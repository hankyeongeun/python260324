import sys
import requests
from bs4 import BeautifulSoup
import openpyxl
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel,
                             QTextEdit, QFileDialog, QMessageBox, QProgressBar)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QFont

# 크롤링 작업을 위한 스레드 클래스
class CrawlingThread(QThread):
    progress = pyqtSignal(str)
    data_updated = pyqtSignal(list, list)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, max_pages=20):
        super().__init__()
        self.max_pages = max_pages
        self.all_data = []
        self.headers_list = []

    def run(self):
        try:
            base_url = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            self.all_data = []
            self.headers_list = []

            # 1부터 최대 페이지까지 크롤링
            for page in range(1, self.max_pages + 1):
                url = f"{base_url}&page={page}"
                self.progress.emit(f"페이지 {page}/{self.max_pages} 크롤링 중...")

                response = requests.get(url, headers=headers, timeout=10)
                response.encoding = 'euc-kr'

                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table', {'class': 'type_1'})

                if table is None:
                    self.progress.emit(f"페이지 {page}: 테이블을 찾을 수 없습니다.")
                    continue

                # 첫 번째 페이지에서만 헤더 추출
                if page == 1:
                    header_row = table.find('tr')
                    self.headers_list = [th.get_text(strip=True) for th in header_row.find_all('th')]

                # 데이터 추출
                for tr in table.find_all('tr')[1:]:
                    cols = tr.find_all('td')
                    if not cols:
                        continue
                    row = [td.get_text(strip=True).replace('\u200b', '') for td in cols]
                    if len(row) >= 2 and any(row):
                        self.all_data.append(row)

                time.sleep(0.5)

            if not self.all_data:
                self.error.emit('데이터를 찾을 수 없습니다.')
            else:
                self.progress.emit(f'총 {len(self.all_data)}개의 데이터를 수집했습니다.')
                self.data_updated.emit(self.headers_list, self.all_data)

        except requests.exceptions.RequestException as e:
            self.error.emit(f'요청 오류: {str(e)}')
        except Exception as e:
            self.error.emit(f'오류 발생: {str(e)}')
        finally:
            self.finished.emit()


# 메인 윈도우 클래스
class Kospi200GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.crawling_thread = None
        self.all_data = []
        self.headers_list = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('네이버 코스피200 편입종목 크롤러')
        self.setGeometry(100, 100, 1000, 700)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout()

        # 상단: 버튼 영역
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton('크롤링 시작')
        self.start_btn.clicked.connect(self.start_crawling)
        button_layout.addWidget(self.start_btn)

        self.save_btn = QPushButton('엑셀로 저장')
        self.save_btn.clicked.connect(self.save_excel)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)

        self.clear_btn = QPushButton('초기화')
        self.clear_btn.clicked.connect(self.clear_data)
        button_layout.addWidget(self.clear_btn)

        main_layout.addLayout(button_layout)

        # 진행률 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # 상태 라벨
        self.status_label = QLabel('준비 완료')
        font = QFont()
        font.setPointSize(10)
        self.status_label.setFont(font)
        main_layout.addWidget(self.status_label)

        # 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        main_layout.addWidget(self.table)

        # 하단: 로그 영역
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        main_layout.addWidget(QLabel('로그:'))
        main_layout.addWidget(self.log_text)

        central_widget.setLayout(main_layout)

    def start_crawling(self):
        if self.crawling_thread and self.crawling_thread.isRunning():
            QMessageBox.warning(self, '경고', '크롤링이 진행 중입니다.')
            return

        self.start_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        self.table.setRowCount(0)
        self.log_text.append('크롤링 시작...')

        self.crawling_thread = CrawlingThread(max_pages=20)
        self.crawling_thread.progress.connect(self.update_status)
        self.crawling_thread.data_updated.connect(self.display_data)
        self.crawling_thread.error.connect(self.show_error)
        self.crawling_thread.finished.connect(self.crawling_finished)
        self.crawling_thread.start()

    def update_status(self, message):
        self.status_label.setText(message)
        self.log_text.append(message)

    def display_data(self, headers, data):
        self.all_data = data
        self.headers_list = headers

        # 테이블 설정
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))

        # 데이터 입력
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                self.table.setItem(row_idx, col_idx, item)

        # 컬럼 너비 자동 조정
        self.table.resizeColumnsToContents()

        self.save_btn.setEnabled(True)

    def save_excel(self):
        if not self.all_data:
            QMessageBox.warning(self, '경고', '저장할 데이터가 없습니다.')
            return

        # 파일 저장 대화상자
        file_path, _ = QFileDialog.getSaveFileName(
            self, '파일 저장', 'kospi200.xlsx', 'Excel Files (*.xlsx)'
        )

        if not file_path:
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = '코스피200 편입종목'

            # 헤더 행 추가
            if self.headers_list:
                ws.append(self.headers_list)

            # 데이터 행 추가
            for row in self.all_data:
                ws.append(row)

            wb.save(file_path)
            QMessageBox.information(self, '성공', f'Excel 파일이 저장되었습니다.\n경로: {file_path}')
            self.log_text.append(f'Excel 파일 저장됨: {file_path} (총 {len(self.all_data)}개 행)')

        except Exception as e:
            QMessageBox.critical(self, '오류', f'파일 저장 중 오류 발생:\n{str(e)}')

    def clear_data(self):
        self.all_data = []
        self.headers_list = []
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.log_text.clear()
        self.status_label.setText('준비 완료')
        self.save_btn.setEnabled(False)
        self.log_text.append('데이터가 초기화되었습니다.')

    def show_error(self, error_message):
        self.log_text.append(f'❌ 오류: {error_message}')
        QMessageBox.critical(self, '오류', error_message)

    def crawling_finished(self):
        self.start_btn.setEnabled(True)
        self.progress_bar.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Kospi200GUI()
    window.show()
    sys.exit(app.exec())


