# Quy tắc dự án chuyển đổi tài liệu trên máy tính

## Mục tiêu và phạm vi

Xây dựng ứng dụng desktop chạy trên Windows, xử lý tài liệu cục bộ, giao diện đơn giản cho người mới. Hỗ trợ nội dung và giao diện tiếng Việt/tiếng Anh. File này là quy tắc phát triển; chỉ triển khai tính năng khi người dùng yêu cầu.

Các chế độ chuyển đổi bắt buộc:

| Chế độ | Đầu vào | Đầu ra |
| --- | --- | --- |
| PDF → Markdown | `.pdf` | `.md` |
| Word → Markdown | `.docx` | `.md` |
| Markdown → PDF | `.md` | `.pdf` |
| Word → PDF | `.docx` | `.pdf` |
| Markdown → Word | `.md` | `.docx` |

Markdown → Word được đưa vào vì có trong ảnh mẫu `Untitled.png` và quy ước định dạng của người dùng. Word mặc định là DOCX; không coi `.doc` là DOCX. Nếu gặp `.doc`, thông báo chưa hỗ trợ; chỉ bổ sung chuyển đổi định dạng cũ khi có yêu cầu riêng.

## Công nghệ và lý do chọn

| Công nghệ | Vai trò | Quy tắc |
| --- | --- | --- |
| Python 3.12 | Ngôn ngữ chính | Một môi trường `.venv`; khai báo phụ thuộc trong `pyproject.toml`. |
| Tkinter + ttk | GUI desktop | Dùng thư viện GUI đi kèm Python; widget chuẩn, bố cục gọn. |
| MarkItDown với extras `pdf,docx` | PDF/Word → MD | Dùng bản tại `D:\appdata\markit`, không viết lại bộ chuyển đổi. |
| markdown-it-py | Phân tích Markdown | Đọc token/cây cú pháp; không dùng regex để phân tích toàn bộ tài liệu. Bật bảng theo cấu hình đã kiểm thử. |
| python-docx | Markdown → DOCX | Ánh xạ cấu trúc và định dạng vào paragraph, run, style, table. |
| LibreOffice Writer, chế độ headless | DOCX → PDF | Dùng chung cho Word → PDF và DOCX trung gian của Markdown → PDF. Là phụ thuộc ngoài, không tự tải hoặc cài ngầm. |
| pathlib, tempfile, subprocess, queue, threading | Đường dẫn, tệp tạm, tiến trình, tác vụ nền | Ưu tiên thư viện chuẩn. |
| pytest + Ruff | Kiểm thử và kiểm tra mã | Chỉ dùng trong môi trường phát triển. |
| PyInstaller | Đóng gói Windows | Chỉ thêm ở bước phát hành; ưu tiên bản thư mục `onedir`, không đóng gói cả kho MarkItDown hoặc skill. |

Chỉ cài extras MarkItDown cần dùng, không cài `[all]`. Khi phát triển, có thể cài editable từ `D:\appdata\markit\packages\markitdown[pdf,docx]`. Khi phát hành, đóng gói đúng bản đã kiểm thử và ghi phiên bản/commit tham chiếu; ứng dụng trên máy khác không được phụ thuộc đường dẫn `D:\appdata\markit`.

Không thêm web server, Electron, cơ sở dữ liệu, tài khoản, cloud hoặc framework GUI thứ hai vào phạm vi hiện tại. LibreOffice phải được tìm qua cấu hình/PATH/vị trí cài đặt thông thường. Khi thiếu, chỉ các chế độ cần xuất PDF bị vô hiệu hóa và hiển thị hướng dẫn ngắn.

## Tham chiếu MarkItDown

Trước khi triển khai hoặc sửa PDF/Word → MD, đọc đúng nguồn tại:

- `D:\appdata\markit\README.md`.
- `D:\appdata\markit\packages\markitdown\pyproject.toml`.
- `D:\appdata\markit\packages\markitdown\src\markitdown\converters\_pdf_converter.py`.
- `D:\appdata\markit\packages\markitdown\src\markitdown\converters\_docx_converter.py`.
- Các test PDF/DOCX tương ứng trong `D:\appdata\markit\packages\markitdown\tests`.

Bản local đã tham khảo dùng Mammoth và bộ chuyển HTML cho DOCX, pdfminer.six và pdfplumber cho PDF. Đây là thông tin của bản local, không giả định mọi bản phát hành có cùng hành vi.

