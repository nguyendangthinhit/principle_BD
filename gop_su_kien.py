import os
import json

def parse_filename(filename):
    """
    Tách 'ten_nguoi_su_kien.json' ->
    person = 'ten_nguoi', event = 'su_kien'
    """
    if not filename.lower().endswith(".json"):
        return None, None

    base = filename[:-5]  # bỏ .json
    if "_" not in base:
        return None, None

    parts = base.split("_", 1)
    person = parts[0]
    event = parts[1] if len(parts) > 1 else ""
    
    return person, event


def remove_empty_comments(data):
    """
    Xóa field 'comments': [] rỗng trong tất cả các comment
    """
    if isinstance(data, dict):
        # Xóa field "comments" nếu nó rỗng
        if "comments" in data and not data["comments"]:
            data.pop("comments", None)
        
        # Đệ quy xử lý các giá trị con
        for key, value in list(data.items()):
            remove_empty_comments(value)
    
    elif isinstance(data, list):
        # Đệ quy xử lý từng phần tử trong list
        for item in data:
            remove_empty_comments(item)
    
    return data


def collect_events_from_dirs():
    """
    Scan 3 thư mục: duy/FilteredDetails, huy, thien
    Gộp theo cấu trúc: name -> events
    """
    dirs = [
        "duy/FilteredDetails",
        "huy", 
        "thien"
    ]
    
    # Dictionary để lưu theo tên người
    people_data = {}

    for folder in dirs:
        if not os.path.isdir(folder):
            print(f"Folder không tồn tại, bỏ qua: {folder}")
            continue

        print(f"Đang xử lý thư mục: {folder}")
        
        for entry in os.listdir(folder):
            if not entry.lower().endswith(".json"):
                continue
            if entry == ".gitkeep":
                continue

            file_path = os.path.join(folder, entry)
            person, event_id = parse_filename(entry)

            if not person or not event_id:
                print(f"Không parse được file: {entry}")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Xóa tất cả "comments": [] rỗng
                data = remove_empty_comments(data)
                
            except Exception as e:
                print(f"Lỗi đọc {file_path}: {e}")
                continue

            # Khởi tạo cấu trúc cho người này nếu chưa có
            if person not in people_data:
                people_data[person] = {
                    "name": person,
                    "events": []
                }

            # Thêm sự kiện
            event_obj = {
                "event": event_id,
                "comments": data
            }

            people_data[person]["events"].append(event_obj)
            print(f"  + Thêm: {person} - {event_id}")

    return people_data


def main():
    print("Bắt đầu gộp file từ duy/FilteredDetails, huy, thien...")
    
    merged_data = collect_events_from_dirs()

    # Lưu ra file tổng
    output_file = "Showbiz.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"\n✓ Đã gộp xong!")
    print(f"✓ Tổng số người: {len(merged_data)}")
    for person, info in merged_data.items():
        print(f"  - {person}: {len(info['events'])} sự kiện")
    print(f"✓ File output: {output_file}")


if __name__ == "__main__":
    main()