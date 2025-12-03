import os
import sys
import json

# ====== CHỈNH LIST NÀY THEO TÊN NGƯỜI BẠN MUỐN XỬ LÝ ======
NAMES = [
    "hangdumuc",
    "quanglinh",
    "thuytien",
    "mailisa",
    "hoanghuong",
    "sharkbinh"
    # thêm tên khác ở đây...
]
# =========================================================


def parse_filename(filename):
    """
    Tách 'hangdumuc_thua_nhan_thieu_trach_nhiem.json' ->
    person = 'hangdumuc', event_id = 'thua_nhan_thieu_trach_nhiem'
    """
    if not filename.lower().endswith(".json"):
        return None, None

    base = filename[:-5]  # bỏ .json
    if "_" not in base:
        return None, None

    person, event = base.split("_", 1)
    return person, event


def collect_events_from_dirs(dirs):
    """
    dirs: list thư mục cần scan, ví dụ ['thien', 'duy']
    return: dict theo format đã mô tả
    """
    result = {}

    # init sẵn khung cho từng người trong NAMES
    for name in NAMES:
        result[name] = {
            "name": name,
            "events": []
        }

    for folder in dirs:
        if not os.path.isdir(folder):
            print(f"Folder không tồn tại, bỏ qua: {folder}")
            continue

        for entry in os.listdir(folder):
            if not entry.lower().endswith(".json"):
                continue
            if entry == ".gitkeep":
                continue

            file_path = os.path.join(folder, entry)
            person, event_id = parse_filename(entry)

            # chỉ xử lý nếu person nằm trong NAMES
            if person not in NAMES:
                # bạn có thể print cảnh báo nếu muốn debug
                # print(f"Bỏ qua file {file_path} vì '{person}' không trong NAMES")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Lỗi đọc {file_path}: {e}")
                continue

            event_obj = {
                "event_id": event_id,
                "file": entry,
                "comments": data  # dữ liệu gốc trong file (list comment)
            }

            result[person]["events"].append(event_obj)

    return result


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python gop_su_kien.py <thu_muc_1> <thu_muc_2> ...")
        print("Ví dụ:    python gop_su_kien.py thien duy")
        return

    dirs = sys.argv[1:]
    merged_data = collect_events_from_dirs(dirs)

    # Lưu ra 1 file tổng
    output_file = "all_people_events.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print("Đã gộp xong, file output:", output_file)


if __name__ == "__main__":
    main()
