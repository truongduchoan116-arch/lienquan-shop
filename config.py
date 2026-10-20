"""
=====================================================================
  CẤU HÌNH DUY NHẤT CỦA WEBSITE SHOP  (chỉ cần sửa file này)
=====================================================================

Quy ước:
  - Chuỗi rỗng ""  = chưa cấu hình  -> nút/mục đó TỰ ẨN, không có link giả.
  - "enabled": False tắt một mục dù đã có URL.
  - Chỉ điền thông tin THẬT. Không bịa số lượng đã bán, đánh giá, bảo hành.
  - Khi sửa, giữ nguyên dấu ngoặc kép "..." và dấu phẩy , ở cuối dòng.
"""

# ---------------------------------------------------------------------
# 1. WEBSITE
# ---------------------------------------------------------------------
SITE = {
    # Địa chỉ công khai của website, ví dụ "https://ten-ban.github.io/lienquan-shop".
    # Khi deploy bằng GitHub Actions thì tự lấy, không cần điền.
    # Cần có địa chỉ này thì mới tạo được mã QR, canonical và ảnh chia sẻ.
    "url": "https://hoan.github.io/lienquan-shop",
    "default_theme": "dark",  # "dark" | "light"
    "lang": "vi",
}

# ---------------------------------------------------------------------
# 2. THƯƠNG HIỆU SHOP
# ---------------------------------------------------------------------
SHOP = {
    "name": "DỊCH VỤ LIÊN QUÂN",            # TODO: tên shop thật
    "tagline": "Hỗ trợ game",
    "description": (
        "Kênh thông tin của shop: xem danh sách tài khoản, được tư vấn và liên hệ "
        "trực tiếp để hỏi trước khi giao dịch."
    ),
    "owner": "Trương Đức Hoan",                         # tên người bán, để trống nếu không công khai
    "logo": "",                          # "assets/logo.png" (đặt file trong static/assets/)
    "background_image": "",              # "assets/bg.jpg" (tuỳ chọn)
    # Màu thương hiệu (mã hex 6 ký tự)
    "colors": {
        "primary": "#d6203f",    # đỏ
        "secondary": "#7c3aed",  # tím
        "electric": "#38bdf8",   # xanh điện
        "gold": "#f5c542",       # vàng gold
    },
       
}

# ---------------------------------------------------------------------
# 3. KÊNH LIÊN HỆ & MẠNG XÃ HỘI
#    Chỉ điền URL thật. Để trống thì nút tự ẩn.
# ---------------------------------------------------------------------
CONTACT = {
    "messenger_url": {"enabled": True, "url": ""},   # ví dụ https://m.me/ten.trang
    "facebook_url":  {"enabled": True, "url": "https://www.facebook.com/hoancubu100cm?locale=vi_VN"},   # trang hoặc trang cá nhân
    "youtube_url":   {"enabled": True, "url": "https://www.youtube.com/@Gocnhinlienquan1"},
    "tiktok_url":    {"enabled": True, "url": "https://www.tiktok.com/@_dhoangaming_"},
    "email":         {"enabled": True, "url": "truongduchoan116@gmail.com"},   # điền địa chỉ email, ví dụ ban@gmail.com
}

# ---------------------------------------------------------------------
# 4. LIÊN KẾT NỔI BẬT  (tự ẩn nếu chưa có URL)
# ---------------------------------------------------------------------
FEATURED_LINKS = [
    {"id": "accounts", "icon": "list",   "label": "Kho tài khoản",       "description": "Xem danh sách tài khoản",   "url": "https://zalo.me/g/tneptb216", "enabled": True},
    {"id": "pricing",  "icon": "tag",    "label": "Bảng giá / sản phẩm", "description": "Giá và danh sách sản phẩm", "url": "", "enabled": True},
    {"id": "guide",    "icon": "book",   "label": "Hướng dẫn giao dịch", "description": "Quy trình từng bước",       "url": "", "enabled": True},
    {"id": "policy",   "icon": "shield", "label": "Chính sách hỗ trợ",   "description": "Điều kiện và hỗ trợ",       "url": "", "enabled": True},
]

