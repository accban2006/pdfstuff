# Chuyển đổi tài liệu trên Windows

Ứng dụng desktop đơn giản bằng Python 3.12 và Tkinter/ttk, theo [AGENTS.md](AGENTS.md)
và bố cục [Untitled.png](Untitled.png). Giao diện mặc định tiếng Việt, có English.
Tài liệu được xử lý trên máy; không có tài khoản, cloud, OCR hay dịch nội dung.

Xem **[Hướng dẫn chạy chi tiết](HUONG_DAN_CHAY.md)** để chạy trên máy hiện tại,
cài trên máy khác, bật xuất PDF, thử tài liệu mẫu và xử lý lỗi thường gặp.

## Chạy ngay trên máy hiện tại

Nhấp đúp **`run.cmd`** ở thư mục dự án. Môi trường `.venv` đã được tạo và cài thư viện.
Hoặc mở PowerShell tại thư mục dự án:

```powershell
.\.venv\Scripts\python.exe -m pdftomd
```

Đây là ứng dụng chạy từ mã nguồn. Chưa đóng gói EXE độc lập bằng PyInstaller.
Môi trường hiện tại dùng Python 3.12.14 đi kèm Codex; khi chuyển sang máy khác,
cần tạo lại `.venv` bằng bản Python 3.12 có Tkinter của máy đó.

## Cách dùng

1. Chọn **Tệp hoặc thư mục nguồn**, hoặc dán đường dẫn máy tính vào ô đầu tiên.
2. Chọn **Thư mục lưu kết quả**. Có thể nhập thư mục mới; ứng dụng thông báo khi tạo.
3. Chọn một chế độ rồi bấm **Chuyển đổi**. Enter kích hoạt thao tác; Tab chuyển giữa các ô/nút.
4. Theo dõi tiến độ. Một tệp lỗi không dừng những tệp khác.
5. Sau khi xong, xem số thành công/cảnh báo/lỗi/hủy. **Xem chi tiết** hiển thị lý do
   và đường dẫn từng kết quả; **Mở thư mục kết quả** mở thư mục trong Explorer.

Để chuyển file `.md`, dùng bộ lọc **Markdown (.md)** trong **Chọn tệp**.
Nếu đang ở chế độ dành cho PDF/Word, chọn file MD sẽ tự chuyển sang
**Markdown → Word** và xuất `.docx`. Có thể đổi sang **Markdown → PDF** để xuất
`.pdf` khi có LibreOffice Writer. Nếu đã chọn MD → Word/PDF, ứng dụng giữ lựa
chọn đó. Với đường dẫn dán trực tiếp hoặc nguồn là thư mục, chọn chế độ thủ công.

Với nguồn là thư mục, chỉ xử lý tệp phù hợp ở cấp hiện tại; không duyệt thư mục con.
Bỏ qua tệp khóa `~$...`, tệp bắt đầu bằng `~` hoặc `.`. Danh sách nguồn được chụp
trước khi chạy. Nguồn không bị sửa. Kết quả trùng tên được lưu thành `ten (1).md`,
`ten (2).md`…; xét cả khác biệt chữ hoa/thường.

**Hủy** dừng hàng đợi; MarkItDown cần hoàn tất tệp đang chạy trước khi hủy.
Kết quả của tệp đang bị hủy không được công bố, các kết quả trước đó được giữ lại.
Đóng cửa sổ đang chạy cũng yêu cầu hủy và chờ backend dừng.

## Các chế độ và tình trạng kiểm chứng

| Chế độ | Backend | Kiểm chứng trên máy hiện tại |
| --- | --- | --- |
| PDF → Markdown | MarkItDown local | Fixture Anh/Việt, bảng đơn giản, ký tự, so sánh nội dung với API local |
| Word → Markdown | MarkItDown local | Fixture Anh/Việt, heading, danh sách, bảng, ký tự; so sánh API local |
| Markdown → Word | markdown-it-py + python-docx | Kiểm tra cấu trúc DOCX, H1–H6, đậm/nghiêng, bảng, danh sách, link, ảnh, code |
| Markdown → PDF | Chính DOCX của chế độ trên → LibreOffice | Đã kiểm thử xuất và render fixture Anh/Việt với LibreOffice 26.8.1.1 |
| Word → PDF | LibreOffice trực tiếp từ bản sao DOCX | Đã kiểm thử fixture hai trang, font, bảng, ảnh và header/footer |

