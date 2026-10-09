"""Small Vietnamese/English message table; document text is never translated."""

TEXT = {
    "markdown_extension": (
        "Cú pháp footnote/math mở rộng được giữ dưới dạng chữ; chưa dựng cấu trúc tương ứng.",
        "Extended footnote/math syntax is kept as text; its structure is not rendered.",
    ),
    "docx_merged_math": (
        "DOCX có ô gộp hoặc công thức. Chưa xác nhận giữ đủ cấu trúc; đối chiếu với nguồn.",
        "DOCX contains merged cells or equations. Full structure is unverified; review the source.",
    ),
    "external_resource": (
        "Word có tài nguyên liên kết ngoài: {detail}. "
        "Hãy nhúng tài nguyên vào DOCX trước khi xuất PDF.",
        "Word contains an external resource: {detail}. "
        "Embed the resource in DOCX before exporting PDF.",
    ),
    "title": ("Chuyển đổi tài liệu", "Document converter"),
    "source": ("Tệp hoặc thư mục nguồn", "Source file or folder"),
    "destination": ("Thư mục lưu kết quả", "Output folder"),
    "file": ("Chọn tệp", "Choose file"),
    "supported_files": ("Tài liệu hỗ trợ", "Supported documents"),
    "all_files": ("Tất cả tệp", "All files"),
    "markdown_output": (
        "Chọn Word (.docx) hoặc PDF cho tệp .md. Tiêu đề/chữ đậm: Arial 15 pt; "
        "chữ thường: Arial 11 pt. Giữ ảnh local cạnh tệp Markdown.",
        "Choose Word (.docx) or PDF for .md files. Headings/bold: Arial 15 pt; "
        "body: Arial 11 pt. Keep local images alongside the Markdown file.",
    ),
    "folder": ("Chọn thư mục", "Choose folder"),
    "convert": ("Chuyển đổi", "Convert"),
    "cancel": ("Hủy", "Cancel"),
    "mode": ("Chế độ chuyển đổi", "Conversion mode"),
    "pdf_md": ("PDF → Markdown", "PDF → Markdown"),
    "word_md": ("Word → Markdown", "Word → Markdown"),
    "md_pdf": ("Markdown → PDF", "Markdown → PDF"),
    "md_word": ("Markdown → Word", "Markdown → Word"),
    "word_pdf": ("Word → PDF", "Word → PDF"),
    "ready": (
        "Sẵn sàng. Chọn nguồn, thư mục lưu và chế độ.",
        "Ready. Choose a source, output folder and mode.",
    ),
    "local": (
        "Xử lý trên máy • Word dùng .docx • Thư mục không gồm thư mục con",
        "Local processing • Word uses .docx • Folders exclude subfolders",
    ),
    "open": ("Mở thư mục kết quả", "Open output folder"),
    "details": ("Xem chi tiết", "View details"),
    "created": ("Đã tạo thư mục lưu: {path}", "Created output folder: {path}"),
    "working": ("Đang xử lý {current}/{total}: {name}", "Processing {current}/{total}: {name}"),
    "cancelling": (
        "Đang hủy; chờ backend dừng tác vụ hiện tại…",
        "Cancelling; waiting for the current backend to stop…",
    ),
    "cancel_after_file": ("Đang hủy sau tệp hiện tại…", "Cancelling after the current file…"),
    "summary": (
        "Thành công: {success} • Cảnh báo: {warning} • Lỗi: {error} • Hủy: {cancelled}",
        "Success: {success} • Warnings: {warning} • Errors: {error} • Cancelled: {cancelled}",
    ),
    "success": ("Thành công", "Success"),
    "warning": ("Có cảnh báo — cần kiểm tra kết quả", "Warning — review the output"),
    "error": ("Lỗi", "Error"),
    "cancelled": ("Đã hủy", "Cancelled"),
    "missing_lo": (
        "Xuất PDF bị tắt vì chưa tìm thấy LibreOffice Writer. "
        "Cài từ https://www.libreoffice.org/download/ rồi bấm Kiểm tra lại. "
        "Nếu đã cài ở nơi khác, bấm Chọn LibreOffice và chọn soffice.exe trong thư mục program.",
        "PDF export is disabled because LibreOffice Writer was not found. "
        "Install from https://www.libreoffice.org/download/ and click Recheck. "
        "For another installation location, click Choose LibreOffice "
        "and select program/soffice.exe.",
    ),
    "choose_lo": ("Chọn LibreOffice", "Choose LibreOffice"),
    "recheck": ("Kiểm tra lại", "Recheck"),
    "pdf_available": (
        "Đã tìm thấy LibreOffice và Arial. Có thể chọn Markdown → PDF hoặc Word → PDF.",
        "LibreOffice and Arial found. You can select Markdown → PDF or Word → PDF.",
    ),
    "invalid_lo": (
        "Hãy chọn tệp soffice.exe hoặc soffice.com của LibreOffice: {detail}",
        "Select LibreOffice's soffice.exe or soffice.com: {detail}",
    ),
    "missing_arial": (
        "Thiếu bộ font Arial. Cài Arial (thường/đậm/nghiêng/đậm nghiêng) rồi bấm Kiểm tra lại.",
        "Arial fonts are missing. Install regular/bold/italic/bold italic Arial and click Recheck.",
    ),
    "missing_glyph": (
        "Arial thiếu ký tự cần dùng. Chưa tạo kết quả: {detail}",
        "Arial lacks required characters. No output created: {detail}",
    ),
    "pdf_font": (
        "PDF dùng font ngoài Arial; chưa xác nhận kết quả: {detail}",
        "PDF contains non-Arial fonts; output was rejected: {detail}",
    ),
    "invalid_pdf": ("Không đọc được PDF kết quả: {detail}", "Output PDF is unreadable: {detail}"),
    "lo_timeout": ("LibreOffice vượt thời gian chờ 120 giây.", "LibreOffice exceeded 120 seconds."),
    "lo_failed": ("LibreOffice báo lỗi (mã {detail}).", "LibreOffice failed (code {detail})."),
    "empty_paths": ("Nhập đường dẫn nguồn và thư mục lưu.", "Enter the source and output folder."),
    "source_missing": ("Không tìm thấy nguồn: {detail}", "Source not found: {detail}"),
    "legacy_doc": (
        "Chưa hỗ trợ .doc. Hãy lưu tài liệu thành .docx trước.",
        ".doc is not supported. Save the document as .docx first.",
    ),
    "wrong_extension": ("Chế độ này yêu cầu tệp {detail}.", "This mode requires a {detail} file."),
    "no_files": (
        "Thư mục không có tệp {detail} phù hợp (không quét thư mục con).",
        "No matching {detail} files in this folder (subfolders are excluded).",
    ),
    "invalid_mode": ("Chế độ không hợp lệ.", "Invalid conversion mode."),
    "missing_dependency": (
        "Thiếu thư viện {detail}. Chạy lại bước cài đặt trong README.",
        "Missing library {detail}. Repeat the README setup step.",
    ),
    "no_text": (
        "Không trích xuất được văn bản. PDF scan cần OCR riêng; ứng dụng chưa có OCR.",
        "No text could be extracted. Scanned PDFs need OCR; this app has no OCR.",
    ),
    "pdf_empty_pages": (
        "Các trang không có lớp văn bản: {detail}. Chưa hỗ trợ OCR.",
        "Pages without text: {detail}. OCR is not supported.",
    ),
    "pdf_structure": (
        "MarkItDown không giữ bố cục trang/font và có thể không giữ heading, "
        "ảnh hoặc cấu trúc phức tạp của PDF. Hãy đối chiếu với nguồn.",
        "MarkItDown does not preserve page layout/fonts and may lose PDF "
        "headings, images or complex structure. Compare with the source.",
    ),
    "docx_images": (
        "DOCX có ảnh. Biểu diễn ảnh do MarkItDown local quyết định; "
        "ảnh nhúng có thể không được giữ trong Markdown. Hãy kiểm tra nguồn.",
        "DOCX contains images. The local MarkItDown backend controls image "
        "representation; embedded images may be omitted. Review the source.",
    ),
    "docx_headers": (
        "Header/footer Word có thể không được MarkItDown giữ trong Markdown.",
        "Word headers/footers may be omitted by MarkItDown.",
    ),
    "docx_complex": (
        "DOCX có text box hoặc thay đổi được theo dõi; chưa xác nhận giữ đủ cấu trúc.",
        "DOCX contains text boxes or tracked changes; full structure is unverified.",
    ),
    "word_pdf_layout": (
        "LibreOffice có thể dàn trang khác Microsoft Word. "
        "Cần kiểm tra PDF với nguồn; chưa có kiểm thử trực quan trên máy này.",
        "LibreOffice may paginate differently from Microsoft Word. "
        "Review the PDF against its source; visual export is unverified here.",
    ),
    "invalid_utf8": ("Markdown không phải UTF-8: {detail}", "Markdown is not UTF-8: {detail}"),
    "remote_image": (
        "Không tải ảnh Internet/tài nguyên ngoài: {detail}. Dùng ảnh local.",
        "Remote/external images are not downloaded: {detail}. Use a local image.",
    ),
    "missing_image": ("Không tìm thấy ảnh: {detail}", "Image not found: {detail}"),
    "invalid_image": (
        "Ảnh hỏng hoặc định dạng chưa hỗ trợ: {detail}",
        "Image is corrupt or unsupported: {detail}",
    ),
    "image_link": (
        "Đã chèn ảnh nhưng chưa giữ liên kết bọc quanh ảnh.",
        "Image was inserted, but the link around the image was not preserved.",
    ),
    "html_literal": (
        "HTML được giữ dưới dạng chữ, không thực thi hoặc dựng bố cục HTML.",
        "HTML is preserved as literal text; it is never executed or rendered.",
    ),
    "unsupported": (
        "Chưa hỗ trợ cấu trúc Markdown: {detail}. Chưa tạo kết quả.",
        "Unsupported Markdown structure: {detail}. No output created.",
    ),
    "file_error": (
        "Không chuyển đổi được tệp ({detail}). Kiểm tra tệp hỏng, mật khẩu hoặc quyền truy cập.",
        "File conversion failed ({detail}). Check for corruption, passwords or access permissions.",
    ),
    "path_error": (
        "Không truy cập được đường dẫn ({detail}). Kiểm tra đường dẫn và quyền đọc/ghi.",
        "Cannot access the path ({detail}). Check paths and read/write permissions.",
    ),
    "pdf_unverified": (
        "Xuất PDF cần kiểm tra trực quan với tài liệu nguồn trước khi sử dụng.",
        "PDF export needs visual review against the source before use.",
    ),
}


def translate(key: str, language: str = "vi", **values: str | int) -> str:
    return TEXT[key][0 if language == "vi" else 1].format(**values)
