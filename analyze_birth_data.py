import pandas as pd
import matplotlib.pyplot as plt
import sys

# 한글 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

# matplotlib 한글 폰트 설정 (Windows용)
plt.rc('font', family='Malgun Gothic')  # Windows 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 엑셀 파일 읽기
file_path = '출생아수__합계출산율__자연증가_등_20260327151751.xlsx'
df = pd.read_excel(file_path)

# 데이터 확인
print("원본 데이터:")
print(df.head())
print("\n데이터 정보:")
print(df.info())

# 데이터 클랜징
# 결측치 확인
print("\n결측치 확인:")
print(df.isnull().sum())

# 결측치 없으므로 그대로 사용
df_clean = df

# 데이터 재구성: melt하여 년도별로
df_melted = df_clean.melt(id_vars=['기본항목별'], var_name='년도', value_name='값')

# 출생아 수만 추출
births_df = df_melted[df_melted['기본항목별'] == '출생아수(명)'].copy()
births_df['년도'] = births_df['년도'].str.replace(' p)', '').astype(int)  # '2025 p)' -> 2025

# 합계출산율 추출
fertility_df = df_melted[df_melted['기본항목별'] == '합계출산율(명)'].copy()
fertility_df['년도'] = fertility_df['년도'].str.replace(' p)', '').astype(int)

print("\n출생아 수 데이터:")
print(births_df.head())

# 다각도 분석
# 1. 통계 요약
print("\n출생아 수 통계 요약:")
print(births_df['값'].describe())

# 2. 상관관계: 출생아 수와 합계출산율
merged_df = pd.merge(births_df, fertility_df, on='년도', suffixes=('_출생아', '_출산율'))
correlation = merged_df[['값_출생아', '값_출산율']].corr()
print("\n출생아 수와 합계출산율 상관관계:")
print(correlation)

# 3. 트렌드 분석: 최근 10년 평균
recent = births_df[births_df['년도'] >= 2015]
print("\n2015년 이후 출생아 수 평균:", recent['값'].mean())

# 라인 그래프: 출생아 수를 년도별로
plt.figure(figsize=(12, 6))
plt.plot(births_df['년도'], births_df['값'], marker='o', linestyle='-')
plt.title('년도별 출생아 수 (대한민국)')
plt.xlabel('년도')
plt.ylabel('출생아 수 (명)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('birth_trend.png')  # 그래프 저장
plt.show()