Hai chế độ xuất PDF bị vô hiệu hóa khi chưa tìm thấy LibreOffice. Các kết quả có
giới hạn đã biết được gắn **cảnh báo**, không tính là thành công đầy đủ.
Không coi việc tạo được tệp là bằng chứng giữ đủ nội dung/bố cục.

## Định dạng Markdown → Word/PDF

- H1–H6 giữ cấp heading, cùng Arial **15 pt, đậm, đen**.
- Chữ đậm trong đoạn, bảng và danh sách: Arial **15 pt, đậm, đen**.
- Chữ thường: Arial **11 pt, đen**. Chữ nghiêng và đích liên kết được giữ.
- A4, lề 2 cm. Bảng có độ rộng vừa vùng nội dung, ảnh giữ tỷ lệ và thu nhỏ khi cần.
- Code giữ ký tự, xuống dòng và khoảng trắng; không thực thi.
- Ảnh local được tìm tương đối theo thư mục của Markdown. Ảnh thiếu/hỏng/từ xa
  làm tệp thất bại thay vì bỏ ảnh âm thầm.
- Kiểm tra bốn font Arial và glyph của chữ xuất trước khi lưu DOCX; ký tự thiếu
  được báo bằng mã Unicode. Không tự thay font. PDF từ Markdown được kiểm tra
  tên font của chữ trích xuất; nghiệm thu trực quan vẫn cần thực hiện.

Markdown đọc UTF-8 hoặc UTF-8 BOM; không bỏ qua lỗi giải mã. Markdown xuất từ
MarkItDown chỉ chuẩn hóa UTF-8 và xuống dòng, không sửa văn bản.

## Cài phụ thuộc trên môi trường phát triển khác

Cài Python **3.12** có Tkinter trước. Không dùng `.venv` sao chép từ máy khác.
Tại PowerShell ở gốc dự án:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -c requirements-lock.txt -e ".[dev]" -e "D:\appdata\markit\packages\markitdown[pdf,docx]"
```

Nếu dùng `uv`, thay dòng cài bằng:

```powershell
uv pip install --python .venv\Scripts\python.exe -c requirements-lock.txt -e ".[dev]" -e "D:\appdata\markit\packages\markitdown[pdf,docx]"
```

Chỉ cài extras `pdf,docx`, không `[all]`. `requirements-lock.txt` khóa toàn bộ
phiên bản đã kiểm thử. MarkItDown local báo phiên bản **0.1.8**, tham chiếu HEAD
**4cc9fa17653d695d64fb9eee5b33d4de55ff84e8**. Mã ứng dụng không chứa đường dẫn
MarkItDown bắt buộc; đường dẫn trên chỉ dùng khi cài editable để phát triển.

Khi phát hành cho máy khác, cần dựng và đóng gói wheel từ đúng nguồn MarkItDown
đã kiểm thử; không thay bằng bản PyPI chỉ vì cùng số phiên bản. Đóng gói Windows
`onedir` là bước phát hành riêng; không đưa `.venv`, skill, cache, fixture hay cả
kho MarkItDown vào ứng dụng.

## Bật xuất PDF

Cài LibreOffice Writer từ [trang chính thức](https://www.libreoffice.org/download/),
rồi bấm **Kiểm tra lại** ngay trong cửa sổ; không cần đóng ứng dụng. Ứng dụng không
tự tải/cài LibreOffice. Nếu cài ở nơi khác, bấm **Chọn LibreOffice**, chọn
`program\soffice.exe` hoặc `soffice.com`. Đường dẫn được lưu tại
`%LOCALAPPDATA%\pdftomd\libreoffice.txt` cho các lần mở sau bằng `run.cmd`.
Các nút bị khóa khi đang chuyển đổi.

Ứng dụng cũng tìm `soffice` qua PATH, các thư mục cài thông thường hoặc biến môi trường:

```powershell
$env:PDFTOMD_LIBREOFFICE = 'C:\Program Files\LibreOffice\program\soffice.exe'
.\.venv\Scripts\python.exe -m pdftomd
```

LibreOffice dùng profile tạm riêng, cửa sổ ẩn và thời gian chờ 120 giây mỗi tệp.
Ứng dụng kiểm tra mã thoát và đọc PDF thực tế trước khi công bố. Word → PDF không
đi qua Markdown và không áp font Arial lên Word nguồn. DOCX có tài nguyên liên kết
ngoài (trừ hyperlink thông thường) phải nhúng tài nguyên trước khi xuất PDF.

## Giới hạn cần biết

- Không hỗ trợ Word `.doc`, PDF scan/OCR, footnote/math/plugin Markdown chuyên biệt.
  CommonMark, bảng và gạch ngang chữ được hỗ trợ; cú pháp mở rộng có thể chỉ được
  giữ dưới dạng chữ thường. Định nghĩa footnote bị từ chối để tránh bị parser bỏ
  mất nội dung; tham chiếu footnote/math `$$` được cảnh báo. HTML được giữ nguyên
  dưới dạng chữ kèm cảnh báo.
- PDF → MD không giữ bố cục/font từng trang. MarkItDown có thể không giữ heading,
  ảnh hoặc cấu trúc PDF phức tạp; kết quả luôn có cảnh báo để đối chiếu.
- DOCX → MD có thể mất header/footer, ảnh nhúng, text box và tracked changes.
  Ảnh của bản MarkItDown này có thể là placeholder data URI. Không tự sửa hoặc
  bổ sung nội dung vào Markdown; giao diện báo khi thấy các thành phần này.
- DOCX có bảng lồng, ô gộp, công thức, nhiều cột hoặc bố cục phức tạp chưa được
  nghiệm thu đầy đủ. Font/bố cục Word không tồn tại trong Markdown.
- Danh sách lồng trên 9 cấp bị từ chối rõ. Link bao quanh ảnh chưa được giữ và
  có cảnh báo. Bảng rất rộng, code dài và đoạn không có điểm ngắt cần kiểm tra
  trực quan trong Word/PDF trước khi sử dụng.
- Đã kiểm tra dấu Việt và © ± € → ≤ ≥ trong DOCX, © ± € trong fixture PDF/Word
  đầu vào. Không tuyên bố hỗ trợ mọi ký tự; emoji thiếu trong Arial bị từ chối.
- Đường dẫn dài phụ thuộc Windows và thư viện; kiểm thử hiện tại dùng đường dẫn
  dưới ngưỡng truyền thống 260 ký tự. Lỗi đường dẫn/quyền được báo, không ghi dở.
- Đã xem PDF fixture xuất bằng LibreOffice; chưa đối chiếu độ trung thực bố cục so với
  Microsoft Word hoặc thao tác thủ công bằng bàn phím trên màn hình nhiều DPI.
  Có kiểm tra tự động vị trí widget ở scaling 2.0, đổi ngôn ngữ và vòng lặp GUI.

## Kiểm thử và cấu trúc mã

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.cache\pytest-current
.\.venv\Scripts\ruff.exe check src tests tools
.\.venv\Scripts\ruff.exe format --check src tests tools
```

