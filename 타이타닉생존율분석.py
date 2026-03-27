import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

# 1. 타이타닉 데이터셋 로드
print("=" * 50)
print("타이타닉호 생존율 분석")
print("=" * 50)

df = sns.load_dataset('titanic')

print("\n[1단계] 원본 데이터 확인")
print(f"전체 데이터 크기: {df.shape}")
print("\n처음 5행:")
print(df.head())

# 2. 데이터 클랜징
print("\n[2단계] 데이터 클랜징")

# 결측치 확인
print("\n결측치 현황:")
missing_data = df.isnull().sum()
print(missing_data[missing_data > 0])

# 분석에 필요한 컬럼만 추출 (sex, survived)
# age 컬럼은 분석에 사용하지 않으므로 제거
df_clean = df[['sex', 'survived']].copy()

# sex 컬럼에 결측치가 없는지 확인
print(f"\nSex 컬럼 결측치: {df_clean['sex'].isnull().sum()}")
print(f"Survived 컬럼 결측치: {df_clean['survived'].isnull().sum()}")

# 데이터 타입 확인
print(f"\nSex 컬럼 고유값: {df_clean['sex'].unique()}")
print(f"Survived 컬럼 고유값: {df_clean['survived'].unique()}")

print(f"\n클랜징 후 데이터 크기: {df_clean.shape}")
print(f"결측치: {df_clean.isnull().sum().sum()}")

# 3. 성별별 생존율 계산
print("\n[3단계] 성별별 생존율 계산")

survival_by_gender = df_clean.groupby('sex')['survived'].agg(['count', 'sum', 'mean'])
survival_by_gender.columns = ['총인원', '생존자', '생존율']
survival_by_gender['생존율(%)'] = survival_by_gender['생존율'] * 100

print("\n생존율 통계:")
print(survival_by_gender)

# 상세 통계
for gender in df_clean['sex'].unique():
    gender_data = df_clean[df_clean['sex'] == gender]
    total = len(gender_data)
    survived = gender_data['survived'].sum()
    rate = (survived / total) * 100
    print(f"\n{gender.upper()}:")
    print(f"  총인원: {total}명")
    print(f"  생존자: {survived}명")
    print(f"  사망자: {total - survived}명")
    print(f"  생존율: {rate:.2f}%")

# 4. 그래프 시각화
print("\n[4단계] 그래프 시각화")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 그래프 1: 성별별 생존율 (막대 그래프)
survival_rates = df_clean.groupby('sex')['survived'].mean() * 100
colors = ['#FF6B6B', '#4ECDC4']  # 빨강(남), 청록(여)
bars = axes[0].bar(survival_rates.index, survival_rates.values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
axes[0].set_ylabel('Survival Rate (%)', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Gender', fontsize=12, fontweight='bold')
axes[0].set_title('Titanic: Survival Rate by Gender', fontsize=14, fontweight='bold')
axes[0].set_ylim(0, 100)
axes[0].grid(axis='y', alpha=0.3)

# 생존율 수치 표시
for bar, rate in zip(bars, survival_rates.values):
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

# 그래프 2: 성별별 생존/사망 인원 (누적 막대 그래프)
survival_counts = df_clean.groupby(['sex', 'survived']).size().unstack()
x_pos = np.arange(len(survival_counts))
width = 0.6

died = survival_counts[0]
survived_count = survival_counts[1]

axes[1].bar(x_pos, died, width, label='Did not survive', color='#E74C3C', alpha=0.7, edgecolor='black', linewidth=1.5)
axes[1].bar(x_pos, survived_count, width, bottom=died, label='Survived', color='#2ECC71', alpha=0.7, edgecolor='black', linewidth=1.5)

axes[1].set_ylabel('Number of People', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Gender', fontsize=12, fontweight='bold')
axes[1].set_title('Titanic: Survival Count by Gender', fontsize=14, fontweight='bold')
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(survival_counts.index)
axes[1].legend(fontsize=11)
axes[1].grid(axis='y', alpha=0.3)

# 인원 수치 표시
for i, (d, s) in enumerate(zip(died, survived_count)):
    axes[1].text(i, d/2, f'{int(d)}', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    axes[1].text(i, d + s/2, f'{int(s)}', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

plt.tight_layout()
plt.show()

print("\n분석 완료!")
