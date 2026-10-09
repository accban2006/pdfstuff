# Hướng dẫn chạy dự án chuyển đổi tài liệu trên Windows

Hướng dẫn dành cho người sử dụng và người cần cài môi trường chạy từ mã nguồn.
Thư mục dự án trên máy hiện tại là `D:\appdata\claude\claudedata\pdftomd`.
Nếu đặt dự án ở nơi khác, thay đường dẫn này trong các lệnh bằng đường dẫn thực tế.

Ứng dụng có giao diện cửa sổ, mặc định tiếng Việt, có thể đổi sang English.
Tài liệu được xử lý cục bộ. Không cần tài khoản, không gửi nội dung tài liệu lên
dịch vụ ngoài. Việc cài thư viện ban đầu có thể cần Internet.
Hiện chưa có bản EXE độc lập; `run.cmd` khởi chạy mã Python đã cài trong `.venv`.

## 1. Chọn cách bắt đầu

| Tình huống | Thực hiện |
| --- | --- |
| Chạy trên máy hiện tại, `.venv` còn hoạt động | Làm theo mục 2 |
| Máy mới hoặc chưa có `.venv` | Cài theo mục 3, rồi chạy theo mục 2 |
| Cần Markdown → PDF hoặc Word → PDF | Thêm LibreOffice theo mục 4 |
| Cửa sổ không mở hoặc chuyển đổi báo lỗi | Tra mục 8 |
| Cần kiểm tra môi trường phát triển | Xem mục 9 |

Kiểm tra trực tiếp ngày **09/10/2026**: môi trường hiện tại có Python **3.12.14**,
Tk **8.6**, MarkItDown **0.1.8** và đủ bốn tệp font Arial mà ứng dụng yêu cầu.
Máy hiện tại đã cài LibreOffice Writer; hai chế độ xuất PDF đã được kiểm thử
với fixture Anh/Việt. Trên máy khác, nếu lựa chọn PDF bị tắt, xem mục 4.
Môi trường này có `uv` nhưng Python trong `.venv` **chưa có pip**; điều này không
cản trở việc mở ứng dụng. Nếu cần cài lại thư viện trên máy này, dùng nhánh `uv`
ở mục 3.4 hoặc bổ sung pip theo mục 8.

## 2. Chạy ngay trên máy hiện tại

### Cách A — Nhấp đúp trong File Explorer

1. Mở File Explorer bằng **Windows + E**.
2. Dán `D:\appdata\claude\claudedata\pdftomd` vào thanh địa chỉ, nhấn Enter.
3. Nhấp đúp **run.cmd**.
4. Chờ cửa sổ **Chuyển đổi tài liệu** xuất hiện.

`run.cmd` tự chuyển về thư mục dự án và dùng `.venv\Scripts\pythonw.exe`.
Nếu hiện thông báo yêu cầu tạo môi trường Python, thực hiện mục 3.
Nếu nhấp đúp mà không thấy cửa sổ, dùng cách B để xem lỗi trong terminal.

### Cách B — Chạy bằng PowerShell

Mở PowerShell, chạy lần lượt:

```powershell
Set-Location 'D:\appdata\claude\claudedata\pdftomd'
.\.venv\Scripts\python.exe -m pdftomd
```

Giữ cửa sổ PowerShell mở trong khi sử dụng. Đóng ứng dụng bằng nút **X** khi xong.
Không cần chạy `Activate.ps1`. Các lệnh trong hướng dẫn gọi đúng Python của dự án
trực tiếp, nên không cần thay đổi Execution Policy của PowerShell.

## 3. Cài lần đầu hoặc cài trên máy khác

### 3.1. Chuẩn bị

- Windows và Python **3.12**, có Tkinter. Dự án khai báo `>=3.12,<3.13`;
  không dùng Python 3.11 hoặc 3.13 cho môi trường này.
- Mã nguồn dự án, gồm `pyproject.toml`, `requirements-lock.txt`, `src` và `run.cmd`.
- Mã nguồn MarkItDown local đã kiểm thử. Trên máy hiện tại, đường dẫn là
  `D:\appdata\markit\packages\markitdown`.
