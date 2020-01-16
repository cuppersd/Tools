from PyPDF2 import PdfFileWriter, PdfFileReader
# 开始页
start_page = 3
# 截止页
end_page = 5
output = PdfFileWriter()
pdf_file = PdfFileReader(open("华为云EI红宝书.pdf", "rb"))
pdf_pages_len = pdf_file.getNumPages()
# 保存input.pdf中的1-5页到output.pdf
for i in range(start_page, end_page):
  output.addPage(pdf_file.getPage(i))
outputStream = open("output.pdf", "wb")
output.write(outputStream)