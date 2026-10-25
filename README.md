# NguyenHieu_OpenAI_DataSet

Dataset OpenAPI — project mẫu đầu tiên.

Đã thiết lập **API-001-Bookstore**, chạy API thật trên localhost và xác minh **28/28 ca HTTP**.
Đây là **1 project mẫu**, chưa phải Dataset 20 project. Mã nguồn giữ nguyên từ repository gốc.

## Chạy bằng Terminal trong VS Code

Mở thư mục `D:\OpenAPI_Dataset` trong VS Code. Chọn **Terminal → New Terminal**.

```powershell
cd D:\OpenAPI_Dataset
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-api.ps1
```

Mở trình duyệt:

- Swagger UI: <http://127.0.0.1:8000/docs>
- OpenAPI được ứng dụng sinh: <http://127.0.0.1:8000/openapi.json>
- Danh sách sách: <http://127.0.0.1:8000/books/>

Giữ terminal đang chạy mở. Nhấn **Ctrl+C** để dừng.
Không cần kích hoạt venv, sửa PATH hay đổi ExecutionPolicy của hệ thống.
Nếu cổng 8000 đang được dùng, thêm `-Port 8001` vào lệnh và mở URL cổng 8001.

## Thử CRUD trong Swagger UI

1. Mở `GET /books/` → **Try it out** → **Execute**. Database mới trả về `[]`.
2. Mở `POST /books/`, gửi JSON:

```json
{"title":"Romeo and Juliet","author":"William Shakespeare","year":1597,"isbn":"demo-001"}
```

3. Lấy ID từ **`data.id`** trong phản hồi, không mặc định ID bằng 1.
4. Gọi `GET /books/{book_id}` với ID đó.
5. Gọi `PUT /books/{book_id}` với đủ bốn trường. Gọi lại GET để kiểm tra dữ liệu đã sửa.
6. Gọi `DELETE /books/{book_id}`, sau đó GET cùng ID sẽ trả về 404.

Database dùng khi chạy thủ công là `api_projects/API-001-Bookstore/src/database.db`.
Nó lưu dữ liệu qua các lần khởi động, và được loại khỏi Git.

## Chạy lại kiểm thử

Mở terminal thứ hai:

```powershell
cd D:\OpenAPI_Dataset
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

Script tự chạy một server trên cổng trống, dùng database tạm riêng và dừng server sau kiểm thử.
Kết quả thành công: `API-001-Bookstore: 28/28 HTTP cases passed.`
Các lần chạy cập nhật bộ bằng chứng hiện tại. `verification.json` ghi trạng thái xác minh của lần chạy.

## Cấu trúc hồ sơ

| Đường dẫn | Nội dung |
|---|---|
| `api_projects/API-001-Bookstore/` | Source gốc, LICENSE MIT, venv; source được ghim bằng Git submodule |
| `ground_truth/API-001-Bookstore/openapi.3.0.3.json` | Đặc tả bổ sung đã đối chiếu source + 28 ca HTTP |
| `ground_truth/API-001-Bookstore/verification.json` | Commit, thời điểm UTC, trạng thái và giới hạn xác minh |
| `test_cases/API-001-Bookstore/cases.json` | 28 ca: CRUD, 404, 422, chuyển hướng, method không hỗ trợ |
| `results/API-001-Bookstore/openapi.generated.json` | OpenAPI 3.1.0 nguyên bản lấy qua HTTP từ ứng dụng |
| `results/API-001-Bookstore/http-results.json` | Request/response thực tế và SHA-256 các file nguồn |
| `results/API-001-Bookstore/summary.md` | Bảng kết quả PASS/FAIL |
| `results/API-001-Bookstore/server.log` | Log của server kiểm thử |
| `documentation/API-001-Bookstore.md` | Nguồn gốc, đối chiếu endpoint, lỗi đã biết và chuẩn hóa |
| `documentation/requirements.windows-py312.lock.txt` | Phiên bản đầy đủ đã cài trên Windows/Python 3.12 |
| `documentation/dataset.csv` | Danh mục project thực có |
| `documentation/EXPANSION.md` | Quy trình tiếp nhận project thứ 2 đến 20 |

## Tái lập trên máy khác

Tải repository kèm mã nguồn API đã ghim:

```powershell
git clone --recurse-submodules https://github.com/Hieu050506/NguyenHieu_OpenAI_DataSet.git
cd NguyenHieu_OpenAI_DataSet
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

`setup.ps1` mặc định tìm Python 3.12 ở `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`.
Nếu cài ở chỗ khác, truyền `-PythonExe 'C:\duong-dan\python.exe'`.
Lock này phục vụ tái lập project gốc, không phải khuyến nghị phiên bản để triển khai production.

## Repository GitHub

Repository Dataset: <https://github.com/Hieu050506/NguyenHieu_OpenAI_DataSet>.
Source upstream được liên kết bằng submodule và ghim commit để tái lập.
Không đưa `.venv`, database hay thông tin đăng nhập lên Git.