Gọi API chuyển đổi cục bộ của MarkItDown, lấy nội dung Markdown từ kết quả. Tách tích hợp vào một adapter nhỏ. Với cùng đầu vào và cấu hình, phần nội dung MD phải tương đương kết quả MarkItDown local; chỉ chuẩn hóa UTF-8 và xuống dòng khi ghi tệp. Không tự thêm bước sửa văn bản, làm sạch, đoán tiêu đề hoặc dịch nội dung.

Không sửa kho `D:\appdata\markit` để phục vụ ứng dụng nếu chưa được yêu cầu. Không bật plugin OCR, LLM hoặc dịch vụ Azure mặc định. PDF scan không có lớp văn bản phải thông báo không trích xuất được thay vì báo thành công với tệp rỗng. OCR Anh/Việt là phần mở rộng riêng nếu được yêu cầu.

## Giao diện theo ảnh mẫu

Lấy `Untitled.png` ở gốc dự án làm tham chiếu bố cục. Dùng một cửa sổ chính, nền sáng, chữ dễ đọc, khoảng cách đều; không có dashboard, sidebar hoặc nhiều màn hình cấu hình.

1. Hàng đầu: nhãn “Tệp hoặc thư mục nguồn”, ô đường dẫn rộng; nút nhỏ “Chọn tệp” và “Chọn thư mục”. Cho phép dán đường dẫn trực tiếp.
2. Hàng thứ hai: nhãn “Thư mục lưu kết quả”, ô đường dẫn và nút “Chọn thư mục”. Đây là đường dẫn máy tính, không phải URL Internet.
3. Bên phải: nút chính “Chuyển đổi” tương ứng “chấp nhận” trong ảnh, phía dưới là “Hủy”.
4. Phía dưới: một nhóm radio button, chỉ chọn một chế độ; PDF → MD, Word → MD, MD → PDF, MD → Word và Word → PDF. Sắp thành hai cột như ảnh; mục thứ năm ở hàng cuối.
5. Góc trên: lựa chọn ngôn ngữ “Tiếng Việt / English”, mặc định tiếng Việt.
6. Cuối cửa sổ: trạng thái ngắn và tiến độ khi đang xử lý. Sau khi xong, hiển thị số thành công/thất bại và nút “Mở thư mục kết quả”. Chi tiết lỗi chỉ mở khi cần.

Dùng Arial cho GUI. Chữ có độ tương phản rõ, nút có nhãn bằng chữ; hỗ trợ Tab/Enter, màn hình DPI cao và thay đổi kích thước cửa sổ mà không cắt nhãn. Không sao chép viền đen dày của bản phác thảo thành phong cách trang trí.

“Hủy” dừng hàng đợi và tác vụ đang chạy khi backend cho phép. Nếu MarkItDown không hỗ trợ ngắt giữa tệp, hiển thị “Đang hủy sau tệp hiện tại”, không báo đã hủy ngay. Khi chưa có tác vụ, nút Hủy bị vô hiệu hóa. Không xóa kết quả đã hoàn thành khi hủy.

## Quy tắc nội dung và định dạng

### Nội dung chung

- Giữ nguyên từ ngữ, thứ tự, con số, dấu câu, dấu tiếng Việt và các ký tự đặc biệt mà backend đọc được. Không tóm tắt, diễn giải, sửa chính tả, dịch hoặc tự thêm/bớt nội dung.
- Chỉ thêm cú pháp/định dạng cần thiết cho định dạng đích. Thông báo lỗi, cảnh báo và thông tin ứng dụng nằm trong GUI hoặc log, không chèn vào tài liệu xuất.
- Đọc MD UTF-8, chấp nhận UTF-8 BOM; ghi MD UTF-8. Khi không giải mã được, báo lỗi rõ, không dùng `errors='ignore'` hoặc thay ký tự âm thầm.
- Giữ heading, paragraph, danh sách, bảng, liên kết, nhấn mạnh và ảnh theo khả năng của từng backend. Cấu trúc không hỗ trợ phải có cảnh báo cụ thể, không âm thầm làm phẳng hoặc mất dữ liệu.
- Markdown không lưu font, cỡ chữ hoặc bố cục trang như Word/PDF. PDF/Word → MD giữ nội dung và cấu trúc theo MarkItDown, không hứa giữ nguyên hình thức từng trang. Với cấu trúc phức tạp, chỉ công bố mức hỗ trợ đã kiểm thử.

