# Tiếp nhận project thứ 2 đến 20

Hiện có **20 project có mã nguồn và hồ sơ**: API-001-Bookstore đã kiểm thử,
API-002 đến API-020 được nhập từ WFD và **chưa xác minh runtime**.
Xem `WFD.md`, `DATASET_STATUS.md` và `dataset.csv` để phân biệt các trạng thái.
Phân bổ giữa ba đề tài cần được nhóm xác nhận theo mục tiêu nghiên cứu; tài liệu hiện tại chưa nêu tên ba đề tài.

Với mỗi repository mới:

1. Ghi URL, commit, license; kiểm tra quyền tái sử dụng và giữ thông tin bản quyền.
2. Đặt mã API-002-..., API-003-...; source được ghim commit bằng submodule.
3. Đọc README, kiểm tra dependencies, database, cấu hình và cách chạy thực tế.
4. Tạo môi trường riêng, chạy được trên máy và ghi phiên bản đủ để tái lập.
5. Lưu đặc tả gốc vào results; không coi đặc tả sinh tự động là Ground Truth đã xác minh.
6. Đối chiếu từng operation: method, path, parameter, request body, status code, response và lỗi.
7. Chuẩn hóa OpenAPI theo phiên bản nghiên cứu, giữ lịch sử biến đổi; xác thực cấu trúc bằng validator.
8. Tạo ca HTTP cho luồng thành công và các lỗi trọng yếu; dùng dữ liệu thử, database hoặc môi trường tạm.
9. Lưu request/response, log, SHA-256 source, kết quả và giới hạn. Chỉ đánh dấu verified khi kiểm tra đạt.
10. Cho thành viên khác tái lập; ghi kết quả review. Cập nhật dataset.csv sau khi hồ sơ đầy đủ.

Mỗi project phải có đủ source, ground_truth, test_cases, results và documentation.
Danh mục cần phân biệt `candidate`, `imported_not_runtime_verified`, `running`, `verified_with_known_limitations`, `reviewed`, `rejected`.
Số lượng project đã xác minh được tính bằng số hồ sơ đầy đủ và đạt kiểm tra, không phải số repository đã tải.
