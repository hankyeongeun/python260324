import requests
from bs4 import BeautifulSoup
import openpyxl
import time

# 네이버 코스피200 편입종목 상위 정보 URL
base_url = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    all_data = []
    headers_list = []

    # 1부터 20페이지까지 크롤링
    for page in range(1, 21):
        url = f"{base_url}&page={page}"
        print(f"페이지 {page} 크롤링 중...")

        response = requests.get(url, headers=headers)
        # 네이버 금융은 euc-kr(또는 cp949)로 인코딩되므로 명시적으로 설정
        response.encoding = 'euc-kr'

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'type_1'})

        if table is None:
            print(f"페이지 {page}: 테이블을 찾을 수 없습니다. 다음 페이지로 진행합니다.")
            continue

        # 첫 번째 페이지에서만 헤더 추출
        if page == 1:
            header_row = table.find('tr')
            headers_list = [th.get_text(strip=True) for th in header_row.find_all('th')]

        # 데이터 추출
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if not cols:
                continue
            row = [td.get_text(strip=True).replace('\u200b', '') for td in cols]
            # 빈값 스킵 및 의미 없는 줄 제외
            if len(row) >= 2 and any(row):
                all_data.append(row)

        # 서버 부하 방지를 위한 짧은 딜레이
        time.sleep(0.5)

    if not all_data:
        print('데이터를 찾을 수 없습니다.')
    else:
        print(f'\n총 {len(all_data)}개의 데이터를 수집했습니다.')
        print('코스피200 편입종목상위 결과 (첫 20개 샘플):')
        print('=' * 90)
        for i, row in enumerate(all_data[:20], 1):
            print(f'{i:>2}.', row)

    # Excel 파일로 저장
    excel_file = 'kospi200.xlsx'

    # 워크북 생성
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = '코스피200 편입종목'

    # 헤더 행 추가
    if headers_list:
        ws.append(headers_list)

    # 데이터 행들 추가
    for row in all_data:
        ws.append(row)

    # 파일 저장
    wb.save(excel_file)

    print(f'Excel 파일 저장됨: {excel_file} (총 {len(all_data)}개 행)')

except requests.exceptions.RequestException as e:
    print(f'요청 오류: {e}')
except Exception as e:
    print(f'오류 발생: {e}')


