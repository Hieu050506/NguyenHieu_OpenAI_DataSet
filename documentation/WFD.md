# Chạy và hoàn thiện 19 project WFD

Dataset đã nhập API-002 đến API-020 từ <https://github.com/WebFuzzing/Dataset>,
ghim commit `915859080da033fc36feae54bab3ad4a7b04e872`.
Đây là **19 project mới có source và hồ sơ, chưa được xác minh bằng HTTP trên máy này**.

## Đã có những gì?

- Mã nguồn Java/Kotlin thực tế trong `sources/WFD/<source_path>`, không phải 19 thư mục trống.
- Nguồn gốc, commit bộ sưu tập, license do WFD ghi nhận, link tới các file license/notice gốc.
- Bản đặc tả nguyên bản `results/<id>/openapi.upstream.json`.
- SHA-256 đặc tả được tính sau khi chuẩn hóa CRLF thành LF để so sánh được trên Windows/Linux.
  Ngoài cách xuống dòng, nội dung đặc tả được giữ nguyên.
- Danh mục operation, kế hoạch GET smoke ban đầu và cấu hình Docker Compose riêng.
- Báo cáo kiểm tra tĩnh: source/hash/đường dẫn đạt 19/19; đặc tả 8 hợp lệ và 11 có lỗi.
- `ground_truth/<id>/verification.json` ghi **not_verified**. Chưa tạo bản OpenAPI 3.0.3 giả định đã đúng.

License của WFD không thay thế license của từng project. Các file thông báo gốc được giữ trong submodule;
`project.json` chỉ ghi nhận thông tin từ WFD, không phải đánh giá pháp lý độc lập.
Hai bản source `features-service` và `scout-api` không có file license/notice riêng trong snapshot WFD;
hồ sơ đánh dấu `wfd_declaration_only_requires_review`, không coi việc kiểm tra giấy phép của hai project này đã hoàn tất.

## 1. Cài điều kiện chạy Docker trên Windows

Máy nhập Dataset chưa tìm thấy Docker CLI. Xem hướng dẫn chính thức:
<https://docs.docker.com/desktop/setup/install/windows-install/>.

Cài Docker Desktop, mở ứng dụng và chờ Docker sẵn sàng ở chế độ **Linux containers**.
Nếu máy yêu cầu cập nhật WSL hoặc khởi động lại, hoàn tất bước đó trước khi build.
Không cần cài riêng bốn phiên bản Java trên Windows: cấu hình build dùng JDK trong container.
Build lần đầu tải image và dependencies; thời gian và dung lượng phụ thuộc project.

Kiểm tra trong terminal mới:

```powershell
docker version
docker compose version
docker info --format '{{.OSType}}'
```

Dòng cuối phải trả về `linux`. Chỉ có Docker CLI mà chưa chạy daemon thì chưa đủ.

## 2. Xem project và kiểm tra dữ liệu đã tải

```powershell
cd D:\OpenAPI_Dataset
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action List
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Audit
```

Audit không chạy HTTP. Kết quả báo rõ các đặc tả còn lỗi, không coi chúng đã đạt chỉ vì file tồn tại.
Khi clone GitHub phải tải submodule:

```powershell
git submodule update --init --recursive
```

## 3. Thử Swagger Petstore trước

Swagger Petstore có đặc tả gốc hợp lệ về cấu trúc, nên dùng làm project đầu tiên để thử quy trình Docker.
Các lệnh build/run dưới đây đã được chuẩn bị và kiểm tra tĩnh, **chưa chạy qua Docker trên máy nhập**.

```powershell
cd D:\OpenAPI_Dataset
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Build -Project API-019-swagger-petstore
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Start -Project API-019-swagger-petstore
```

Sau khi API khởi động, đặc tả dự kiến theo WFD driver tại:
<http://127.0.0.1:8119/api/v3/openapi.json>.
Nếu build hoặc startup lỗi, giữ log để sửa nguyên nhân trước khi chạy test.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Smoke -Project API-019-swagger-petstore
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Stop -Project API-019-swagger-petstore
```

Đổi ID bằng một project khác từ lệnh List để áp dụng cùng quy trình.
Mỗi project có cổng HTTP riêng 8102–8120, cổng auth riêng nếu cần. Các cổng host được bind vào loopback.
Chỉ nên bắt đầu một project để xác minh quy trình và tài nguyên trước khi chạy nhiều project.

## 4. Từ smoke test đến Ground Truth

Smoke test chỉ thử GET không cần tham số bắt buộc theo đặc tả gốc. Nó không thay thế CRUD đầy đủ.
Các endpoint khai báo yêu cầu xác thực sẽ bị ghi skipped; dùng fixture cục bộ từ WFD/auth sau khi kiểm tra source.
Một số project có thể không có GET đủ điều kiện; khi đó không được báo smoke pass.
Client chỉ gửi request tới localhost, không gửi vào server công cộng ghi trong đặc tả upstream.

Để một project được tính là verified:

1. Build và khởi động thành công, lưu log và phiên bản môi trường.
2. Đối chiếu bản spec gốc với source và phản hồi thực tế; sửa lỗi có ghi lại lý do.
3. Tạo ca thành công, dữ liệu sai, ID không tồn tại, xác thực, và toàn bộ vòng đời dữ liệu phù hợp API.
4. Chuẩn hóa OpenAPI 3.0.3 nếu nghiên cứu yêu cầu; xác thực schema và response.
5. Lưu request/response, review độc lập và cập nhật trạng thái trong danh mục.

## Bằng chứng được lưu

- `static-audit.json`: kiểm tra source và cấu trúc spec.
- `runtime-status.json`: chưa chạy / đã yêu cầu khởi động container; không tự coi là API khỏe.
- `build-status.json`: chỉ được tạo khi build thật hoàn tất và có JAR.
- `smoke-results.json`: chỉ được tạo khi chạy smoke thật; không đổi Ground Truth sang verified.
- `traffic/`: log proxy cục bộ, được loại khỏi Git.

File kết quả runtime có thể chứa dữ liệu thử; kiểm tra nội dung trước khi chủ động thêm vào Git.
