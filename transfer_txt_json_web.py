import sys
import json
from pathlib import Path
from datetime import datetime

def parse_article_from_lines(lines):
    data = {
        "id": "",
        "title": "",
        "source_type": "",
        "source_url": "",
        "date": datetime.today().strftime("%Y-%m-%d"),
        "content": "",
        "highlights": []
    }

    content_started = False
    content_lines = []

    for line in lines:
        if line.startswith("id:"):
            data["id"] = line[3:].strip()
        elif line.startswith("link:"):
            data["source_url"] = line[5:].strip()
        elif line.startswith("source_type:"):
            data["source_type"] = line[12:].strip()
        elif line.startswith("title:"):
            data["title"] = line[6:].strip()
        elif line.startswith("content:"):
            content_started = True
            content_lines.append(line[8:].strip())
        elif content_started:
            content_lines.append(line.strip())

    data["content"] = "\n".join(content_lines).strip()
    return data

def main():
    if len(sys.argv) != 2:
        print("⚠️ Cách dùng: python process_web.py <path/to/file.txt>")
        print("Ví dụ: python process_web.py thinh/cao_web.txt")
        sys.exit(1)

    txt_path = Path(sys.argv[1])
    if not txt_path.exists():
        print(f"❌ Không tìm thấy file: {txt_path}")
        sys.exit(1)

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    parsed_article = parse_article_from_lines(lines)

    user_folder = txt_path.parent.name
    json_path = txt_path.parent / f"{user_folder}_all_web_posts.json"

    # Gộp nếu đã có file json trước đó
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(parsed_article)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu vào: {json_path}")

if __name__ == "__main__":
    main()
