!pip install -q transformers accelerate tqdm
import torch
print(torch.cuda.get_device_name(0))
import os
import json
from tqdm import tqdm
from transformers import pipeline

# Zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# File đầu vào
INPUT_FILE = "Thinh_all_posts.json"
CHECK_FILE = "links_fb.json"
OUTPUT_FILE = "processed_data.json"


from datetime import datetime
import re

def merge_author(poster, author):
    return author if author else poster

def normalize_time(raw_time, url):
    # Ví dụ: "28 tháng 6 lúc 11:25" => "2025-06-28T11:25"
    try:
        pattern = r"(\d{1,2}) tháng (\d{1,2}) lúc (\d{1,2}):(\d{2})"
        match = re.search(pattern, raw_time)
        if match:
            day, month, hour, minute = map(int, match.groups())
            dt = datetime(2025, month, day, hour, minute)
            return dt.isoformat()
    except Exception as e:
        print(f"[!] Lỗi parse time: {raw_time} ({url}) → {e}")
    return raw_time

def is_valid_comment(text):
    if not text.strip():
        return False
    if len(text.strip()) < 3:
        return False
    if re.fullmatch(r"[\W_]+", text):  # icon-only
        return False
    if re.search(r"https?://", text):
        return False
    return True

def classify_comment(text):
    labels = ["Tích cực", "Tiêu cực", "Trung lập"]
    result = classifier(text, labels)
    return result["labels"][0], float(result["scores"][0])

# Load dữ liệu gốc
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load check_link
with open(CHECK_FILE, 'r', encoding='utf-8') as f:
    raw_check_data = json.load(f)

# Tạo dict check_data
check_data = {item["source_url"]: item["time"] for item in raw_check_data}

# Nếu OUTPUT_FILE đã tồn tại, load dữ liệu đã xử lý
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        processed = json.load(f)
    print(f"✅ Đã load {len(processed)} bài đã xử lý từ '{OUTPUT_FILE}'.")
else:
    processed = []
    print("🔵 Chưa có dữ liệu đã xử lý, bắt đầu mới.")

# Tạo set để tránh xử lý trùng
processed_urls = {post["url"] for post in processed}
# Bắt đầu xử lý
total_posts = len(data)
done_count = len(processed)

progress = tqdm(data, desc=f"Processing posts ({done_count}/{total_posts})")

for post in progress:
    url = post.get("url", "")
    if url in processed_urls:
        progress.set_postfix_str("Đã xử lý, bỏ qua")
        continue

    # Gộp author
    post["author"] = merge_author(post.get("poster", ""), post.get("author", ""))
    post["time"] = normalize_time(post.get("time", ""), url)

    valid_comments = []
    opinion_summary = {}

    for cmt in post.get("comments", []):
        if not is_valid_comment(cmt["text"]):
            continue
        label, score = classify_comment(cmt["text"])
        cmt["label"] = label
        cmt["score"] = round(score, 3)

        if label not in opinion_summary:
            opinion_summary[label] = []
        opinion_summary[label].append(cmt["text"])

        valid_comments.append(cmt)

    post["comments"] = valid_comments
    post["opinion_summary"] = {k: v[:3] for k, v in opinion_summary.items()}

    processed.append(post)
    processed_urls.add(url)

    # Save ngay sau mỗi bài
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        json.dump(processed, out, ensure_ascii=False, indent=2)

    done_count += 1
    progress.set_postfix_str(f"Đã xử lý {done_count}/{total_posts}")

print("✅ Hoàn tất xử lý tất cả bài.")

