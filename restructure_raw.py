import os
import json
import sys

def restructure(username):
    root = username
    raw_path = os.path.join(root, f"{username}_raw_data.json")

    if not os.path.isfile(raw_path):
        print("Không tìm thấy file:", raw_path)
        return

    # Đọc dữ liệu merge cũ
    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    new_data = {}

    # data có dạng: { "file.json": [cmt1, cmt2, ...], ... }
    for filename, comments_list in data.items():
        # 1. title = tên file bỏ đuôi .json
        if filename.lower().endswith(".json"):
            title = filename[:-5]
        else:
            title = filename

        # 2. Gom comment theo postTitle
        posts_dict = {}  # { postTitle: [list comment] }

        for cmt in comments_list:
            if not isinstance(cmt, dict):
                continue

            # lấy postTitle (có thể là "postTitle" hoặc "posttitle" cho chắc)
            post_title = cmt.get("postTitle") or cmt.get("posttitle") or "UNKNOWN_POST_TITLE"

            # copy comment & bỏ field postTitle bên trong
            cmt_clean = dict(cmt)
            cmt_clean.pop("postTitle", None)
            cmt_clean.pop("posttitle", None)

            # thêm vào group
            posts_dict.setdefault(post_title, []).append(cmt_clean)

        # 3. Chuyển posts_dict -> list post
        posts_list = []
        for pt, cmts in posts_dict.items():
            posts_list.append({
                "postTitle": pt,
                "comments": cmts
            })

        # 4. Gán vào new_data với cấu trúc:
        # "file.json": { "title": <tên>, "post": [ {postTitle, comments}, ... ] }
        new_data[filename] = {
            "title": title,
            "post": posts_list
        }

    # 5. Lưu ra file mới trong thư mục user
    out_path = os.path.join(root, f"{username}_raw_data_structured.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

    print("Đã restructure xong! File mới:", out_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cách dùng: python restructure_raw.py <username>")
    else:
        restructure(sys.argv[1])
