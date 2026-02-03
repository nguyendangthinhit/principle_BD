# Principle_BD — Hướng dẫn nhanh

Xin chào mọi người 😃  
Đây là project của môn thầy Long. Mục tiêu: xây dựng một chatbot hoàn chỉnh — từ thu thập dữ liệu, tiền xử lý, tinh chỉnh mô hình, đến triển khai giao diện.

---

## Mục lục
1. Giới thiệu ngắn
2. Nội dung chính của project
3. Hướng dẫn cào dữ liệu (workflow)
4. Cấu trúc dữ liệu & file mẫu
5. Lưu ý khi dùng Git
6. Quy tắc đặt tên file
7. Các trường dữ liệu bắt buộc
8. Công nghệ sử dụng

---

## 1. Giới thiệu ngắn
Project tập trung vào:
- Thu thập dữ liệu (Facebook hiện đã làm trước; sẽ cập nhật cho YouTube, News… )
- Tiền xử lý & EDA
- Xây dựng RAG, orchestration bằng n8n
- UI: Messenger
- Triển khai/kiểm thử (Flask/Streamlit)

---

## 2. Nội dung chính
- Thu thập dữ liệu (Data acquisition): dự kiến ~XX,XXX mẫu (tuỳ dự án)
- Tiền xử lý & Phân tích (EDA): làm sạch, trực quan hoá, trích đặc trưng
- Sử dụng RAG và n8n cho pipeline
- Giao diện người dùng (Messenger)
- Kiểm thử, đánh giá và cải tiến

---

## 3. Workflow cào dữ liệu (quan trọng)
Trước khi cào, **LUÔN** làm các bước sau:
1. Pull repo về (không làm việc trên phiên bản cũ).
2. Kiểm tra link có trùng lặp hay chưa (rất quan trọng).
3. Cào dữ liệu vào đúng thư mục của từng thành viên.
4. Sau khi hoàn tất, push lên (nhớ theo quy tắc đặt tên).

Cảnh báo quan trọng:
> ⚠️ Nhớ pull dữ liệu về trước rồi mới push! Nếu không, dễ gây xung đột hoặc mất dữ liệu.

Files liên quan:
- `data/links_fb.json` — chứa toàn bộ link đã cào
- `check_link.py` — script kiểm tra link đã tồn tại hay chưa (mở file để xem hướng dẫn)
- `transfer_txt_json_web.py`, `transfer_txt_json_fb.py` — file mẫu & hướng dẫn format

---

## 4. Cấu trúc dữ liệu & file mẫu
Sau khi cào, dữ liệu lưu dưới dạng JSON. Mỗi file JSON chứa thông tin bài viết và comment theo format mẫu.  
Ví dụ (khung mẫu):

```json
{
  "link": "<link>",
  "profileName": "<tên người đăng>",
  "postTitle": "<tiêu đề>",
  "text": "<nội dung bài/ comment>",
  "commentsCount": 123,
  "likesCount": 45,
  "parentRely": "<nội dung parent nếu là reply>",
  "comments": [ /* mảng comment */ ]
}
```

Ghi chú:
- Nếu bài viết là ảnh, cần bổ sung mô tả (caption) thủ công để đảm bảo dữ liệu có nội dung text.

---

## 5. Lưu ý khi làm việc với Git
- Những file mẫu, script xử lý dữ liệu, và file kiểm soát link: **KHÔNG sửa bậy** nếu không có thảo luận với team.
- Quy trình:
  - Pull trước khi làm
  - Làm xong -> commit & push ngay
  - Tránh để file lệch version gây lỗi cho cả team

---

## 6. Quy tắc đặt tên & lưu trữ
Tên file sau khi cào:
``
<tên_người_liên_quan>_<tên_sự_kiện>.json
```
Và đặt vào đúng thư mục có tên thành viên trong `data/`.

---

## 7. Các trường dữ liệu cần lấy (bắt buộc — 7 trường)
Khi cào nhớ lấy đủ 7 trường sau:
1. `commentsCount`
2. `comments`
3. `text`
4. `profileName`
5. `postTitle`
6. `parentRely`
7. `likesCount`

---

## 8. Công nghệ sử dụng
- Ngôn ngữ: Python
- Thư viện: TensorFlow / PyTorch, Scikit-learn, Pandas, Matplotlib
- Công cụ: Jupyter Notebook, VS Code, GitHub
- Triển khai: Flask / Streamlit
- Orchestration: n8n (cho RAG / pipeline)

---

Nếu cần, mình có thể:
- Viết lại README tiếng Anh
- Tạo template file JSON mẫu trong repo
- Thêm CI check đơn giản để kiểm tra tên file / format trước khi push
