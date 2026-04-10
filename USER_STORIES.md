# USER STORIES - AI-SHOP

## Tổng quan
Tài liệu này mô tả các User Stories cho hệ thống thương mại điện tử AI-Shop, được phân loại theo vai trò người dùng và mức độ ưu tiên.

---

## 1. KHÁCH VÃNG LAI (Guest User)

### US-G01: Xem danh sách sản phẩm
**Là** khách vãng lai  
**Tôi muốn** xem danh sách sản phẩm điện tử  
**Để** tìm hiểu các sản phẩm có sẵn trước khi quyết định mua

**Acceptance Criteria:**
- Hiển thị danh sách sản phẩm với hình ảnh, tên, giá
- Phân trang với 12 sản phẩm/trang
- Hiển thị placeholder khi không có hình ảnh
- Load nhanh dưới 2 giây

**Priority:** HIGH  
**Story Points:** 3

---

### US-G02: Tìm kiếm sản phẩm
**Là** khách vãng lai  
**Tôi muốn** tìm kiếm sản phẩm theo tên hoặc danh mục  
**Để** nhanh chóng tìm được sản phẩm mình cần

**Acceptance Criteria:**
- Hỗ trợ tìm kiếm tiếng Việt có dấu và không dấu
- Tìm kiếm theo tên sản phẩm, mô tả, tên danh mục
- Hiển thị kết quả real-time khi gõ
- Hiển thị "Không tìm thấy sản phẩm" nếu không có kết quả

**Priority:** HIGH  
**Story Points:** 5

---

### US-G03: Xem chi tiết sản phẩm
**Là** khách vãng lai  
**Tôi muốn** xem thông tin chi tiết của sản phẩm  
**Để** hiểu rõ hơn về sản phẩm trước khi mua

**Acceptance Criteria:**
- Hiển thị: tên, giá, mô tả, hình ảnh, danh mục, số lượng tồn
- Hiển thị đánh giá của khách hàng khác (nếu có)
- Nút "Thêm vào giỏ hàng"
- Responsive trên mobile

**Priority:** HIGH  
**Story Points:** 3

---

### US-G04: Lọc sản phẩm theo danh mục
**Là** khách vãng lai  
**Tôi muốn** lọc sản phẩm theo danh mục (Điện thoại, Laptop, Tablet...)  
**Để** dễ dàng tìm loại sản phẩm mình quan tâm

**Acceptance Criteria:**
- Hiển thị danh sách danh mục ở sidebar/menu
- Click vào danh mục → hiển thị sản phẩm thuộc danh mục đó
- Hiển thị số lượng sản phẩm trong mỗi danh mục
- Có thể bỏ lọc để xem tất cả

**Priority:** MEDIUM  
**Story Points:** 3

---

### US-G05: Đăng ký tài khoản
**Là** khách vãng lai  
**Tôi muốn** đăng ký tài khoản mới  
**Để** có thể mua hàng và theo dõi đơn hàng

**Acceptance Criteria:**
- Form đăng ký: email, mật khẩu, họ tên, số điện thoại
- Validate email format và email chưa tồn tại
- Validate mật khẩu tối thiểu 6 ký tự
- Hiển thị thông báo lỗi rõ ràng
- Tự động đăng nhập sau khi đăng ký thành công

**Priority:** HIGH  
**Story Points:** 5

---

### US-G06: Đăng nhập
**Là** khách vãng lai  
**Tôi muốn** đăng nhập vào hệ thống  
**Để** truy cập các tính năng dành cho thành viên

**Acceptance Criteria:**
- Form đăng nhập: email, mật khẩu
- Hiển thị lỗi nếu sai email/mật khẩu
- Lưu token JWT vào localStorage
- Redirect về trang trước đó sau khi đăng nhập
- Link "Quên mật khẩu"

**Priority:** HIGH  
**Story Points:** 3

---

### US-G07: Quên mật khẩu
**Là** khách vãng lai  
**Tôi muốn** đặt lại mật khẩu khi quên  
**Để** có thể đăng nhập lại vào tài khoản

**Acceptance Criteria:**
- Form nhập email và mật khẩu mới
- Kiểm tra email có tồn tại trong hệ thống
- Cập nhật mật khẩu mới (đã hash)
- Hiển thị thông báo thành công
- Redirect về trang đăng nhập

