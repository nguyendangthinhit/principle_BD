Đôi lời gửi ae 😃
Đây là dự án của môn thầy Long. Mục tiêu của dự án là xây dựng một ứng dụng chat bot hoàn chỉnh từ khâu thu thập dữ liệu, tiền xử lý, tinh chỉnh mô hình cho đến triển khai giao diện người dùng.

Nội dung chính
Thu thập dữ liệu (Data Acquisition): Bộ dữ liệu gồm khoảng XX,XXX mẫu (tuỳ dự án cụ thể).

Tiền xử lý & Phân tích (EDA): Làm sạch dữ liệu, trực quan hóa và phân tích đặc trưng.

Sử dụng RAG, build trên nền tảng n8n.

Giao diện người dùng (UI): Messenger.

Kiểm thử & Cải tiến: Đánh giá hiệu năng, tinh chỉnh tham số và cải thiện kết quả.

Công nghệ sử dụng
Ngôn ngữ: Python

Thư viện: TensorFlow / PyTorch, Scikit-learn, Pandas, Matplotlib

Công cụ: Jupyter Notebook, GitHub, VS Code

Triển khai: Flask / Streamlit cho giao diện người dùng

Kết quả
# 📁 Folder chứa dữ liệu của nhóm

> ⚠️ **Nhớ pull dữ liệu về trước rồi hãy push nhaaaaaaaaaaaa!!!!!!!!!!!!!!!!!**  
Tui nhắc lại workflow cào dữ liệu của cả nhóm (do có xíu thay đổi để hợp lý hơn). Tui chỉ nói với vài người nên mấy ak khác coi kỹ 🤭  

---

## 🔵 1. Ghi chú ban đầu
Hiện tại tui **mới làm phần cào data Facebook thui nha**.  
Khi nào làm tới YouTube, báo – news – các kiểu thì tui sẽ cập nhật lại sau.

Trong folder này tui đã **chuẩn bị sẵn thư mục cho từng người rồi**.  
Nhiệm vụ của mn: **đặt tên đúng → cào đúng folder → xong.**

---

## 🔵 2. Kiểm tra link trước khi cào (rất quan trọng!!!)

Việc đầu tiên mấy má phải làm trước khi đi cào dữ liệu:  
👉 **Check xem link có bị trùng không.**  
Không check → cào trùng → tốn thời gian → dữ liệu lỗi 😐

Trong thư mục `data/` sẽ có:

- `links_fb.json` – chứa toàn bộ link mọi người đã cào  
- `check_link.py` – script để kiểm tra link đã tồn tại hay chưa  

Vào file `check_link.py` xem hướng dẫn sử dụng rồi chạy theo nha.

---

## 🔵 3. Cấu trúc dữ liệu sau khi cào

Sau khi check link xong thì bắt đầu đi cào.  
Dữ liệu thu được sẽ có dạng:

```
link: <link>  
...
(nội dung file .json)
...
Nội dung bài viết: <nội dung ở trỏng>__
```

### 🔸 Note:
Nếu bài viết là **dạng hình ảnh** → mn phải **tự thêm nội dung mô tả** cho phù hợp.

Trong repo này đã có **1 file mẫu** để mọi người tham khảo cách cào và cách format.  
Trong `transfer_txt_json_web.py` và `transfer_txt_json_fb.py` tui đã hướng dẫn cách xài rồi đó → mở lên chạy thử là hiểu 😌

---

## 🔵 4. Lưu ý khi làm việc với Git

Mấy file như:

- file mẫu,
- file xử lý dữ liệu,
- file xử lý link,

👉 **cấm sửa bậy nhaaa 🙂**

Quy tắc:  
- Git repo này -> mn pull về  
- Làm việc xong -> nhớ update lên liền  
- Đừng để file lệch version gây lỗi cho cả team 🤝

---

# 📌 Quy tắc đặt tên & định dạng dữ liệu

Dữ liệu sau khi cào về lưu theo format:

```
<tên người liên quan sự kiện>_<tên sự kiện>.json
```

Và để vào đúng **thư mục tên của mình**.

---

# 🧩 Các trường dữ liệu cần lấy (7 trường)

Khi cào, nhớ lấy đủ 7 trường sau:

1. `commentsCount`
2. `comments`  
3. `text`  
4. `profileName`  
5. `postTitle`  
6. `parentRely`  
7. `likesCount`
