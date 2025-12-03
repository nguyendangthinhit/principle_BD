import os
import json

def merge_and_restructure():
    username = "thinh"
    root = username
    
    # Kiểm tra thư mục tồn tại
    if not os.path.isdir(root):
        print(f"Không tìm thấy thư mục: {root}")
        return
    
    # BƯỚC 1: Gộp tất cả file JSON (trừ .gitkeep)
    merged_data = {}
    
    for filename in os.listdir(root):
        # Bỏ qua .gitkeep và các file không phải JSON
        if filename == ".gitkeep" or not filename.lower().endswith(".json"):
            continue
        
        filepath = os.path.join(root, filename)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                file_data = json.load(f)
                
                # Nếu file_data là list, gán vào merged_data
                if isinstance(file_data, list):
                    merged_data[filename] = file_data
                else:
                    print(f"Cảnh báo: {filename} không phải list, bỏ qua")
        except Exception as e:
            print(f"Lỗi đọc file {filename}: {e}")
    
    # Lưu file merge tạm
    merge_path = os.path.join(root, f"{username}_raw_data.json")
    with open(merge_path, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
    
    print(f"Đã gộp {len(merged_data)} file vào: {merge_path}")
    
    # BƯỚC 2: Restructure theo cấu trúc mới
    new_data = {}
    
    for filename, comments_list in merged_data.items():
        # 1. title = tên file bỏ đuôi .json
        if filename.lower().endswith(".json"):
            title = filename[:-5]
        else:
            title = filename
        
        # 2. Gom comment theo postTitle
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
        
        # 3. Chuyển posts_dict thành list (bỏ qua post có comments rỗng)
        posts_list = []
        for pt, cmts in posts_dict.items():
            # Chỉ thêm vào nếu comments không rỗng
            if cmts:
                posts_list.append({
                    "postTitle": pt,
                    "comments": cmts
                })
        
        # 4. Gán vào new_data (chỉ thêm nếu có posts_list)
        if posts_list:
            new_data[filename] = {
                "title": title,
                "post": posts_list
            }
    
    # 5. Lưu file structured
    out_path = os.path.join(root, "education.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
    
    print(f"Đã restructure xong! File mới: {out_path}")
    print(f"Tổng cộng: {len(new_data)} file được xử lý")


if __name__ == "__main__":
    merge_and_restructure()