- Font Arial thường, đậm, nghiêng và đậm nghiêng cho các chế độ bắt đầu từ Markdown.
- LibreOffice Writer nếu cần xuất PDF; có thể bổ sung sau.

Không sao chép `.venv` sang máy khác: môi trường có thể tham chiếu Python ở máy cũ.
Để chạy từ mã nguồn trên máy mới, cần tạo `.venv` mới và có bản MarkItDown phù hợp.
Kho MarkItDown local được ghi nhận trong dự án có phiên bản **0.1.8**, commit
tham chiếu `4cc9fa17653d695d64fb9eee5b33d4de55ff84e8`.
Không mặc định bản PyPI cùng số phiên bản có hành vi giống bản local.

### 3.2. Kiểm tra Python và Tkinter

```powershell
py -3.12 --version
py -3.12 -m tkinter
```

Lệnh thứ hai phải mở cửa sổ thử Tkinter. Đóng cửa sổ đó sau khi kiểm tra.
Nếu không nhận diện được `py` hoặc không có Python 3.12, cài Python 3.12 có
thành phần Tcl/Tk rồi mở lại PowerShell. Nếu dùng Python ở đường dẫn riêng,
thay `py -3.12` bằng `& 'C:\duong-dan-thuc-te\python.exe'`.

### 3.3. Tạo một môi trường cho dự án

Chỉ thực hiện khi chưa có `.venv` hoạt động:

```powershell
Set-Location 'D:\appdata\claude\claudedata\pdftomd'
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe --version
```

Kết quả phải là Python 3.12.x. Nếu đang thay môi trường lỗi, đóng ứng dụng và
đổi tên `.venv` cũ để giữ bản dự phòng trước khi tạo lại. Không xóa tài liệu nguồn
hoặc thư mục kết quả khi sửa môi trường.

### 3.4. Cài thư viện

Chọn **một** trong hai cách dưới đây. Chạy từ thư mục gốc dự án.
`requirements-lock.txt` là tệp ràng buộc phiên bản dùng với `-c`; lệnh vẫn cần
chỉ định gói dự án và nguồn MarkItDown.

**Dùng pip trong môi trường vừa tạo:**

```powershell
.\.venv\Scripts\python.exe -m pip install -c requirements-lock.txt -e ".[dev]" -e "D:\appdata\markit\packages\markitdown[pdf,docx]"
```

**Dùng uv nếu đã có uv, phù hợp với máy hiện tại:**

```powershell
uv pip install --python .venv\Scripts\python.exe -c requirements-lock.txt -e ".[dev]" -e "D:\appdata\markit\packages\markitdown[pdf,docx]"
```

Nếu kho MarkItDown ở nơi khác, thay phần đường dẫn trong đối số cuối.
Phải giữ extras `[pdf,docx]`, không dùng `[all]`.
`.[dev]` cài thêm pytest và Ruff để chạy các kiểm tra của dự án; nếu chỉ sử dụng
ứng dụng, có thể thay `".[dev]"` bằng `"."`.
Editable (`-e`) khiến môi trường dùng mã nguồn ở đường dẫn đã cài; vì vậy không
di chuyển hoặc xóa các thư mục mã nguồn đó sau khi cài.

### 3.5. Kiểm tra và khởi chạy

```powershell
.\.venv\Scripts\python.exe -c "import tkinter, markitdown, markdown_it, docx, fontTools, PIL; print('Import OK')"
.\.venv\Scripts\python.exe -m pdftomd
```

`Import OK` chỉ xác nhận các thư viện import được; cần thử chuyển đổi ở mục 6
để kiểm tra một luồng sử dụng. Khi cửa sổ đã mở được, các lần sau có thể dùng
`run.cmd`.

## 4. Bật hai chế độ xuất PDF