# ---------------------------------------------------------------------
# 5. DỊCH VỤ
#    target:
#      "accounts" | "pricing" | "guide" | "policy"  -> dùng URL ở FEATURED_LINKS trên
#      "contact"  -> mở mục Liên hệ trong trang
#      "faq"      -> mở mục Câu hỏi thường gặp
#    Nếu URL đích chưa có thì nút sẽ mở kênh liên hệ chính (Messenger/Facebook);
#    nếu cũng chưa có thì nút ẩn, card vẫn hiện phần mô tả.
# ---------------------------------------------------------------------
SERVICES = [
    {"icon": "list",      "name": "Xem danh sách tài khoản",    "description": "Xem các tài khoản shop đang có.",                      "target": "accounts", "action": "Xem danh sách"},
    {"icon": "search",    "name": "Tư vấn chọn tài khoản",      "description": "Trao đổi nhu cầu để được gợi ý tài khoản phù hợp.",   "target": "contact",  "action": "Nhờ tư vấn"},
    {"icon": "headset",   "name": "Hỗ trợ trước giao dịch",     "description": "Hỏi mọi thông tin cần biết trước khi quyết định.",     "target": "contact",  "action": "Liên hệ hỏi"},
    {"icon": "book",      "name": "Hướng dẫn giao dịch",        "description": "Các bước giao dịch do shop công bố.",                  "target": "guide",    "action": "Xem hướng dẫn"},
    {"icon": "shield",    "name": "Làm chung sức liên quân",       "description": "Theo chính sách thực tế mà shop công bố.",             "target": "policy",   "action": "Xem chính sách"},
    {"icon": "help",      "name": "Câu hỏi thường gặp",         "description": "Giải đáp nhanh những thắc mắc phổ biến.",              "target": "faq",      "action": "Xem FAQ"},
]

# ---------------------------------------------------------------------
# 6. FAQ  (câu trả lời chỉ dựa trên thông tin đã cấu hình; sửa cho đúng với shop)
# ---------------------------------------------------------------------
FAQ = [
    {"q": "Làm thế nào để liên hệ shop?",
     "a": "Bạn dùng các nút trong mục Liên hệ (Messenger, Facebook hoặc Email)",
    {"q": "Xem danh sách sản phẩm ở đâu?",
     "a": "Nếu shop đã công bố kho tài khoản hoặc bảng giá thì sẽ có nút trong mục Liên kết nổi bật. Nếu chưa thấy, hãy liên hệ shop để được gửi danh sách."},
    {"q": "Làm thế nào để kiểm tra thông tin trước khi giao dịch?",
     "a": "Hãy hỏi shop trực tiếp mọi thông tin bạn cần và yêu cầu shop làm rõ trước khi quyết định. Không gửi mật khẩu hay mã OTP của bạn cho bất kỳ ai."},
    {"q": "Chính sách hỗ trợ được công bố ở đâu?",
     "a": "Nếu shop có trang chính sách thì nút sẽ hiện trong Liên kết nổi bật. Nếu chưa có, vui lòng hỏi shop về chính sách trước khi giao dịch."},
]

# ---------------------------------------------------------------------
# 7. FOOTER
# ---------------------------------------------------------------------
FOOTER = {
    "text": "Cảm ơn bạn đã dùng dịch vụ của tôi",   # dòng chữ thêm ở chân trang (tuỳ chọn)
    "disclaimer": "Đây là trang độc lập của shop, không phải website chính thức của Garena. "
                  "Liên Quân Mobile là thương hiệu của chủ sở hữu tương ứng.",
    "policy_url": "",   # liên kết chính sách ở chân trang (tuỳ chọn)
}