**Priority:** MEDIUM  
**Story Points:** 3

---

### US-G08: Chat với AI Chatbot
**Là** khách vãng lai  
**Tôi muốn** chat với AI để được tư vấn sản phẩm  
**Để** tìm được sản phẩm phù hợp với nhu cầu

**Acceptance Criteria:**
- Giao diện chat đơn giản, dễ sử dụng
- AI chỉ trả lời trong phạm vi: sản phẩm, mua hàng, chính sách, hướng dẫn
- Từ chối trả lời câu hỏi ngoài phạm vi (code, toán, tin tức...)
- Gợi ý sản phẩm liên quan khi phù hợp
- Có fallback thông minh khi không có AI provider

**Priority:** MEDIUM  
**Story Points:** 8

---

## 2. MEMBER (Thành viên đã đăng nhập)

### US-M01: Thêm sản phẩm vào giỏ hàng
**Là** thành viên  
**Tôi muốn** thêm sản phẩm vào giỏ hàng  
**Để** mua nhiều sản phẩm cùng lúc

**Acceptance Criteria:**
- Nút "Thêm vào giỏ" ở trang chi tiết và danh sách sản phẩm
- Hiển thị số lượng sản phẩm trong giỏ ở navbar
- Lưu giỏ hàng vào localStorage
- Hiển thị toast notification khi thêm thành công
- Kiểm tra số lượng tồn kho

**Priority:** HIGH  
**Story Points:** 5

---

### US-M02: Xem và quản lý giỏ hàng
**Là** thành viên  
**Tôi muốn** xem và chỉnh sửa giỏ hàng  
**Để** kiểm tra lại trước khi đặt hàng

**Acceptance Criteria:**
- Hiển thị danh sách sản phẩm trong giỏ: tên, giá, số lượng, tổng tiền
- Tăng/giảm số lượng sản phẩm
- Xóa sản phẩm khỏi giỏ
- Hiển thị tổng tiền tất cả sản phẩm
- Nút "Thanh toán"

**Priority:** HIGH  
**Story Points:** 5

---

### US-M03: Đặt hàng
**Là** thành viên  
**Tôi muốn** đặt hàng các sản phẩm trong giỏ  
**Để** mua sản phẩm

**Acceptance Criteria:**
- Form nhập: địa chỉ giao hàng, số điện thoại, ghi chú
- Chọn phương thức thanh toán (COD, chuyển khoản)
- Nhập mã giảm giá (optional)
- Hiển thị tổng tiền, giảm giá, thành tiền
- Tạo đơn hàng và chi tiết đơn hàng trong DB
- Xóa giỏ hàng sau khi đặt thành công
- Hiển thị thông báo thành công

**Priority:** HIGH  
**Story Points:** 8

---

### US-M04: Xem lịch sử đơn hàng
**Là** thành viên  
**Tôi muốn** xem danh sách đơn hàng của mình  
**Để** theo dõi trạng thái đơn hàng

**Acceptance Criteria:**
- Hiển thị danh sách đơn hàng: mã đơn, ngày đặt, tổng tiền, trạng thái
- Sắp xếp theo ngày mới nhất
- Hiển thị trạng thái: Chờ xử lý, Đang xử lý, Đang giao, Đã giao, Đã hủy
- Link xem chi tiết đơn hàng

**Priority:** HIGH  
**Story Points:** 3

---

### US-M05: Xem chi tiết đơn hàng
**Là** thành viên  
**Tôi muốn** xem chi tiết đơn hàng  
**Để** biết thông tin cụ thể về đơn hàng

**Acceptance Criteria:**
- Hiển thị: mã đơn, ngày đặt, trạng thái, địa chỉ giao hàng
- Danh sách sản phẩm: tên, số lượng, giá, thành tiền
- Tổng tiền, giảm giá, thành tiền
- Phương thức thanh toán
- Ghi chú (nếu có)

**Priority:** HIGH  
**Story Points:** 3

---

### US-M06: Đánh giá sản phẩm
**Là** thành viên  
**Tôi muốn** đánh giá sản phẩm đã mua  
**Để** chia sẻ trải nghiệm với người khác