Markdown → PDF và Word → PDF cần **LibreOffice Writer**. Ứng dụng không tự tải
hoặc cài LibreOffice. Tải từ [trang chính thức](https://www.libreoffice.org/download/).
Sau khi cài Writer, bấm **Kiểm tra lại** ngay trong cửa sổ để bật chế độ PDF.
Nếu cài ở vị trí khác, bấm **Chọn LibreOffice** và chọn `program\soffice.exe`
hoặc `soffice.com`. Ứng dụng lưu đường dẫn cho lần mở sau tại
`%LOCALAPPDATA%\pdftomd\libreoffice.txt`; không cần thiết lập biến môi trường.

Ứng dụng tìm `soffice` qua biến `PDFTOMD_LIBREOFFICE`, PATH và các vị trí cài
LibreOffice thông thường. Nếu không tìm thấy tự động, chỉ định tệp thực thi:

```powershell
Set-Location 'D:\appdata\claude\claudedata\pdftomd'
Test-Path 'C:\Program Files\LibreOffice\program\soffice.exe'
$env:PDFTOMD_LIBREOFFICE = 'C:\Program Files\LibreOffice\program\soffice.exe'
.\.venv\Scripts\python.exe -m pdftomd
```

`Test-Path` phải trả về `True`; nếu là `False`, tìm vị trí cài thực tế rồi thay
đường dẫn. Biến `$env:...` trên chỉ áp dụng cho phiên PowerShell đó và ứng dụng
được mở từ phiên đó, không tự lưu cho những lần nhấp đúp `run.cmd` về sau.
Nếu cần lưu lâu dài, thêm biến người dùng `PDFTOMD_LIBREOFFICE` trong phần
Environment Variables của Windows, rồi mở lại PowerShell/File Explorer trước
khi khởi chạy. Không thêm dấu ngoặc kép vào giá trị biến qua hộp thoại.

Có thể kiểm tra cách ứng dụng tìm LibreOffice bằng:

```powershell
.\.venv\Scripts\python.exe -c "from pdftomd.converters.word_to_pdf import find_libreoffice; print(find_libreoffice())"
```

Kết quả `None` nghĩa là chưa tìm thấy. Một đường dẫn nghĩa là tìm được tệp thực
thi, chưa xác nhận chuyển đổi PDF thành công. Mỗi tệp có timeout **120 giây**.
LibreOffice chạy nền với profile tạm riêng.

Hai chế độ PDF đã được xuất/render thực tế trên fixture theo
[VALIDATION.md](VALIDATION.md). Với tài liệu của bạn, cần thử
và đối chiếu PDF với nguồn trước khi sử dụng chính thức. Markdown → PDF dùng
DOCX trung gian với cùng định dạng của Markdown → Word; Word → PDF xuất trực
tiếp từ bản sao DOCX và không áp quy tắc font Markdown lên Word nguồn.

## 5. Thao tác trong giao diện

1. Chọn ngôn ngữ ở góc trên nếu muốn dùng **English**. Đổi ngôn ngữ giao diện
   không dịch nội dung tài liệu.
2. Chọn **Chế độ chuyển đổi**. Với file `.md`, có thể dùng bộ lọc
   **Markdown (.md)** trong hộp chọn tệp; ứng dụng tự chọn **Markdown → Word**
   nếu đang ở chế độ dành cho PDF/Word. Nếu đã chọn **Markdown → PDF**, lựa
   chọn đó được giữ. Đường dẫn dán trực tiếp và thư mục cần chọn chế độ thủ công.
3. Ở **Tệp hoặc thư mục nguồn**, bấm **Chọn tệp** hoặc **Chọn thư mục**.
   Có thể dán đường dẫn trực tiếp; đây là đường dẫn trên máy, không phải URL.
4. Ở **Thư mục lưu kết quả**, chọn hoặc nhập một thư mục có quyền ghi.
   Nếu thư mục chưa có, ứng dụng tạo và thông báo đường dẫn.
5. Bấm **Chuyển đổi**. Trạng thái cho biết tên tệp và số thứ tự đang xử lý.
6. Sau khi hoàn tất, xem số **Thành công / Cảnh báo / Lỗi / Hủy**.
7. Bấm **Xem chi tiết** để đọc lý do và đường dẫn kết quả từng tệp;
   bấm **Mở thư mục kết quả** để xem trong Explorer.

| Lựa chọn | Đầu vào | Đầu ra | Phụ thuộc bổ sung cần có |
| --- | --- | --- | --- |
| PDF → Markdown | `.pdf` có văn bản trích xuất được | `.md` | MarkItDown extras PDF |
| Word → Markdown | `.docx` | `.md` | MarkItDown extras DOCX |
| Markdown → Word | `.md` UTF-8 hoặc UTF-8 BOM | `.docx` | Đủ bộ Arial |
| Markdown → PDF | `.md` UTF-8 hoặc UTF-8 BOM | `.pdf` | Đủ bộ Arial, LibreOffice Writer |
| Word → PDF | `.docx` | `.pdf` | LibreOffice Writer |

Một lượt chỉ chọn một chế độ. Với thư mục có nhiều loại tài liệu, chạy riêng
từng chế độ. Không hỗ trợ `.doc`; phải lưu thành DOCX bằng phần mềm soạn thảo,
không chỉ đổi đuôi tên tệp.

**Xử lý thư mục:** chỉ lấy tệp đúng phần mở rộng ở cấp thư mục đã chọn, không
duyệt thư mục con. Bỏ qua tệp có tên bắt đầu bằng `~$`, `~` hoặc `.`.
Danh sách được chụp trước khi chạy, không lấy thêm tệp vừa xuất vào cùng thư mục.
Một tệp lỗi không làm dừng cả lô.

**Tên kết quả:** giữ tên gốc và thay đuôi. Nếu tên đã tồn tại, dùng `ten (1).md`,
`ten (2).md`… hoặc đuôi tương ứng; không ghi đè và có xét chữ hoa/thường.
Nguồn không bị sửa. Chỉ công bố kết quả sau khi hoàn tất; tệp tạm được dọn khi
lỗi/hủy. Bạn có thể chọn cùng thư mục nguồn, nhưng thư mục kết quả riêng sẽ
dễ đối chiếu hơn.

**Bàn phím:** Tab chuyển tiêu điểm. Enter kích hoạt nút đang có tiêu điểm;
khi ở ô nhập đường dẫn và ứng dụng đang rảnh, Enter bắt đầu chuyển đổi.

**Hủy:** bấm **Hủy** để dừng hàng đợi. Với PDF/Word → Markdown, backend cần
xử lý xong tệp đang chạy nên hiện “Đang hủy sau tệp hiện tại…”. Kết quả tệp
đang bị hủy không được công bố; kết quả đã hoàn tất trước đó vẫn giữ lại.
Đóng cửa sổ giữa tác vụ cũng yêu cầu hủy và chờ backend dừng. Khi rảnh, nút Hủy
bị vô hiệu hóa.

## 6. Ví dụ chạy thử bằng tài liệu có sẵn

Không cần đưa tài liệu cá nhân vào lần thử đầu. Dự án có fixture tổng hợp Anh/Việt.
Các đường dẫn dưới đây nhập vào giao diện, không phải lệnh chuyển đổi terminal.

### Ví dụ A — Markdown → Word

- Chế độ: **Markdown → Word**.
- Nguồn: `D:\appdata\claude\claudedata\pdftomd\tests\fixtures\sample.md`.
- Đích: `D:\appdata\claude\claudedata\pdftomd\ket-qua-thu`.
- Bấm **Chuyển đổi**, rồi **Mở thư mục kết quả**.

Kết quả dự kiến là `sample.docx` hoặc `sample (1).docx` nếu tên đã tồn tại.
Giữ `local.png` cạnh `sample.md` vì mẫu dùng ảnh tương đối. Mở DOCX trong
Word/Writer để kiểm tra dấu Việt, bảng, ảnh, danh sách, liên kết và chữ đậm.
H1–H6 và chữ đậm phải Arial **15 pt, đậm, đen**; chữ thường Arial **11 pt, đen**.
Trang A4, lề 2 cm. Ứng dụng không tự chèn bìa, ngày hoặc số trang.

### Ví dụ B — Word → Markdown theo lô

- Chế độ: **Word → Markdown**.
- Nguồn: `D:\appdata\claude\claudedata\pdftomd\tests\fixtures`.
- Đích: `D:\appdata\claude\claudedata\pdftomd\ket-qua-thu\word-md`.

Ứng dụng lấy các DOCX trong thư mục này như `en.docx`, `vi.docx`,
`word-layout.docx`, bỏ qua PDF/MD/PNG. Đọc **Xem chi tiết**, nhất là cảnh báo
header/footer hoặc ảnh. Mở MD bằng trình soạn thảo hỗ trợ UTF-8 để đối chiếu.

### Ví dụ C — PDF văn bản và PDF scan

Chọn **PDF → Markdown**, thử lần lượt `tests\fixtures\vi.pdf` và
`tests\fixtures\scan.pdf` với thư mục kết quả bạn chọn. Đường dẫn tương đối
này nằm bên dưới gốc dự án.
`vi.pdf` dùng để kiểm tra nội dung tiếng Việt; PDF → MD có cảnh báo giới hạn
cấu trúc. `scan.pdf` dùng để kiểm tra thông báo không trích xuất được văn bản,
không phải trường hợp chuyển đổi thành công. Dự án chưa có OCR.

Sau khi có LibreOffice, có thể thử **Markdown → PDF** với `sample.md` và
**Word → PDF** với `word-layout.docx`. Kiểm tra PDF trực quan: dấu Việt, font,
bảng, ảnh, header/footer và ngắt trang; không chỉ kiểm tra tệp có tồn tại.

## 7. Hiểu kết quả và giới hạn

| Trạng thái | Ý nghĩa và việc cần làm |
| --- | --- |
| Thành công | Hoàn tất theo các kiểm tra của backend; vẫn nên đối chiếu tài liệu quan trọng |
| Cảnh báo | Có kết quả nhưng có giới hạn cần xem; đọc chi tiết và so với nguồn |
| Lỗi | Tệp không tạo được kết quả hoàn chỉnh; sửa nguyên nhân rồi chạy lại |
| Hủy | Tệp chưa được công bố do hủy; các kết quả hoàn tất trước đó còn nguyên |

PDF → MD không giữ font/bố cục từng trang và có thể mất cấu trúc phức tạp.
Word → MD có thể mất ảnh, header/footer, text box hoặc tracked changes.
Không cam kết giữ hình thức trang khi chuyển sang Markdown.

Markdown đầu vào phải là UTF-8 hoặc UTF-8 BOM. Ảnh phải là tài nguyên local;
ảnh tương đối được tìm theo thư mục chứa MD. Ảnh thiếu, hỏng hoặc URL từ xa
gây lỗi thay vì bị bỏ qua âm thầm. Không tự tải ảnh Internet.
HTML được giữ như chữ và có cảnh báo; không thực thi HTML hoặc code.
Footnote, toán và các cú pháp mở rộng chưa được hỗ trợ đầy đủ; một số cấu trúc
bị từ chối để tránh mất nội dung. Arial thiếu glyph sẽ báo mã Unicode,
không tự thay bằng font khác.

Xem đầy đủ các giới hạn tại [README.md](README.md) và các kiểm tra đã thực sự
chạy tại [VALIDATION.md](VALIDATION.md). Việc viết hướng dẫn này không bổ sung
nghiệm thu PDF thực tế hoặc nghiệm thu thủ công giao diện.

## 8. Khắc phục lỗi thường gặp

| Hiện tượng | Cách xử lý |
| --- | --- |
| Nhấp đúp `run.cmd` không mở cửa sổ | Chạy bằng PowerShell ở mục 2 để thấy lỗi; kiểm tra `.venv\Scripts\python.exe` tồn tại |
| `No module named pdftomd` | Vào đúng gốc dự án, dùng Python của `.venv`, cài lại gói theo mục 3.4 |
| Thiếu `markitdown`, `mammoth`, `pdfminer` hoặc thư viện khác | Chạy lại đúng lệnh cài với nguồn MarkItDown local và extras `[pdf,docx]` |
| `No module named pip` | Dùng lệnh `uv pip install` ở mục 3.4; hoặc thử `python.exe -m ensurepip --upgrade` như bên dưới |
| Không tìm thấy đường dẫn MarkItDown khi cài | Kiểm tra vị trí kho local và sửa đối số `-e`; không chỉ thay bằng bản PyPI chưa kiểm thử |
| Hai chế độ PDF bị mờ | Cài Writer rồi bấm **Kiểm tra lại**; nếu đã cài nơi khác, dùng **Chọn LibreOffice** |
| Markdown → Word/PDF bị mờ, có thông báo thiếu Arial | Bổ sung đủ Arial thường/đậm/nghiêng/đậm nghiêng, rồi mở lại |
| Báo nguồn thiếu hoặc sai đuôi | Kiểm tra đường dẫn và chế độ; `.doc` phải được lưu thành `.docx` thực sự |
| Thư mục không có tệp phù hợp | Chọn đúng thư mục chứa tệp, đúng chế độ; không quét thư mục con |
| Không truy cập được đích | Nhập đường dẫn thư mục, không phải tên tệp; chọn nơi có quyền ghi và đủ dung lượng |
| PDF không trích xuất được văn bản | Có thể là PDF scan; cần một quy trình OCR riêng, hiện ứng dụng chưa cung cấp |
| Markdown không phải UTF-8 | Mở bằng trình soạn thảo và lưu bản sao UTF-8; không bỏ qua ký tự lỗi |
| Không tìm thấy ảnh | Giữ ảnh đúng vị trí tương đối với MD, kiểm tra tên/đuôi; với URL ảnh cần chuẩn bị bản local |
| Arial thiếu ký tự `U+...` | Đối chiếu ký tự được báo; hiện chưa thể xuất đúng ký tự đó bằng bộ Arial đang có |
| LibreOffice vượt 120 giây hoặc không có PDF đọc được | Thử một DOCX nhỏ, mở bản sao nguồn trong Writer để kiểm tra; xem mã lỗi trong chi tiết |
| Word có tài nguyên liên kết ngoài | Nhúng ảnh/tài nguyên vào DOCX trước khi xuất; hyperlink thông thường được cho phép |
| Chạy lại thấy tên có `(1)`, `(2)` | Đây là cơ chế tránh ghi đè; mở đúng đường dẫn kết quả trong chi tiết |

Nếu cần bổ sung pip vào `.venv` và bản Python có `ensurepip`:

```powershell
.\.venv\Scripts\python.exe -m ensurepip --upgrade
.\.venv\Scripts\python.exe -m pip --version
```

Nếu `ensurepip` không có, dùng `uv` đã cài hoặc tạo môi trường bằng bản Python
3.12 đầy đủ. Không cần sửa chính sách PowerShell cho các lệnh này.
Ứng dụng chưa cấu hình một tệp log cố định; khi chẩn đoán, dùng thông báo
**Xem chi tiết** và đầu ra PowerShell. Không cần chia sẻ toàn bộ tài liệu để
báo lỗi môi trường.

## 9. Kiểm tra cho người phát triển

Các lệnh sau cần phụ thuộc `.[dev]`, chạy tại gốc dự án:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.cache\pytest-current
.\.venv\Scripts\ruff.exe check src tests tools
.\.venv\Scripts\ruff.exe format --check src tests tools
```

Kiểm tra tính nhất quán phụ thuộc bằng một trong hai lệnh, tùy công cụ đã có:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

```powershell
uv pip check --python .venv\Scripts\python.exe
```

Các test LibreOffice thực tế có thể bị skip khi không tìm được LibreOffice.
Skip không có nghĩa đã kiểm chứng xuất PDF. Kết quả lịch sử **36 passed,
2 skipped** thuộc báo cáo ngày 08/10/2026 trong `VALIDATION.md`, không phải
kết quả chạy lại khi soạn hướng dẫn này. Các kiểm tra tự động cũng không thay
việc render và đối chiếu trực quan tài liệu xuất.

Không cần chạy `tools/generate_fixtures.py` để dùng ứng dụng hoặc thử fixture
có sẵn; công cụ tạo fixture cần ReportLab riêng trong môi trường phát triển.
Không cần cài skill, plugin hoặc PyInstaller để khởi chạy từ mã nguồn.
