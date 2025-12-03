import json
import sys
import os

def merge_mailisa(raw_file, main_file):
    # đọc file all_people_events_clean.json
    with open(main_file, "r", encoding="utf-8") as f:
        main_data = json.load(f)

    # đọc file mailisa_merged_raw.json
    with open(raw_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # chuẩn bị object mailisa dạng chuẩn events
    mailisa_obj = {
        "name": "mailisa",
        "events": []
    }

    for key, comments in raw_data.items():
        # key = "mailisa_2700_ti_dong"
        if not key.startswith("mailisa_"):
            continue

        event_id = key[len("mailisa_"):]  # lấy phần sau prefix
        filename = key + ".json"

        mailisa_obj["events"].append({
            "event_id": event_id,
            "file": filename,
            "comments": comments
        })

    # gắn mailisa vào main_data
    main_data["mailisa"] = mailisa_obj

    # lưu file mới
    out_file = "all_people_events_merged.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(main_data, f, ensure_ascii=False, indent=4)

    print("Đã merge mailisa vào file tổng!")
    print("Output:", out_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Cách dùng:")
        print("  python merge_mailisa_into_all.py <raw_mailisa_file> <main_all_file>")
        sys.exit(0)

    merge_mailisa(sys.argv[1], sys.argv[2])
