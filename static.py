import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Configure style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Data for perfect scores (10 marks) by subject
data = {
    'mon_hoc': ['Địa lý', 'Vật lý', 'Lịch sử', 'Hóa học', 'Toán', 'Tiếng Anh', 
                'CN Nông nghiệp', 'Sinh học', 'Tin học', 'Ngữ Văn'],
    'so_bai_diem_10': [6907, 3929, 1518, 625, 513, 141, 101, 82, 60, 0]
}

df = pd.DataFrame(data)

# Summary statistics

total_perfect_scores = df['so_bai_diem_10'].sum()
top_subject = df.loc[df['so_bai_diem_10'].idxmax()]
subjects_with_scores = len(df[df['so_bai_diem_10'] > 0])
subjects_without_scores = len(df[df['so_bai_diem_10'] == 0])



# Dữ liệu mẫu cho sentiment analysis (thay thế bằng dữ liệu thật từ JSON)
sentiment_data = {
    'trước khi có kết quả thi thpt': {
        'vui': 120,
        'buồn': 450,
        'đề_khó': 680,
        'trung_tính': 200
    },
    'sau khi có kết quả thi thpt': {
        'vui': 280,
        'buồn': 320,
        'đề_khó': 150,
        'quay_xe': 240,
        'trung_tính': 180
    }
}

# Tạo figure với 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# ==================== BIỂU ĐỒ 1: SỐ BÀI ĐIỂM 10 (BÊN TRÁI) ====================
df_plot = df.sort_values('so_bai_diem_10', ascending=False)

# Create color mapping based on score ranges
def get_color(score):
    if score == 0:
        return '#d32f2f'  # Red for zero
    elif score < 100:
        return '#ff9800'  # Orange for very low
    elif score < 500:
        return '#ffc107'  # Yellow for low
    elif score < 2000:
        return '#4caf50'  # Green for medium
    else:
        return '#2196f3'  # Blue for high

colors_mapped = [get_color(score) for score in df_plot['so_bai_diem_10']]

bars1 = ax1.bar(range(len(df_plot)), df_plot['so_bai_diem_10'], 
               color=colors_mapped, edgecolor='black', linewidth=1.2, alpha=0.8)

ax1.set_title('SỐ BÀI ĐIỂM 10 THEO MÔN HỌC', fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('Môn học', fontsize=12, fontweight='bold', labelpad=-20)
ax1.set_ylabel('Số bài điểm 10', fontsize=12, fontweight='bold', labelpad=-5)

# Customize x-axis
ax1.set_xticks(range(len(df_plot)))
ax1.set_xticklabels(df_plot['mon_hoc'], rotation=45, ha='right', fontsize=10)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars1, df_plot['so_bai_diem_10'])):
    height = bar.get_height()
    if value > 0:
        ax1.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{value:,}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    else:
        ax1.text(bar.get_x() + bar.get_width()/2., 50,
                'KHÔNG CÓ\nĐIỂM 10', ha='center', va='bottom', 
                fontweight='bold', fontsize=8, color='white',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='red', alpha=0.8))

# Add grid
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add legend for color coding
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2196f3', label='Cao (≥2000 bài)'),
    Patch(facecolor='#4caf50', label='Trung bình (500-1999 bài)'),
    Patch(facecolor='#ffc107', label='Thấp (100-499 bài)'),
    Patch(facecolor='#ff9800', label='Rất thấp (1-99 bài)'),
    Patch(facecolor='#d32f2f', label='Không có điểm 10')
]
ax1.legend(handles=legend_elements, loc='upper right', fontsize=9)

# ==================== BIỂU ĐỒ 2: SENTIMENT ANALYSIS (BÊN PHẢI) ====================

# Chuẩn bị dữ liệu cho biểu đồ cột nhóm
periods = list(sentiment_data.keys())
sentiment_types = ['vui', 'buồn', 'đề_khó', 'quay_xe', 'trung_tính']