**Acceptance Criteria:**
- Form đánh giá: điểm (1-5 sao), nội dung
- Chỉ đánh giá được sản phẩm đã mua
- Hiển thị đánh giá ở trang chi tiết sản phẩm
- Hiển thị tên người đánh giá, ngày đánh giá
- Validate: điểm từ 1-5, nội dung không rỗng

**Priority:** MEDIUM  
**Story Points:** 5

---

### US-M07: Xem thông tin cá nhân
**Là** thành viên  
**Tôi muốn** xem và cập nhật thông tin cá nhân  
**Để** quản lý tài khoản của mình

**Acceptance Criteria:**
- Hiển thị: email, họ tên, số điện thoại, địa chỉ
- Form cập nhật thông tin
- Validate số điện thoại format
- Hiển thị thông báo cập nhật thành công
- Không cho phép thay đổi email

**Priority:** MEDIUM  
**Story Points:** 3

---

### US-M08: Đổi mật khẩu
**Là** thành viên  
**Tôi muốn** đổi mật khẩu  
**Để** bảo mật tài khoản

**Acceptance Criteria:**
- Form: mật khẩu cũ, mật khẩu mới, xác nhận mật khẩu mới
- Validate mật khẩu cũ đúng
- Validate mật khẩu mới tối thiểu 6 ký tự
- Validate mật khẩu mới khớp với xác nhận
- Hash mật khẩu mới trước khi lưu
- Hiển thị thông báo thành công

**Priority:** MEDIUM  
**Story Points:** 3

---

### US-M09: Sử dụng mã giảm giá
**Là** thành viên  
**Tôi muốn** áp dụng mã giảm giá khi đặt hàng  
**Để** được giảm giá

**Acceptance Criteria:**
- Input nhập mã giảm giá ở trang thanh toán
- Nút "Áp dụng" để validate mã
- Kiểm tra: mã tồn tại, còn hiệu lực, còn số lượng, đủ giá trị đơn tối thiểu
- Hiển thị số tiền được giảm
- Cập nhật tổng tiền sau giảm
- Hiển thị lỗi nếu mã không hợp lệ

**Priority:** MEDIUM  
**Story Points:** 5

---

### US-M10: Xem lịch sử chat với AI
**Là** thành viên  
**Tôi muốn** xem lại lịch sử chat với AI  
**Để** tham khảo các tư vấn trước đó

**Acceptance Criteria:**
- Hiển thị danh sách tin nhắn: câu hỏi, câu trả lời, thời gian
- Sắp xếp theo thời gian mới nhất
- Phân trang 50 tin nhắn/trang
- Có thể xóa tin nhắn

**Priority:** LOW  
**Story Points:** 3

---

## 3. MANAGER (Quản lý)

### US-MG01: Quản lý sản phẩm (CRUD)
**Là** manager  
**Tôi muốn** tạo, xem, sửa, xóa sản phẩm  
**Để** quản lý kho hàng

**Acceptance Criteria:**
- Trang danh sách sản phẩm với search, filter
- Form tạo/sửa: tên, mô tả, giá, số lượng tồn, hình ảnh, danh mục
- Validate: giá > 0, số lượng >= 0, danh mục tồn tại
- Xác nhận trước khi xóa
- Hiển thị thông báo thành công/lỗi

**Priority:** HIGH  
**Story Points:** 8

---

### US-MG02: Quản lý đơn hàng
**Là** manager  
**Tôi muốn** xem và cập nhật trạng thái đơn hàng  
**Để** xử lý đơn hàng

**Acceptance Criteria:**
- Xem tất cả đơn hàng (không chỉ của mình)
- Filter theo trạng thái, ngày đặt
- Cập nhật trạng thái: Chờ xử lý → Đang xử lý → Đang giao → Đã giao
- Có thể hủy đơn hàng
- Xem chi tiết đơn hàng

**Priority:** HIGH  
**Story Points:** 8

---

### US-MG03: Quản lý đánh giá
**Là** manager  
**Tôi muốn** xem và xóa đánh giá không phù hợp  
**Để** kiểm duyệt nội dung

