# Sửa việc bật Markdown → PDF ngày 2026-10-09

Nguyên nhân tái hiện: `find_libreoffice()` trả về `None`, `check_dependencies('md_pdf')`
báo `missing_lo`, nên GUI khóa xuất PDF. Sau khi người dùng cho phép tải/cài,
đã cài LibreOffice 26.8.1.1 tại `C:\Program Files\LibreOffice`, mã thoát MSI 0.
Bộ cài được đối chiếu SHA-256 với danh sách mirror chính thức và chữ ký hợp lệ
của The Document Foundation; không khởi động lại máy.

Cập nhật GUI: **Chọn LibreOffice**, **Kiểm tra lại**, hướng dẫn Việt/Anh khi
thiếu Writer; bật các chế độ PDF sau khi kiểm tra lại mà không đóng cửa sổ.
Lưu vị trí cài riêng vào `%LOCALAPPDATA%\pdftomd\libreoffice.txt` để lần mở sau
vẫn nhận được, kể cả khi chạy qua `run.cmd`. Các nút bị khóa khi đang xử lý.

Các lệnh kiểm tra cuối đã chạy:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.cache/tests-pdf-final-fixed --tb=short
.\.venv\Scripts\ruff.exe check src tests tools
.\.venv\Scripts\ruff.exe format --check src tests tools
.\.venv\Scripts\python.exe .cache/verify_pdf_export.py
```

Kết quả: **50 passed**, không skip; Ruff check và format check đạt.
Hai test LibreOffice thật đã chạy. MD → PDF: tiếng Anh/Việt, ký tự © ± € → ≤ ≥,
Arial 15 pt đậm và Arial 11 pt, chữ đen. Word → PDF: hai trang, Times New Roman
18 pt, bảng, ảnh, header/footer. Luồng `jobs.run` thật cũng xuất được cả hai
PDF, giữ hash nguồn và công bố kết quả với cảnh báo kiểm tra bố cục.

Đã render bằng Poppler và xem cả trang PDF Markdown cùng hai trang PDF Word
tại `.cache/pdf-real`: không thấy chữ bị cắt/chồng, dấu Việt thiếu hoặc ảnh bị bỏ.
Đây là kiểm tra fixture trong dự án; chưa đối chiếu mọi tài liệu người dùng hoặc
bố cục render từ Microsoft Word. Cảnh báo kiểm tra PDF trong GUI vẫn được giữ.

Một số lần chạy trước gặp lỗi đọc thư viện Tk ngẫu nhiên, đã từng ghi nhận trong
báo cáo cũ. Một test mới cũng làm rò biến môi trường trỏ đến executable giả;
đã sửa cleanup của test. Lần chạy toàn bộ cuối ở trên đạt cả GUI và PDF thật.

Các mục bên dưới là báo cáo lịch sử trước khi cài LibreOffice.

# Cập nhật Markdown → Word/PDF ngày 2026-10-09

Hai converter đã có trong dự án. Cập nhật này thêm bộ lọc Markdown vào hộp chọn
tệp, tự chọn Markdown → Word khi chọn `.md` từ chế độ dành cho PDF/Word, giữ
chế độ MD → PDF đã chọn và hiển thị hướng dẫn định dạng bằng tiếng Việt/Anh.

Lệnh đã chạy trên mã cập nhật:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.cache/tests-md-verified --tb=short
.\.venv\Scripts\ruff.exe check src tests tools
.\.venv\Scripts\ruff.exe format --check src tests tools
```

Kết quả cuối: **45 passed, 2 skipped**; Ruff check và format check đều đạt.
Kiểm tra mới gồm chọn tệp `.MD` có dấu, giữ lựa chọn xuất PDF, đổi ngôn ngữ và
hướng dẫn theo chế độ trong Tk thật. Luồng MD → PDF được kiểm tra với backend
PDF giả cho nội dung Anh/Việt: DOCX trung gian thật, Arial 15/11 pt, chữ đậm/đen,
tránh ghi đè tên khác chữ hoa/thường, giữ nguồn và dọn tệp tạm khi lỗi/hủy.
PDF giả chỉ kiểm tra điều phối, không chứng minh chất lượng PDF thực tế.