Fixture là tài liệu tổng hợp Anh/Việt, không có tài liệu người dùng.
`tools/generate_fixtures.py` tạo lại fixture với `reportlab` và `python-docx` ở
môi trường công cụ phát triển; ReportLab không phải phụ thuộc chạy ứng dụng.
Các test PDF thực tế sẽ tự chạy khi có LibreOffice, nhưng vẫn cần render và
đối chiếu trực quan trước khi xác nhận nghiệm thu hai chế độ PDF.

| Module | Trách nhiệm |
| --- | --- |
| `gui.py` | Thu thập lựa chọn, trạng thái, queue/after và thao tác trên luồng chính |
| `jobs.py` | Chụp nguồn, kiểm tra trước khi chạy, tuần tự, hủy, kết quả và tên an toàn |
| `converters/markitdown_adapter.py` | API MarkItDown local và cảnh báo giới hạn |
| `converters/markdown_to_docx.py` | Token Markdown → paragraph/run/table/image/numbering |
| `converters/word_to_pdf.py` | LibreOffice riêng biệt, timeout/hủy, đọc PDF kết quả |
| `styles.py` | Font, glyph, A4/lề và cấu hình style duy nhất |
| `i18n.py` | Bảng khóa thông báo Việt/Anh |

Tham khảo kỹ thuật: [Tkinter và luồng](https://docs.python.org/3/library/tkinter.html),
[token Markdown](https://markdown-it-py.readthedocs.io/en/latest/using.html),
[định dạng python-docx](https://python-docx.readthedocs.io/en/latest/user/text.html),
[tham số PDF LibreOffice](https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html).

## English quick start

Double-click `run.cmd`, select the source file/folder, output folder and mode,
then click Convert. Switch to English in the top-right box. Existing output files
are never overwritten. Processing stays local. LibreOffice Writer is required for
both PDF export modes; those modes are disabled while it is missing. Actual PDF
export and visual layout remain unverified on this machine. See the limitations
above before relying on the output.
