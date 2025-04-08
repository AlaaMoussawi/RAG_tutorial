from docling.document_converter import DocumentConverter
# pip install accelerate


def extract_text(source):
    converter = DocumentConverter()
    result = converter.convert(source)

    return result.document.export_to_markdown()

pptx_source = "https://scholar.harvard.edu/files/torman_personal/files/samplepptx.pptx"
docx_source = "https://www.cte.iup.edu/cte/Resources/DOCX_TestPage.docx"
pdf_source = "https://pdfobject.com/pdf/sample.pdf"

extract_text(pdf_source)