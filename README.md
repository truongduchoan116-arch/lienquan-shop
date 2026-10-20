# Shop Liên Quân – Link Hub (Python)

Website một trang cho shop, sinh bằng Python (Jinja2). Mọi thông tin nằm trong **config.py**.

## Chạy thử (Windows PowerShell)

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 build.py --serve
```
Mở http://localhost:8000. Sửa `config.py` rồi chạy lại để thấy thay đổi.

## Điền thông tin (config.py)

| Cần điền | Chỗ sửa |
|---|---|
| Tên shop, mô tả, tagline, logo, màu | `SHOP` |
| Messenger, Facebook, YouTube, TikTok, Email | `CONTACT` (để trống = nút tự ẩn) |
| Kho tài khoản, bảng giá, hướng dẫn, chính sách | `FEATURED_LINKS` (để trống = ẩn) |
| Danh sách dịch vụ | `SERVICES` |
| Câu hỏi thường gặp | `FAQ` (sửa cho đúng chính sách thật của shop) |
| Chân trang | `FOOTER` |

Logo/ảnh nền: chép file vào `static/assets/` rồi ghi `"assets/ten-file.png"`.
Mục có `"example": True` là nội dung mẫu, xoá dòng đó khi đã điền thật.

## Deploy (GitHub Pages, miễn phí)

1. Tạo repo mới trên GitHub (ví dụ `lienquan-shop`), đẩy toàn bộ file lên nhánh `main`
   (nhớ có thư mục `.github`).
2. Settings → Pages → Source: **GitHub Actions**.
3. Tab Actions: chờ workflow có dấu ✅. Link: `https://<user>.github.io/<repo>/`.
   Mã QR trên trang tự tạo theo link này khi build trên GitHub.

## Danh sách cần điền trước khi công khai

- [ ] Tên shop thật, mô tả, logo
- [ ] Ít nhất một kênh liên hệ thật (Messenger hoặc Facebook)
- [ ] YouTube / TikTok / Email nếu có
- [ ] Link kho tài khoản, bảng giá, hướng dẫn, chính sách (nếu có)
- [ ] Sửa FAQ đúng với cách shop làm việc thật
- [ ] Không ghi bảo hành/hoàn tiền nếu shop chưa có chính sách chính thức

Website không thu thập mật khẩu game, OTP hay dữ liệu khách; không có số liệu hay đánh giá giả.
