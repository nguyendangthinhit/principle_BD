" HƯỚNG DẪN SỬ DỤNG"
"mà có chi mô hướng dẫn , đọc cái test input phần main ak, lấy dữ liệu cho giống cái nớ quăng dô thế chỗ nớ là đc"

import json
import re
import os

def normalize(text):
    """Chuẩn hóa chuỗi: loại bỏ khoảng trắng thừa ở đầu, cuối, và rút gọn giữa"""
    return re.sub(r'\s+', ' ', text.strip())

def normalize_content(raw_content):
    """Xử lý content có thể là list hoặc string"""
    if isinstance(raw_content, list):
        return normalize(" ".join(raw_content))
    elif isinstance(raw_content, str):
        return normalize(raw_content)
    else:
        return ""

def is_duplicate_link_and_add(new_entry, file_path='links_fb.json'):
    new_name = normalize(new_entry.get('name', ''))
    new_time = normalize(new_entry.get('time', ''))
    new_content = normalize_content(new_entry.get('content', ''))
    new_url = normalize(new_entry.get('source_url', ''))

    new_entry_normalized = {
        "name": new_name,
        "time": new_time,
        "content": new_content,
        "source_url": new_url
    }

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    for entry in data:
        name = normalize(entry.get('name', ''))
        time = normalize(entry.get('time', ''))
        content = normalize_content(entry.get('content', ''))
        if new_name == name and new_time == time and new_content == content:
            return "trùng rồi"

    data.append(new_entry_normalized)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return "oke"


# =============================
# 👇 Đoạn test mẫu
# =============================
"ví dụ"
# test_input = {
#         "name": "Kaito Kid",
#         "time": "10 tháng 7 lúc 14:17",
#         "content": "Đề thi tốt nghiệp THPT quá khó, Quốc hội yêu cầu báo cáo",
#         "source_url": "https://www.facebook.com/share/p/1C8B5TNDDp/"
#     }
if __name__ == "__main__":
    test_input = {
        "name": "Kaito Kid",
        "time": "27 tháng 6 lúc 09:50 ",
        "content": "CHÍNH THỨC: Đề thi tốt nghiệp THPT môn Vật Lý năm 2025.",
        "source_url": "https://www.facebook.com/share/p/19bPCoimAv/"
    }


    print(is_duplicate_link_and_add(test_input))  # Kết quả: "oke" hoặc "trùng rồi"