Lần chạy đầu sau chỉnh sửa có một lỗi khởi tạo Tk (`tk.tcl` không đọc được
`ttk/panedwindow.tcl`); lần chạy lại toàn bộ suite ở trên đã đạt.
Chưa tìm thấy LibreOffice (`find_libreoffice()` trả về `None`), nên hai test xuất
PDF thực tế vẫn bị skip; chưa render/kiểm tra trực quan PDF xuất.
Thư mục hiện tại không có Git nên không tạo commit.

# Kết quả kiểm tra ngày 2026-10-08

Môi trường: Windows, Python 3.12.14, Tk 8.6.12, Arial có sẵn.
Phụ thuộc được khóa tại `requirements-lock.txt`.
MarkItDown local: phiên bản 0.1.8, HEAD tham chiếu
`4cc9fa17653d695d64fb9eee5b33d4de55ff84e8`.

Lệnh thực sự đã chạy:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.cache/tests-final3 --tb=short
.\.venv\Scripts\ruff.exe check src tests tools --fix --output-format concise
.\.venv\Scripts\ruff.exe format src tests tools
```

Kết quả: **36 passed, 2 skipped**. Ruff không còn lỗi.
Đã chạy `compileall` và `ruff format --check` ở bước kiểm tra trước đó.

Đã kiểm tra:

- PDF/DOCX Anh/Việt đối chiếu nội dung với API MarkItDown local, không sửa nguồn.
- PDF scan không có văn bản, PDF/DOCX hỏng, ảnh/header/footer DOCX có cảnh báo.
- H1–H6 và bold Arial 15 pt đậm đen; normal Arial 11 pt; A4, bảng, hyperlink,
  italic, ảnh local giữ tỷ lệ, code giữ khoảng trắng; kiểm tra cấu trúc DOCX.
- Danh sách có heading/blockquote/code ở đầu mục; footnote được từ chối thay vì
  bị mất định nghĩa. Arial thiếu glyph, ảnh thiếu/từ xa và MD không phải UTF-8.
- Lô có cả tệp tốt/lỗi, snapshot cố định, trùng tên khác chữ hoa/thường, nguồn
  thiếu/sai đuôi/.doc, thư mục rỗng, đường dẫn có dấu/khoảng trắng và độ dài tăng.
- Hủy giữa tệp không công bố tệp dở; hủy sau tệp hoàn tất giữ kết quả trước đó.
- Tình huống thiếu phụ thuộc, quyền ghi bị từ chối và công bố kết quả thất bại
  được kiểm tra với mock; không thay quyền thực tế trên tài liệu người dùng.
- Tk thật với scaling 2.0 trước khi tạo widget, vị trí nút ở các kích thước,
  đổi tiếng Anh, chế độ PDF bị tắt khi thiếu LibreOffice, xử lý nền và tiến độ.
- Đọc PDF hợp lệ/hỏng; tài nguyên external trong DOCX bị từ chối. Các nhánh
  LibreOffice exit lỗi, timeout, hủy, thiếu output và output hợp lệ được kiểm tra
  bằng tiến trình giả; đây không phải kiểm chứng LibreOffice thực tế.

Chưa nghiệm thu:

- Hai test `test_real_markdown_pdf` và `test_real_word_pdf` được skip vì chưa có
  LibreOffice. Không có PDF đầu ra LibreOffice để render và kiểm tra trực quan.
- Chưa đối chiếu bố cục với Microsoft Word, glyph trong PDF xuất, bảng/ảnh/font
  Word gốc hay đường dẫn vượt giới hạn truyền thống Windows.
- Chưa thao tác thủ công Tab/Enter, clipboard, file dialog, DPI đa màn hình hoặc
  xem trực quan DOCX trong Microsoft Word. Widget/queue được kiểm tra tự động.
- Chưa đóng gói EXE độc lập. Thư mục hiện tại không có Git nên không tạo commit.

Mã được rà soát độc lập theo skill requesting-code-review; hai lỗi đánh số danh
sách và kích thước tối thiểu ở DPI cao đã được sửa và có kiểm thử hồi quy.
Các giới hạn dùng tài liệu được ghi tại `README.md` và trong cảnh báo của GUI.
