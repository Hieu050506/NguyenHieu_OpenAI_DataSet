# NguyenHieu_OpenAI_DataSet

Dataset OpenAPI — 20 project đã nhập mã nguồn, phân biệt rõ trạng thái kiểm thử.

| Trạng thái | Số lượng |
|---|---:|
| Project có mã nguồn và hồ sơ trong danh mục | **20** |
| Project đã kiểm thử HTTP và đối chiếu OpenAPI | **1 — Bookstore, 28/28 ca** |
| Project WFD mới nhập, chưa build/chạy HTTP trên máy này | **19** |

**Chưa có 20 project đã xác minh.** Trong 19 đặc tả WFD nguyên bản, kiểm tra cấu trúc cho kết quả
**8 hợp lệ, 11 có lỗi**. Chi tiết ở [báo cáo nhập WFD](results/wfd-import-audit.json).
Source WFD được giữ tại `sources/WFD`, ghim commit; mỗi project có đường dẫn source riêng trong `project.json`.

## Xem và quản lý 19 project WFD

```powershell
cd D:\OpenAPI_Dataset
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action List
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Audit
```

Danh sách đầy đủ: [documentation/DATASET_STATUS.md](documentation/DATASET_STATUS.md).
Hướng dẫn build/chạy từng project bằng Docker: [documentation/WFD.md](documentation/WFD.md).
Máy nhập dữ liệu chưa có Docker Desktop; script sẽ báo thiếu điều kiện thay vì tạo kết quả kiểm thử giả.

## Chạy bằng Terminal trong VS Code

Phần này chạy project **API-001-Bookstore** đã được thiết lập sẵn.

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
| `sources/WFD/` | Submodule WFD ghim commit, chứa source và cấu hình upstream |
| `api_projects/API-002-...` đến `API-020-...` | Hồ sơ và cấu hình build/run riêng cho 19 project WFD |
| `results/API-002-...` đến `API-020-...` | Đặc tả gốc và kết quả kiểm tra tĩnh; chưa có bằng chứng HTTP |

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
