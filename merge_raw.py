import os
import json
import sys

def merge_json(username):
    root = username  # thư mục người dùng

    if not os.path.isdir(root):
        print("Thư mục không tồn tại:", root)
        return

    output = {}

    # Duyệt toàn bộ file trong thư mục (kèm subfolder)
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith(".json"):
                file_path = os.path.join(dirpath, filename)

                # Skip file output cũ để tránh tự đọc lại chính nó
                if filename == f"{username}_raw_data.json":
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception as e:
                    print(f"Lỗi đọc {file_path}: {e}")
                    continue

                # Lưu theo format:
                # { "filename.json": { ...data... } }
                output[filename] = data

    # Lưu file output vào ngay bên trong thư mục user
    out_path = os.path.join(root, f"{username}_raw_data.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    print("Đã gộp xong! File output nằm tại:", out_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cách dùng: python merge_raw.py <username>")
    else:
        merge_json(sys.argv[1])