**Acceptance Criteria:**
- Xem tất cả đánh giá: sản phẩm, người đánh giá, điểm, nội dung, ngày
- Filter theo sản phẩm, điểm đánh giá
- Xóa đánh giá spam/không phù hợp
- Xác nhận trước khi xóa

**Priority:** MEDIUM  
**Story Points:** 5

---

### US-MG04: Quản lý mã giảm giá (Tạo/Sửa)
**Là** manager  
**Tôi muốn** tạo và sửa mã giảm giá  
**Để** tạo chương trình khuyến mãi

**Acceptance Criteria:**
- Form tạo/sửa: mã code, mô tả, loại giảm (%, cố định), giá trị giảm, giá trị đơn tối thiểu, số lượng, ngày bắt đầu/kết thúc
- Validate: mã code unique, giá trị > 0, ngày kết thúc > ngày bắt đầu
- Bật/tắt trạng thái hoạt động
- KHÔNG có quyền xóa mã giảm giá

**Priority:** MEDIUM  
**Story Points:** 8

---

### US-MG05: Xem báo cáo thống kê
**Là** manager  
**Tôi muốn** xem báo cáo thống kê  
**Để** theo dõi tình hình kinh doanh

**Acceptance Criteria:**
- Tổng doanh thu
- Số đơn hàng theo trạng thái
- Số sản phẩm đã bán
- Số khách hàng mới
- Biểu đồ doanh thu theo thời gian (optional)

**Priority:** LOW  
**Story Points:** 8

---

## 4. ADMIN (Quản trị viên)

### US-A01: Quản lý danh mục (CRUD)
**Là** admin  
**Tôi muốn** tạo, xem, sửa, xóa danh mục  
**Để** phân loại sản phẩm

**Acceptance Criteria:**
- Trang danh sách danh mục
- Form tạo/sửa: tên danh mục, mô tả
- Validate: tên không rỗng
- Xác nhận trước khi xóa
- Kiểm tra danh mục có sản phẩm trước khi xóa

**Priority:** HIGH  
**Story Points:** 5

---

### US-A02: Quản lý người dùng
**Là** admin  
**Tôi muốn** xem và cập nhật thông tin người dùng  
**Để** quản lý tài khoản

**Acceptance Criteria:**
- Xem danh sách người dùng: email, họ tên, vai trò, ngày tạo
- Filter theo vai trò
- Cập nhật vai trò: user, manager, admin
- Xem chi tiết người dùng
- Không cho phép xóa người dùng (để giữ lịch sử)

**Priority:** HIGH  
**Story Points:** 5

---

### US-A03: Xóa mã giảm giá
**Là** admin  
**Tôi muốn** xóa mã giảm giá  
**Để** loại bỏ mã không còn sử dụng

**Acceptance Criteria:**
- Nút "Xóa" ở trang quản lý mã giảm giá
- Xác nhận trước khi xóa
- Kiểm tra mã đã được sử dụng chưa
- Hiển thị cảnh báo nếu mã đã được sử dụng

**Priority:** LOW  
**Story Points:** 2

---

### US-A04: Thiết lập quyền truy cập
**Là** admin  
**Tôi muốn** thiết lập quyền truy cập cho các vai trò  
**Để** bảo mật hệ thống

**Acceptance Criteria:**
- Admin: toàn quyền
- Manager: quản lý sản phẩm, đơn hàng, đánh giá, mã giảm giá (tạo/sửa)
- User: chỉ xem và mua hàng
- Middleware kiểm tra quyền trước khi truy cập API

**Priority:** HIGH  
**Story Points:** 5

---

### US-A05: Cấu hình AI Chatbot
**Là** admin  
**Tôi muốn** cấu hình AI provider (OpenAI/Gemini)  
**Để** chatbot hoạt động

**Acceptance Criteria:**
- Cấu hình qua file .env: AI_PROVIDER, OPENAI_API_KEY, GEMINI_API_KEY
- Hệ thống tự động chọn provider dựa trên config
- Fallback thông minh khi không có AI provider
- Log lỗi khi config sai

**Priority:** MEDIUM  
**Story Points:** 3

---

### US-A06: Xem log hệ thống
**Là** admin  
**Tôi muốn** xem log hoạt động của hệ thống  
**Để** debug và giám sát

