# from PyPDF2 import PdfFileReader, PdfFileWriter
#
#
# def splitPDF():
#     # C:\Users\knighthood\OneDrive\桌面\python合集\Python爬虫开发与项目实战.pdf
#     readFile = input('请输入原PDF的所在位置与名称：')
#     # .\copy.pdf 该格式使得pdf在当前目录下
#     outFile = input('请输入你要将生成的PDF保存的位置与名称：')
#     # 调用PdfFileWriter()类
#     pdfFileWriter = PdfFileWriter()
#
#     # 获取PdfFileReader 对象
#     pdfFileReader = PdfFileReader(readFile)
#     # 文档总页数
#     numPages = pdfFileReader.getNumPages()
#     print("原文档有{}页".format(numPages))
#
#     a = int(input('从哪一页开始：'))
#     b = int(input('到哪一页结束：'))
#     c = b - a + 1
#     # 显示新文档有几页
#     print("新文档共有{}页".format(c))
#     for i in range(a - 1, b):
#         page = pdfFileReader.getPage(i)
#         pdfFileWriter.addPage(page)
#
#     # 添加完每页，然后一起保存在outFile中
#     with open(outFile, 'wb') as f:
#         pdfFileWriter.write(f)
#
#
# splitPDF()


import PyPDF2

# 打开pdf文件
pdf_file = open('read.pdf', 'rb')

# 创建一个PDF对象
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# 遍历每一页
for page_num in range(pdf_reader.numPages):
    # 获取当前页对象
    page = pdf_reader.getPage(page_num)
    # 获取当前页中的文本
    text = page.extractText()
    # 打印文本
    print(text)

# 关闭pdf文件
pdf_file.close()