### Markdown → Word/PDF

- Mọi heading H1–H6: **Arial, 15 pt, đậm, màu đen `#000000`**. Giữ cấp heading trong DOCX dù cùng cỡ chữ.
- Mọi đoạn nhấn mạnh đậm `**...**` hoặc `__...__`: **Arial, 15 pt, đậm, màu đen `#000000`**, kể cả trong bảng hoặc danh sách. Quy ước này áp dụng cho cả heading và chữ đậm; không tự tăng heading lên cỡ 18–24 pt.
- Phần chữ thường mặc định Arial 11 pt, màu đen; đây là giá trị thiết kế mặc định cho phần chưa được người dùng quy định. Chữ nghiêng giữ nghiêng; liên kết giữ đích liên kết và màu đen.
- Code giữ nguyên ký tự, xuống dòng và khoảng trắng có ý nghĩa; dùng Arial theo quy ước font của dự án. Không thực thi code hoặc nội dung HTML trong MD.
- Dùng một cấu hình style chung để xuất MD → DOCX; MD → PDF phải đi qua chính DOCX đó rồi xuất bằng LibreOffice. Không duy trì hai bộ quy tắc font độc lập.
- Trang mặc định A4, lề 2 cm, cho bảng/ảnh vừa vùng nội dung và ngắt trang hợp lý. Không tự chèn tiêu đề, trang bìa, ngày xuất hoặc số trang.
- Xử lý ảnh local tương đối theo thư mục của file MD; giữ tỷ lệ, không bỏ ảnh âm thầm. Không tự tải ảnh từ Internet; tài nguyên thiếu hoặc từ xa phải báo rõ trước khi coi kết quả là hoàn chỉnh.
- Kiểm tra Arial có sẵn và PDF xuất đúng font; nếu thiếu, yêu cầu cài Arial, không tự thay bằng font khác. Kiểm tra dấu Việt và glyph ký tự đặc biệt trước khi xác nhận hỗ trợ chúng.

### Word → PDF

Xuất trực tiếp từ Word bằng LibreOffice để giữ định dạng gốc. Không chuyển Word qua MD và không áp quy ước Arial 15 pt vào Word nguồn. Giữ font, cỡ chữ, bảng, ảnh, header/footer và bố cục trong phạm vi backend hỗ trợ. Kiểm thử bằng tài liệu thực vì LibreOffice có thể dàn trang khác Microsoft Word; không tuyên bố giữ nguyên tuyệt đối khi chưa có bằng chứng.

## Xử lý tệp và tác vụ

- Nguồn có thể là một tệp hoặc một thư mục. Với thư mục, xử lý tất cả tệp đúng phần mở rộng của chế độ trong thư mục đó; mặc định không duyệt thư mục con. Bỏ qua tệp khóa Word `~$...` và tệp tạm.
- Chụp danh sách nguồn trước khi chạy, sắp xếp ổn định; không quét lại để lấy cả kết quả vừa tạo. Không sửa, đổi tên hoặc xóa tệp nguồn.
- Giữ tên gốc, chỉ thay phần mở rộng. Khi trùng kết quả, tạo tên tiếp theo như `ten (1).md`; không ghi đè tệp có sẵn, kể cả trùng tên do chữ hoa/thường trên Windows.
- Kiểm tra đầu vào, chế độ, quyền đọc/ghi và phụ thuộc trước khi chạy. Nếu tạo thư mục đích mới, thông báo rõ nơi lưu. Khi thư mục không có tệp phù hợp, hiển thị lý do thay vì chạy tác vụ rỗng.
- Xử lý tuần tự trong worker nền, cập nhật GUI qua queue và `after()` ở luồng chính. Không gọi widget từ worker; cửa sổ phải phản hồi được trong suốt quá trình.
- Một tệp lỗi không dừng cả lô. Kết quả mỗi tệp có trạng thái thành công, lỗi, hủy hoặc cảnh báo; bản có mất thành phần đã biết không được gắn nhãn thành công đầy đủ.
- Ghi ra thư mục tạm riêng cho tác vụ; chỉ chuyển kết quả hoàn chỉnh đến đích. Dọn tệp tạm khi lỗi/hủy; không để lại file cuối bị ghi dở. Với nhiều tài nguyên kèm theo, chỉ xác nhận hoàn tất sau khi chúng đều được lưu.
- Gọi LibreOffice bằng danh sách đối số, `shell=False`, timeout và profile tạm riêng để tránh ảnh hưởng phiên LibreOffice của người dùng. Chạy nền với cửa sổ ẩn trên Windows; kiểm tra mã thoát, sự tồn tại và khả năng đọc file PDF, không chỉ dựa vào việc tiến trình kết thúc.
- Chỉ xử lý dữ liệu trên máy, không gửi nội dung lên dịch vụ ngoài. Ghi log phục vụ chẩn đoán nhưng không ghi toàn bộ nội dung tài liệu.

