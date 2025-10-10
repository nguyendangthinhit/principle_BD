# file này là file chuyển dữ liệu từ txt sang json để sau này tiện cho việc xử lí và train ai :) sao tôi k viết hoa đc 
# run thử file để biết cách sử dụng
import sys
import json
import re
from typing import List, Dict
from pathlib import Path

def parse_post_from_lines(lines: List[str]) -> Dict:
    post_data = {
        "url": "",
        "poster": "",
        "author": "",
        "content": "",
        "time": "",
        "comments": []
    }

    i = 0
    while i < len(lines):
        line = lines[i]

        # ✅ Nhận link (dù là "Link:", "Link ", hoặc chứa facebook.com)
        if "facebook.com" in line:
            match = re.search(r"https?://\S+", line)
            if match:
                post_data["url"] = match.group(0)

        elif line.startswith("Bài viết của"):
            post_data["poster"] = line[12:].strip()

        elif line == "Tác giả":
            if i + 1 < len(lines):
                post_data["author"] = lines[i + 1].strip()
                i += 1

        elif line.startswith("Nội dung bài viết:"):
            post_data["content"] = line[20:].strip()

        elif re.match(r"\d+ (giây|phút|giờ|ngày|tuần|tháng|năm)", line):
            post_data["time"] = line

        elif line == "Trả lời":
            break

        i += 1

    # Parse comments
    while i < len(lines):
        line = lines[i]

        # Bỏ các dòng không quan trọng
        if line in {"Trả lời", "Đã chỉnh sửa", "Fan cứng", "Fan đang lên", "Xem bản dịch"}:
            i += 1
            continue

        if i + 2 >= len(lines):
            break

        user = lines[i]
        text = lines[i + 1]
        time = lines[i + 2]

        if not re.match(r"\d+ (giây|phút|giờ|ngày|tuần|tháng|năm)", time):
            i += 1
            continue

        post_data["comments"].append({
            "user": user,
            "text": text,
            "time": time
        })
        i += 3

    return post_data


def main():
    if len(sys.argv) != 2:
        print("⚠️ Cách dùng: python process.py <path/file.txt>")
        print("Ví dụ: python process.py thinh/cao.txt")
        sys.exit(1)

    txt_path = Path(sys.argv[1])

    if not txt_path.exists():
        print(f"❌ Không tìm thấy file: {txt_path}")
        sys.exit(1)

    user_folder = txt_path.parent.name
    json_path = txt_path.parent / f"{user_folder}_all_posts.json"

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    parsed_post = parse_post_from_lines(lines)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            all_posts = json.load(f)
    except FileNotFoundError:
        all_posts = []

    all_posts.append(parsed_post)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Đã thêm bài viết mới vào: {json_path}")
    print(f"📎 Link bài viết: {parsed_post['url']}")
    print(f"📝 Số comment: {len(parsed_post['comments'])}")

if __name__ == "__main__":
    main()
