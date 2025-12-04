"""
Script 2: Thống kê chi tiết theo từng bài viết
Input: data_reclassified.json
Output: statistics_by_post.json, education_statistics.png
Chỉ xử lý 3 loại: Type 2, 3, 4
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from typing import Dict, List

# ========================================
# CONFIGURATION
# ========================================

# Chỉ có 3 loại
TYPE_LABELS = {
    2: "Đồng tình",
    3: "Phản đối", 
    4: "Góp ý"
}

TYPE_LABELS_FULL = {
    2: "Đồng tình (Ủng hộ bỏ học bạ, ủng hộ thi)",
    3: "Phản đối (Muốn giữ học bạ, chống bỏ)",
    4: "Góp ý (Đề xuất giải pháp, trung lập)"
}

# ========================================
# STATISTICAL ANALYSIS
# ========================================

class EducationStatistics:
    """Thống kê chi tiết theo từng bài viết - chỉ 3 loại"""
    
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.data = None
        self.df = None
        
    def load_data(self):
        """Load dữ liệu và lọc chỉ lấy type 2, 3, 4"""
        print("📂 Loading data from:", self.input_file)
        with open(self.input_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Chuyển sang DataFrame và lọc chỉ lấy type 2, 3, 4
        self.df = pd.DataFrame(self.data)
        original_count = len(self.df)
        self.df = self.df[self.df['type'].isin([2, 3, 4])].copy()
        filtered_count = len(self.df)
        
        print(f"✅ Loaded {original_count} comments")
        print(f"✅ Filtered to {filtered_count} comments (Type 2, 3, 4 only)")
        print(f"📊 Columns: {list(self.df.columns)}")
        
    def calculate_post_statistics(self) -> List[Dict]:
        """Tính thống kê theo từng bài viết"""
        print("\n🔢 Calculating statistics by post...")
        
        post_stats = []
        
        for post_title in self.df['post_title'].unique():
            post_data = self.df[self.df['post_title'] == post_title]
            
            stats = {
                'post_title': post_title,
                'total_comments': len(post_data),
                'total_likes': int(post_data['likes'].sum()),
                'avg_likes': round(post_data['likes'].mean(), 2),
                'median_likes': int(post_data['likes'].median()),
                'max_likes': int(post_data['likes'].max()),
                'min_likes': int(post_data['likes'].min())
            }
            
            # Type distribution
            type_counts = post_data['type'].value_counts().to_dict()
            stats['type_distribution'] = {
                'Đồng tình (Type 2)': type_counts.get(2, 0),
                'Phản đối (Type 3)': type_counts.get(3, 0),
                'Góp ý (Type 4)': type_counts.get(4, 0)
            }
            
            # Type percentages
            total = len(post_data)
            stats['type_percentages'] = {
                'Đồng tình (Type 2) (%)': round(type_counts.get(2, 0) / total * 100, 2),
                'Phản đối (Type 3) (%)': round(type_counts.get(3, 0) / total * 100, 2),
                'Góp ý (Type 4) (%)': round(type_counts.get(4, 0) / total * 100, 2)
            }
            
            # Average likes by type
            stats['avg_likes_by_type'] = {}
            for type_id in [2, 3, 4]:
                type_data = post_data[post_data['type'] == type_id]
                if len(type_data) > 0:
                    stats['avg_likes_by_type'][TYPE_LABELS[type_id]] = round(type_data['likes'].mean(), 2)
                else:
                    stats['avg_likes_by_type'][TYPE_LABELS[type_id]] = 0
            
            # Top 3 comments
            top_comments = post_data.nlargest(3, 'likes')[['author', 'likes', 'text', 'type']].to_dict('records')
            stats['top_3_comments'] = [
                {
                    'author': c['author'],
                    'likes': int(c['likes']),
                    'text': c['text'][:100] + ('...' if len(c['text']) > 100 else ''),
                    'type': TYPE_LABELS[c['type']]
                }
                for c in top_comments
            ]
            
            post_stats.append(stats)
        
        # Sort by total comments
        post_stats.sort(key=lambda x: x['total_comments'], reverse=True)
        
        print(f"✅ Calculated statistics for {len(post_stats)} posts")
        return post_stats
    
    def calculate_overall_statistics(self) -> Dict:
        """Tính thống kê tổng thể"""
        print("\n📊 Calculating overall statistics...")
        
        report = {
            'total_comments': len(self.df),
            'total_likes': int(self.df['likes'].sum()),
            'avg_likes': round(self.df['likes'].mean(), 2),
            'median_likes': int(self.df['likes'].median()),
            'total_posts': self.df['post_title'].nunique(),
            'total_authors': self.df['author'].nunique()
        }
        
        # Overall type distribution
        overall_type_counts = self.df['type'].value_counts().to_dict()
        report['type_distribution'] = {
            'Đồng tình (Type 2)': overall_type_counts.get(2, 0),
            'Phản đối (Type 3)': overall_type_counts.get(3, 0),
            'Góp ý (Type 4)': overall_type_counts.get(4, 0)
        }
        
        # Type percentages
        total = len(self.df)
        report['type_percentages'] = {
            'Đồng tình (Type 2) (%)': round(overall_type_counts.get(2, 0) / total * 100, 2),
            'Phản đối (Type 3) (%)': round(overall_type_counts.get(3, 0) / total * 100, 2),
            'Góp ý (Type 4) (%)': round(overall_type_counts.get(4, 0) / total * 100, 2)
        }
        
        # Average likes by type
        report['avg_likes_by_type'] = {}
        for type_id in [2, 3, 4]:
            type_data = self.df[self.df['type'] == type_id]
            if len(type_data) > 0:
                report['avg_likes_by_type'][TYPE_LABELS[type_id]] = round(type_data['likes'].mean(), 2)
            else:
                report['avg_likes_by_type'][TYPE_LABELS[type_id]] = 0
        
        return report
    
    def generate_visualizations(self, post_stats: List[Dict]):
        """Tạo các biểu đồ thống kê"""
        print("\n📈 Generating visualizations...")
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 12))
        
        # Color palette cho 3 types
        colors = {
            2: '#2ecc71',  # Green for Support
            3: '#e74c3c',  # Red for Oppose
            4: '#f39c12'   # Orange for Suggest
        }
        
        # 1. Comments per Post
        ax1 = plt.subplot(2, 3, 1)
        post_titles_short = [p['post_title'][:40] + '...' for p in post_stats]
        comment_counts = [p['total_comments'] for p in post_stats]
        ax1.barh(post_titles_short, comment_counts, color='skyblue')
        ax1.set_xlabel('Số lượng comments', fontsize=12, fontweight='bold')
        ax1.set_title('📊 Số lượng comments theo bài viết', fontsize=14, fontweight='bold')
        ax1.invert_yaxis()
        
        # 2. Total Likes per Post
        ax2 = plt.subplot(2, 3, 2)
        total_likes = [p['total_likes'] for p in post_stats]
        ax2.barh(post_titles_short, total_likes, color='lightcoral')
        ax2.set_xlabel('Tổng likes', fontsize=12, fontweight='bold')
        ax2.set_title('❤️ Tổng likes theo bài viết', fontsize=14, fontweight='bold')
        ax2.invert_yaxis()
        
        # 3. Type Distribution (Overall)
        ax3 = plt.subplot(2, 3, 3)
        overall_type_counts = self.df['type'].value_counts().to_dict()
        type_labels = [TYPE_LABELS[t] for t in [2, 3, 4]]
        type_counts = [overall_type_counts.get(t, 0) for t in [2, 3, 4]]
        type_colors = [colors[t] for t in [2, 3, 4]]
        
        wedges, texts, autotexts = ax3.pie(
            type_counts, 
            labels=type_labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=type_colors
        )
        ax3.set_title('🎯 Phân bố loại comment (Tổng thể)', fontsize=14, fontweight='bold')
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # 4. Average Likes by Type (Box Plot)
        ax4 = plt.subplot(2, 3, 4)
        type_labels_full = [TYPE_LABELS[t] for t in self.df['type']]
        self.df['type_label'] = type_labels_full
        
        box_data = [self.df[self.df['type'] == t]['likes'].values for t in [2, 3, 4]]
        bp = ax4.boxplot(box_data, labels=[TYPE_LABELS[t] for t in [2, 3, 4]], patch_artist=True)
        
        for patch, type_id in zip(bp['boxes'], [2, 3, 4]):
            patch.set_facecolor(colors[type_id])
        
        ax4.set_ylabel('Số likes', fontsize=12, fontweight='bold')
        ax4.set_title('📦 Phân bố likes theo loại comment', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        # 5. Type Distribution by Post (Stacked Bar)
        ax5 = plt.subplot(2, 3, 5)
        
        type_2_counts = [p['type_distribution']['Đồng tình (Type 2)'] for p in post_stats]
        type_3_counts = [p['type_distribution']['Phản đối (Type 3)'] for p in post_stats]
        type_4_counts = [p['type_distribution']['Góp ý (Type 4)'] for p in post_stats]
        
        x = range(len(post_stats))
        ax5.barh(x, type_2_counts, color=colors[2], label='Đồng tình')
        ax5.barh(x, type_3_counts, left=type_2_counts, color=colors[3], label='Phản đối')
        ax5.barh(x, type_4_counts, left=[t2 + t3 for t2, t3 in zip(type_2_counts, type_3_counts)], 
                color=colors[4], label='Góp ý')
        
        ax5.set_yticks(x)
        ax5.set_yticklabels(post_titles_short)
        ax5.set_xlabel('Số lượng comments', fontsize=12, fontweight='bold')
        ax5.set_title('📊 Phân bố loại comment theo bài viết', fontsize=14, fontweight='bold')
        ax5.legend()
        ax5.invert_yaxis()
        
        # 6. Top Authors by Total Likes
        ax6 = plt.subplot(2, 3, 6)
        author_likes = self.df.groupby('author')['likes'].sum().sort_values(ascending=False).head(10)
        ax6.barh(author_likes.index, author_likes.values, color='mediumpurple')
        ax6.set_xlabel('Tổng likes', fontsize=12, fontweight='bold')
        ax6.set_title(' Top 10 tác giả có nhiều likes nhất', fontsize=14, fontweight='bold')
        ax6.invert_yaxis()
        
        plt.tight_layout()
        plt.savefig('education_statistics.png', dpi=300, bbox_inches='tight')
        print("✅ Saved visualization: education_statistics.png")
        
        return fig
    
    def print_summary(self, overall: Dict, post_stats: List[Dict]):
        """In tóm tắt thống kê"""
        print("\n" + "="*80)
        print("📊 TỔNG QUAN THỐNG KÊ")
        print("="*80)
        
        print(f"\n📝 TỔNG THỂ:")
        print(f"   Tổng số comments: {overall['total_comments']}")
        print(f"   Tổng số bài viết: {overall['total_posts']}")
        print(f"   Tổng số tác giả: {overall['total_authors']}")
        print(f"   Tổng likes: {overall['total_likes']}")
        print(f"   Trung bình likes/comment: {overall['avg_likes']}")
        
        print("\n📈 PHÂN BỐ LOẠI COMMENT:")
        for type_name, count in overall['type_distribution'].items():
            pct = overall['type_percentages'][type_name + ' (%)']
            print(f"   {type_name}: {count} ({pct}%)")
        
        print("\n❤️ TRUNG BÌNH LIKES THEO LOẠI:")
        for type_name, avg_likes in overall['avg_likes_by_type'].items():
            print(f"   {type_name}: {avg_likes}")
        
        print("\n📊 TOP 3 BÀI VIẾT NHIỀU COMMENTS NHẤT:")
        for i, post in enumerate(post_stats[:3], 1):
            print(f"\n   {i}. {post['post_title'][:60]}...")
            print(f"      Comments: {post['total_comments']} | Likes: {post['total_likes']} | Avg: {post['avg_likes']}")
            print(f"      Phân bố: Type2={post['type_distribution']['Đồng tình (Type 2)']} | " +
                  f"Type3={post['type_distribution']['Phản đối (Type 3)']} | " +
                  f"Type4={post['type_distribution']['Góp ý (Type 4)']}")
    
    def generate_report(self, output_file: str = 'statistics_by_post.json'):
        """Tạo báo cáo thống kê đầy đủ"""
        print("\n📝 Generating statistical report...")
        
        # Calculate statistics
        post_stats = self.calculate_post_statistics()
        overall_stats = self.calculate_overall_statistics()
        
        # Generate visualizations
        self.generate_visualizations(post_stats)
        
        # Create full report
        report = {
            'overall_statistics': overall_stats,
            'post_statistics': post_stats
        }
        
        # Save to file
        print(f"\n💾 Saving report to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Report saved successfully")
        
        # Print summary
        self.print_summary(overall_stats, post_stats)
        
        return report

# ========================================
# MAIN EXECUTION
# ========================================

def main():
    """Main execution"""
    print("="*80)
    print("📊 EDUCATION STATISTICS ANALYZER - By Post Analysis")
    print("="*80)
    
    # Initialize analyzer
    analyzer = EducationStatistics(input_file='data_reclassified.json')
    
    # Load data
    analyzer.load_data()
    
    # Generate report
    report = analyzer.generate_report(output_file='statistics_by_post.json')
    
    print("\n✅ ANALYSIS COMPLETED!")
    print(f"📁 Output files:")
    print(f"   - statistics_by_post.json")
    print(f"   - education_statistics.png")
    
    return report

if __name__ == "__main__":
    report = main()