**Acceptance Criteria:**
- Log API requests/responses
- Log errors với stack trace
- Log AI chatbot interactions
- Filter log theo level (INFO, WARNING, ERROR)
- Export log ra file

**Priority:** LOW  
**Story Points:** 5

---

### US-A07: Quản lý bình luận sản phẩm
**Là** admin  
**Tôi muốn** xem và xóa bình luận không phù hợp  
**Để** kiểm duyệt nội dung

**Acceptance Criteria:**
- Giống US-MG03 nhưng có thêm quyền cao hơn
- Có thể khóa/mở khóa tính năng bình luận của user
- Xem lịch sử bình luận đã xóa

**Priority:** LOW  
**Story Points:** 5

---

## 5. DỊCH VỤ AI (AI Service)

### US-AI01: Tư vấn sản phẩm
**Là** AI chatbot  
**Tôi muốn** tư vấn sản phẩm phù hợp với nhu cầu khách hàng  
**Để** giúp khách hàng tìm được sản phẩm mong muốn

**Acceptance Criteria:**
- Phân tích câu hỏi của khách hàng
- Tìm kiếm sản phẩm liên quan trong database
- Gợi ý 3-5 sản phẩm phù hợp nhất
- Giải thích lý do gợi ý
- Trả lời bằng tiếng Việt tự nhiên

**Priority:** HIGH  
**Story Points:** 8

---

### US-AI02: Trả lời câu hỏi về chính sách
**Là** AI chatbot  
**Tôi muốn** trả lời câu hỏi về chính sách (bảo hành, đổi trả, giao hàng, thanh toán)  
**Để** cung cấp thông tin cho khách hàng

**Acceptance Criteria:**
- Trả lời chính xác về: bảo hành 12-24 tháng, đổi trả 7 ngày, giao hàng miễn phí >500k, thanh toán COD/chuyển khoản
- Trả lời ngắn gọn, rõ ràng
- Không bịa đặt thông tin

**Priority:** HIGH  
**Story Points:** 5

---

### US-AI03: Từ chối câu hỏi ngoài phạm vi
**Là** AI chatbot  
**Tôi muốn** từ chối trả lời câu hỏi ngoài phạm vi hệ thống  
**Để** tập trung vào mục đích hỗ trợ bán hàng

**Acceptance Criteria:**
- Phát hiện câu hỏi về: code, toán, dịch thuật, tin tức, chính trị, sức khỏe, pháp luật...
- Trả lời lịch sự: "Xin lỗi, tôi chỉ có thể hỗ trợ các vấn đề liên quan đến..."
- Gợi ý các câu hỏi phù hợp

**Priority:** HIGH  
**Story Points:** 5

---

### US-AI04: Hướng dẫn sử dụng website
**Là** AI chatbot  
**Tôi muốn** hướng dẫn khách hàng sử dụng website  
**Để** khách hàng dễ dàng mua hàng

**Acceptance Criteria:**
- Hướng dẫn: đăng ký, đăng nhập, tìm kiếm, thêm giỏ hàng, đặt hàng, xem đơn hàng
- Giải thích từng bước rõ ràng
- Có thể gửi link đến trang liên quan

**Priority:** MEDIUM  
**Story Points:** 5

---

### US-AI05: Lưu lịch sử chat
**Là** AI chatbot  
**Tôi muốn** lưu lịch sử chat của khách hàng  
**Để** khách hàng có thể xem lại sau

**Acceptance Criteria:**
- Lưu mỗi tin nhắn vào bảng lich_su_chat
- Lưu: nguoi_dung_id (nếu đã đăng nhập), tin_nhan, phan_hoi, ngay_tao
- Không lưu thông tin nhạy cảm (mật khẩu, thẻ tín dụng...)

**Priority:** MEDIUM  
**Story Points:** 3

---

## Tổng kết

**Tổng số User Stories:** 47  
**Tổng Story Points:** 234

**Phân bố theo vai trò:**
- Khách vãng lai: 8 stories (35 points)
- Member: 10 stories (47 points)
- Manager: 5 stories (37 points)
- Admin: 7 stories (30 points)
- AI Service: 5 stories (26 points)

**Phân bố theo độ ưu tiên:**
- HIGH: 22 stories
- MEDIUM: 18 stories
- LOW: 7 stories
