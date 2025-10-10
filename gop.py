import os
import json

# Các thư mục chứa dữ liệu từ từng người
folders = ['Thinh', 'Huy',"Loan","quang"]
merged_data = []

for folder in folders:
    # Lấy ra tên file, ví dụ 'thinh_all_post.json'
    json_filename = f"{folder}_all_web_posts.json"
    json_path = os.path.join(folder, json_filename)

    # Kiểm tra file tồn tại không
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    merged_data.append(data)
            except json.JSONDecodeError as e:
                print(f"⚠️ Lỗi đọc file {json_path}: {e}")
    else:
        print(f"❌ Không tìm thấy file: {json_path}")

# Ghi dữ liệu gộp vào file data.json
with open('data_web.json', 'w', encoding='utf-8') as f_out:
    json.dump(merged_data, f_out, ensure_ascii=False, indent=2)

print(f"✅ Đã gộp xong dữ liệu từ {len(folders)} thư mục vào 'data_web.json'. Số lượng mục: {len(merged_data)}")



