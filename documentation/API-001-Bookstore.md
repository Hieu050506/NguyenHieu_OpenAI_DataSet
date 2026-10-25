# Hồ sơ API-001-Bookstore

## Nguồn gốc và môi trường

- Nguồn: <https://github.com/martcpp/crud-api-fastapi>.
- Commit cố định: `6888542d376057a82d954d31ec4a962d6f8e1839`.
- License: MIT, copyright 2024 MORDECAI ETUKUDO; giữ nguyên file LICENSE trong source.
- Python đã dùng: 3.12.10, Windows; FastAPI 0.111.0, SQLAlchemy 2.0.29, Pydantic 2.7.1.
- Cài đúng `requirements.txt` gốc; thêm `openapi-spec-validator==0.7.2` để xác thực đặc tả.
- Backend thực tế: SQLite (`src/database.py`), không cần cài server MySQL/PostgreSQL.
- Source ứng dụng giữ nguyên; script chạy, đặc tả và kiểm thử thuộc Dataset ở thư mục bên ngoài source.
- `http-results.json` ghi thời điểm UTC và SHA-256 của các file được kiểm tra.

## Đối chiếu source và hành vi thực tế

| Endpoint | Source | Thành công | Lỗi đã thử |
|---|---|---|---|
| GET /books/ | `src/app.py:fetch_books` | 200, array; database rỗng trả về [] | Chuyển hướng 307 từ /books |
| POST /books/ | `src/app.py:create_book`, `src/schema.py:bookbase` | 201, message và data chứa sách | 422 khi thiếu trường, sai year, null title hoặc JSON sai |
| GET /books/{book_id} | `src/app.py:fetch_book_id` | 200, object sách | 404 khi không tồn tại; 422 khi ID không là integer |
| PUT /books/{book_id} | `src/app.py:update_book` | 200, message và data={} ở runtime đã ghim | 404 khi sách không tồn tại |
| DELETE /books/{book_id} | `src/app.py:delete_book` | 200, message | 404 khi sách không tồn tại hoặc đã xóa |

Schema đầu vào bắt buộc `title`, `author`, `year`, `isbn`. PUT nhận đủ bốn trường, không phải PATCH.
Model lưu `id` tự tăng; test lấy ID từ `response.data.id` thay vì giả định ID.
Source không đặt ràng buộc unique cho ISBN; ca TC17 xác nhận ISBN trùng được chấp nhận.
Không thêm ràng buộc năm dương hay định dạng ISBN vào đặc tả khi ứng dụng không kiểm tra chúng.

## Tách bản sinh tự động và bản chuẩn hóa

1. `results/.../openapi.generated.json` giữ nguyên nội dung JSON lấy từ `/openapi.json`, phiên bản **3.1.0**.
2. Bản gốc thiếu schema response cụ thể cho nhiều endpoint và thiếu khai báo lỗi 404 của ứng dụng.
3. `ground_truth/.../openapi.3.0.3.json` giữ request schema và parameters đơn giản của bản gốc;
   bổ sung Book, schema phản hồi CRUD và NotFound theo source + HTTP.
4. Với bộ schema này, không có cấu trúc chỉ dùng được ở 3.1 cần chuyển đổi (ví dụ type union null).
   Không sử dụng cách đổi số phiên bản cho các project khác mà chưa xem schema.
5. Xác thực cả hai bản bằng `openapi-spec-validator`; xác thực response JSON của các status được khai báo
   bằng JSON Schema, đồng thời kiểm tra trạng thái và các giá trị trọng yếu trong ca HTTP.
6. `verification.json` chỉ ghi `verified_with_known_limitations` khi toàn bộ 28 ca đạt.
   Nếu một lần kiểm thử sau thất bại, trạng thái chuyển `failed`; không coi đặc tả cũ còn được xác minh.

Bản chuẩn này mô tả project gốc tại commit và runtime đã ghim. Nó chưa được phản biện thủ công bởi nhóm,
chưa bao phủ mọi đầu vào, và không chứng minh tính an toàn hay chất lượng production.

## Lỗi và giới hạn đã biết

- **PUT trả về data rỗng:** commit làm ORM object hết hạn, ứng dụng trả object trước khi refresh.
  TC15 kiểm tra phản hồi `{\"message\":\"Book updated successfully\",\"data\":{}}`.
  TC16 gọi GET riêng để xác nhận dữ liệu đã cập nhật. Đặc tả ghi nhận data là object rỗng;
  đây là mô tả lỗi hiện tại, không phải thiết kế được khuyến nghị.
- **Test upstream không đủ để làm bằng chứng:** một số test cố định ID=1; một số lấy ID ở cấp ngoài
  `response.id` trong khi response thực tế dùng `response.data.id`, nên có thể bỏ qua nhánh kiểm tra.
  Dataset dùng bộ 28 ca độc lập, không sửa test upstream và không tuyên bố test upstream đã đạt.
- Không có authentication, phân trang hoặc unique ISBN trong source này.
- Phiên bản thư viện gốc cũ được giữ để tái lập; không có kiểm toán bảo mật trong hồ sơ này.
- Kiểm tra /docs là kiểm tra HTTP chứa Swagger UI, chưa phải kiểm thử giao diện bằng trình duyệt.

## Phạm vi bằng chứng

28 ca HTTP bao phủ 5 operation CRUD, đọc database rỗng, tạo rồi đọc lại,
cập nhật rồi đọc xác nhận, xóa rồi kiểm tra 404, request sai, ID sai, ISBN trùng,
redirect, method không hỗ trợ và route không tồn tại.
28 ca kiểm thử vẫn chỉ là **một project**, không được tính thành 28 project Dataset.
