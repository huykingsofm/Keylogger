# 1. Giới thiệu
Tên phần mềm: Keylogger  
Phân loại: Malware  
Mục đích: Sử dụng cho nghiên cứu và học tập. Dùng để cài đặt lên máy tính nạn nhân và ghi lại các sự kiện nhấn phím, sau đó gửi về email cho kẻ tấn công.  
*Lưu ý: Phần mềm chỉ sử dụng cho mục đích học tập.*

# 2. Chức năng
1. Phần mềm này có thể chạy ngầm mà không bị phát hiện bởi người dùng bình thường.
2. Chương trình sử dụng chức năng hook keyboard của thư viện `keyboard` để can thiệp vào hàng đợi sự kiện của máy tính, do đó không bỏ sót sự kiện dù người dùng nhấn phím quá nhanh hoặc sử dụng bàn phím ảo.
3. Phần mềm được trang bị tính năng ghi log thông minh, có thể nhận biết được người dùng đang nhấn combokey, backspace và thấy cửa sổ người dùng đang active. Từ đó tạo ra file log dễ hiểu và dễ khai thác.
4. Các file log được lưu ở những vị trí ngẫu nhiên và tên ngẫu nhiên, do đó khó bị phát hiện.
# 3. Hạn chế
1. Cần kết nối mạng để có thể gửi mail thông tin file log về attacker.
2. Không thể ẩn chương trình khỏi TaskManager.
3. Không ghi lại bất kỳ gì khác ngoài sự kiện bàn phím.

# 4. Hướng dẫn sử dụng
1. Thay đổi địa chỉ email của attacker trong file receiver.txt hoặc thay đổi code để chèn trực tiếp nó vào file python.
2. Biên dịch lại chương trình với pyinstaller (nếu thay đổi code), hướng dẫn tại mục 5.
3. Lây nhiễm file exe (và receiver.txt nếu không nhúng trực tiếp địa chỉ email vào file python) cho máy nạn nhân.
4. Khởi chạy chương trình keylogger.exe trên máy nạn nhân.
5. Chờ trong khoảng 30s (có thể thay đổi thời gian chờ trong file python) để nhận được email gửi từ máy nạn nhân.
6. Tắt keylogger bằng cách kill process của nó.

# Hướng dẫn tự biên dịch file exe
> `$ pip install -r requirements.txt`  
> `$ pyinstaller --onefile keylogger.py`