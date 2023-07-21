# <center>Student-attendance-system-V2</center>

## Giải pháp điểm danh đầu giờ bằng nhận diện khuôn mặt sử dụng thuật toán deeplearning và trí tuệ nhân tạo

<table>
<tr>
<td width="48%">
  <a href="https://www.youtube.com/watch?v=J8AUoJnYRo8">
    <img src="/img/home.png" />
  </a>
</id>
</table>

### 1. Mô tả

Student-attendance-system-V2 là một hệ thống điểm danh tự động dựa trên nhận diện khuôn mặt sử dụng các thuật toán deeplearning và trí tuệ nhân tạo. Đây là phiên bản nâng cấp của phiên bản trước đó, nhằm tăng cường độ chính xác và hiệu suất của hệ thống.

#### Tính năng chính:

- Nhận diện khuôn mặt đa chiều: Hệ thống sử dụng thuật toán deeplearning để nhận diện khuôn mặt của học sinh từ nhiều góc độ, giúp tăng cường khả năng nhận dạng và giảm thiểu sai sót.
- Giao diện đa nền tảng: Student-attendance-system-V2 được xây dựng với giao diện hỗ trợ nhiều nền tảng, bao gồm Web, Application, Android và iOS, giúp người dùng dễ dàng sử dụng trên các thiết bị khác nhau.
- Tiết kiệm thời gian và công sức: Hệ thống tự động điểm danh giúp giáo viên tiết kiệm thời gian và công sức khi thực hiện điểm danh đầu giờ, tập trung nhiều hơn vào việc giảng dạy và chăm sóc học sinh.

### 2. Pipeline

#### Các bước chính trong quá trình điểm danh:

1. Thu thập dữ liệu: Hệ thống sử dụng camera để thu thập dữ liệu khuôn mặt của học sinh trong lớp học.
2. Tiền xử lý dữ liệu: Dữ liệu thu thập được sẽ được tiền xử lý để loại bỏ nhiễu và chuẩn hóa.
3. Xây dựng mô hình nhận diện khuôn mặt: Sử dụng thuật toán deeplearning, mô hình nhận diện khuôn mặt sẽ được xây dựng và huấn luyện trên dữ liệu đã được tiền xử lý.
4. Điểm danh tự động: Khi bắt đầu giờ học, hệ thống sẽ tiến hành điểm danh tự động dựa trên việc nhận diện khuôn mặt của học sinh trong lớp.
5. Ghi nhận dữ liệu điểm danh: Kết quả điểm danh sẽ được lưu trữ và ghi nhận trong hệ thống.

### 3. Cách cài đặt code

Để cài đặt và chạy hệ thống Student-attendance-system-V2, bạn cần thực hiện các bước sau:

Phiên bản [Python3.8](https://www.python.org/downloads/release/python-380/)

#### 1. Clone source code và setup môi trường
- Clone source code:

```
git clone https://github.com/baolongdev/Student-attendance-system-V2.git
cd Student-attendance-system-V2
```

- Setup môi trường:

```
pip install -r requirements.txt # Nếu máy có gpu
```
hoăc: 
```
pip install -r requirements.txt --no-cache-dir # Nếu không có gpu
```

#### 2. Deploy on web
```
streamlit run main.py
```
