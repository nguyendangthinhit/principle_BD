import json
from collections import defaultdict

# ====== BƯỚC 1: Nhập danh sách bài Before/After ======
# Ví dụ mẫu (bạn thay bằng danh sách thực tế của bạn)
before_titles = [
    "@ Nhiều người nhận xét rằng đề thi toán kì thi THPT Quốc gia 2025 quá dài và khó ",
    "@ Nhiều sĩ tử nhận xét đề thi tiếng Anh kì thi THPT Quốc gia 2025 khá khó đối với những bạn chưa tiếp xúc với đề thi IELTS",
    "@ Đối với năm nay - năm 2025, đề thi tiếng Anh kì thi THPT Quốc gia được nhiều người nhận định rằng đề quá dài và cỡ chữ được in với kích thước nhỏ hơn bình thường",
    "@ ‼BỘ GIÁO DỤC LÝ GIẢI VỀ ĐỘ KHÓ CỦA ĐỀ THI TỐT NGHIỆP THPT 2025: ”Ma trận đề thi tốt nghiệp khiến giáo viên, học sinh không thể đoán trước, đảm bảo học thật, thi thật”",
    "@ Đề thi Ngữ văn kì thi THPT Quốc gia 2025 được đánh giá là đề thi vừa sức, vừa sâu sắc, góp phần đổi mới phương pháp thi – học song song với đó điểm Ngữ văn cao nhất là 9,5 điểm ",
    "@ Đề thi THPT Quốc gia môn Vật Lý năm 2025 được đánh giá là dễ hơn các môn còn lại và vừa sức với sĩ tủ "

]
after_titles = [
    "@ Thi tốt nghiệp THPT: Đã xuất hiện những bài Văn đạt điểm 9 và trên 9, phần nghị luận “Vùng trời quê hương nào cũng là bầu trời tổ quốc” nhiều bài viết rất tốt, có dẫn chứng thực tế về việc sáp nhập tỉnh, thành ❤🇻🇳",
    "@ Sau khi Bộ GD & ĐT công bố đáp án chính thức các môn thi tốt nghiệp THPT năm 2025 thì dư luận đã có xư hướng quay xe, không còn nhận định đề khó",
    "@ Nhiều chuyên gia nhận định tổ hợp D01 (toán, văn, tiếng Anh) sẽ biến động mạnh sau khi công bố điểm thi tốt nghiệp THPT",
    "@ Đề tiếng Anh kì thi THPT 2025 được nhận định là đề thi vừa sức, số lượng câu hỏi khó không nhiều",
    "@ Đề thi THPT Quốc gia 2025 được nhận định là đề vừa sức, điểm cao xuất hiện nhiều ở các môn Văn, Toán, Tiếng Anh",
    "@ Đề thi Ngữ văn kì thi THPT Quốc gia 2025 được đánh giá là đề thi vừa sức, vừa sâu sắc, góp phần đổi mới phương pháp thi – học song song với đó điểm Ngữ văn cao nhất là 9,5 điểm "
    
]
print("độ dài của số trước ",len(before_titles))
print("độ dài của số sau ",len(after_titles))

# ====== BƯỚC 2: Load file clean_data.json ======
with open("clean_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ====== BƯỚC 3: Hàm gom thống kê ======
def collect_stats(target_titles, dataset):
    stats = defaultdict(int)
    for post in dataset:
        content = post.get("content", "")
        if isinstance(content, list):
            content = " ".join(content)
        if content in target_titles:
            opinions = post.get("summary", {}).get("opinions", [])
            for op in opinions:
                label = op.get("label", "").strip()
                desc = op.get("description", "").lower().replace("số lượng comment:", "").strip()
                try:
                    count = int(desc)
                except:
                    count = 0
                stats[label] += count
    return stats

# ====== BƯỚC 4: Gom số liệu ======
before_stats = collect_stats(before_titles, data)
after_stats = collect_stats(after_titles, data)

# ====== BƯỚC 5: Xuất kết quả ======
print("=== Thống kê BEFORE ===")
for label, count in before_stats.items():
    print(f"{label}: {count}")
print(f"Tổng BEFORE: {sum(before_stats.values())}")

print("\n=== Thống kê AFTER ===")
for label, count in after_stats.items():
    print(f"{label}: {count}")
print(f"Tổng AFTER: {sum(after_stats.values())}")

# ====== Nếu muốn lưu ra JSON ======
output = [
    {"id": "trước khi có kết quả thi thpt", "result": before_stats},
    {"id": "sau khi có kết quả thi thpt", "result": after_stats}
]
with open("summary_selected_posts.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("\nĐã lưu file summary_selected_posts.json")
