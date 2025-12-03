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


def collect_events_from_dirs():
    """
    Scan 3 thư mục: duy/FilteredDetails, huy, thien
    Gộp theo cấu trúc: name -> events (mỗi event có postTitle và comments)
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
                    comments_list = json.load(f)
                
            except Exception as e:
                print(f"Lỗi đọc {file_path}: {e}")
                continue

            # Khởi tạo cấu trúc cho người này nếu chưa có
            if person not in people_data:
                people_data[person] = []

            # Kiểm tra comments_list phải là list
            if not isinstance(comments_list, list):
                print(f"File {entry} không phải list, bỏ qua")
                continue

            # Gom comment theo postTitle
            posts_dict = {}
            
            for cmt in comments_list:
                if not isinstance(cmt, dict):
                    continue
                
                # Lấy postTitle
                post_title = cmt.get("postTitle") or cmt.get("posttitle") or "UNKNOWN_POST_TITLE"
                
                # Copy comment và bỏ field postTitle
                cmt_clean = dict(cmt)
                cmt_clean.pop("postTitle", None)
                cmt_clean.pop("posttitle", None)
                
                # Xóa field "comments": [] nếu có và rỗng
                if "comments" in cmt_clean and not cmt_clean["comments"]:
                    cmt_clean.pop("comments", None)
                
                # Thêm vào group
                posts_dict.setdefault(post_title, []).append(cmt_clean)
            
            # Chuyển posts_dict thành events list
            for post_title, comments in posts_dict.items():
                if comments:  # Chỉ thêm nếu có comments
                    event_obj = {
                        "events": event_id,
                        "postTitle": post_title,
                        "comments": comments
                    }
                    people_data[person].append(event_obj)

            print(f"  + Thêm: {person} - {event_id} ({len(posts_dict)} posts)")

    # Chuyển sang cấu trúc cuối cùng
    final_data = []
    for person, events_list in people_data.items():
        final_data.append({
            "name": person,
            "events": events_list
        })

    return final_data


def main():
    print("Bắt đầu gộp file từ duy/FilteredDetails, huy, thien...")
    
    merged_data = collect_events_from_dirs()

    # Lưu ra file tổng
    output_file = "Showbiz.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"\n✓ Đã gộp xong!")
    print(f"✓ Tổng số người: {len(merged_data)}")
    for person_data in merged_data:
        print(f"  - {person_data['name']}: {len(person_data['events'])} bài post")
    print(f"✓ File output: {output_file}")


if __name__ == "__main__":
    main()