# Màu sắc cho từng loại sentiment
sentiment_colors = {
    'vui': '#4CAF50',        # Green
    'buồn': '#F44336',       # Red
    'đề_khó': '#FF9800',     # Orange  
    'quay_xe': '#9C27B0',    # Purple
    'trung_tính': '#607D8B'  # Blue Grey
}

# Tính toán vị trí các cột
x = np.arange(len(periods))  # vị trí các nhóm
width = 0.15  # độ rộng của mỗi cột
multiplier = 0

# Vẽ từng loại sentiment
bars_sentiment = []
for sentiment_type in sentiment_types:
    values = []
    for period in periods:
        values.append(sentiment_data[period].get(sentiment_type, 0))
    
    offset = width * multiplier
    bars = ax2.bar(x + offset, values, width, 
                   label=sentiment_type.title(), 
                   color=sentiment_colors[sentiment_type], 
                   alpha=0.8, edgecolor='black', linewidth=0.8)
    bars_sentiment.append(bars)
    
    # Thêm nhãn giá trị lên cột
    for bar, value in zip(bars, values):
        if value > 0:
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
                    f'{value}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    multiplier += 1

# Thiết lập biểu đồ sentiment
ax2.set_title('PHÂN TÍCH SENTIMENT COMMENTS', fontsize=16, fontweight='bold', pad=20)
ax2.set_xlabel('Thời điểm', fontsize=12, fontweight='bold', labelpad=13)
ax2.set_ylabel('Số lượng comments', fontsize=12, fontweight='bold')

# Thiết lập x-axis
ax2.set_xticks(x + width * 2)  # Đặt ở giữa các nhóm cột
ax2.set_xticklabels(['Trước khi có\nkết quả thi THPT', 'Sau khi có\nkết quả thi THPT'], 
                   fontsize=11, ha='center')

# Thêm lưới
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Thêm legend
ax2.legend(loc='upper left', fontsize=10, framealpha=0.9)

# Tính toán và hiển thị thống kê tổng hợp
total_before = sum(sentiment_data['trước khi có kết quả thi thpt'].values())
total_after = sum(sentiment_data['sau khi có kết quả thi thpt'].values())

stats_text_sentiment = f"""THỐNG KÊ SENTIMENT:
Trước: 6 bài và {total_before:,} comments
Sau:   6 bài và {total_after:,} comments  
Tổng:  {total_before + total_after:,} comments"""


ax2.text(0.95, 0.95, stats_text_sentiment, transform=ax2.transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='right',multialignment='left',
         bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.8))

# Điều chỉnh layout
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()

# In thống kê tổng hợp cho cả 2 biểu đồ
print("\n" + "="*80)
print("TỔNG HỢP THỐNG KÊ PHÂN TÍCH THI TỐT NGHIỆP THPT 2025".center(80))
print("="*80)

print(f"\n📊 THỐNG KÊ ĐIỂM 10:")
print(f"   • Tổng số bài điểm 10: {total_perfect_scores:,}")
print(f"   • Môn cao nhất: {top_subject['mon_hoc']} ({top_subject['so_bai_diem_10']:,} bài)")

print(f"\n💬 THỐNG KÊ SENTIMENT:")
print(f"   • Tổng comments phân tích: {total_before + total_after:,}")
print(f"   • Tổng số bài dùng để làm phân tích: 6 bài trước và 6 bài sau kì thi THPT")
print(f"   • Comments trước kết quả: {total_before:,}")
print(f"   • Comments sau kết quả: {total_after:,}")

print(f"\n📈 XU HƯỚNG SENTIMENT:")
for sentiment_type in sentiment_types:
    before_count = sentiment_data['trước khi có kết quả thi thpt'].get(sentiment_type, 0)
    after_count = sentiment_data['sau khi có kết quả thi thpt'].get(sentiment_type, 0)
    if before_count > 0:
        change_percent = ((after_count - before_count) / before_count) * 100
        trend = "📈" if change_percent > 0 else "📉" if change_percent < 0 else "➡️"
        print(f"   • {sentiment_type.title()}: {before_count} → {after_count} ({trend} {change_percent:+.1f}%)")

print("="*80)