## Clean code và giới hạn quy mô

Cấu trúc dự kiến khi triển khai:

```text
src/pdftomd/
  __main__.py
  gui.py
  jobs.py
  converters/
    markitdown_adapter.py
    markdown_to_docx.py
    word_to_pdf.py
  styles.py
  i18n.py
tests/
  fixtures/
pyproject.toml
AGENTS.md
Untitled.png
```

GUI chỉ thu thập lựa chọn và hiển thị trạng thái. `jobs.py` điều phối hàng đợi, hủy và kết quả; converter xử lý tài liệu; `styles.py` là nguồn duy nhất của định dạng xuất. MD → PDF được điều phối từ converter hiện có, không sao chép logic MD → DOCX.

Dùng tên hàm rõ nghĩa, type hint, hàm có trách nhiệm cụ thể và lỗi có ngữ cảnh. Chỉ tách module khi có trách nhiệm độc lập; không dựng plugin framework, lớp trừu tượng hoặc cấu hình hàng chục lựa chọn khi chưa cần. Giao diện Anh/Việt dùng một bảng khóa dịch nhỏ; đổi ngôn ngữ giao diện không đổi nội dung tài liệu.

Không đưa `.venv`, tệp build, tài liệu người dùng, cache, thư mục `.agents/skills` hoặc toàn bộ kho MarkItDown vào gói ứng dụng. Skill phục vụ phát triển, không phải phụ thuộc chạy ứng dụng. Mọi phụ thuộc mới phải có chức năng cần thiết, được khai báo và khóa phiên bản đã kiểm thử.

## Tiêu chí nghiệm thu

Trước khi xác nhận một chế độ hoạt động, có kiểm thử thực cho cả Anh và Việt:

- PDF/Word → MD: so sánh với MarkItDown local cùng cấu hình trên fixture đã biết; kiểm tra văn bản, heading, danh sách, bảng và ký tự đặc biệt mà bộ chuyển đổi hỗ trợ.
- MD → DOCX/PDF: kiểm tra H1–H6 và chữ đậm đều Arial 15 pt, đậm, đen; chữ thường Arial 11 pt. Kiểm tra cấu trúc DOCX và render PDF để kiểm tra trực quan, không chỉ so khớp văn bản.
- Word → PDF: kiểm tra font/cỡ chữ gốc, bảng, ảnh, header/footer và ngắt trang trên fixture có mẫu kỳ vọng.
- Kiểm tra tên tệp có dấu/khoảng trắng, đường dẫn dài trong khả năng Windows, tệp hỏng, PDF scan, nguồn thiếu, đích không ghi được, trùng tên, thiếu Arial/LibreOffice, ảnh thiếu và tác vụ bị hủy.
- Kiểm tra lô có cả tệp hợp lệ và lỗi, tiến độ đúng, GUI không treo, Tab/Enter, đổi ngôn ngữ và DPI cao.
- Với ký tự hoặc cấu trúc chưa hỗ trợ, ứng dụng phải báo giới hạn cụ thể. Không coi việc tạo được tệp là bằng chứng nội dung đúng.

Hoàn thành khi các chế độ trong phạm vi đã qua kiểm thử liên quan, không sửa nguồn, không mất nội dung đã kiểm chứng và mọi giới hạn còn lại được ghi rõ. Chỉ báo đã thực hiện những kiểm tra thực sự chạy.

## Tài liệu kỹ thuật tham chiếu

- [Tkinter và mô hình luồng](https://docs.python.org/3/library/tkinter.html).
- [markdown-it-py: sử dụng token và cây cú pháp](https://markdown-it-py.readthedocs.io/en/latest/using.html).
- [python-docx: định dạng chữ](https://python-docx.readthedocs.io/en/latest/user/text.html).
- [LibreOffice: tham số xuất PDF qua dòng lệnh](https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html).
- MarkItDown: nguồn local được chỉ định ở mục tham chiếu phía trên.
