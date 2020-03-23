import struct
import os,sys,time
from zipfile import ZipFile


filelist = []
disk_list = []

def typeList():
    # 支持文件类型
    # 用16进制字符串的目的是可以知道文件头是多少字节
    # 各种文件头的长度不一样，少半2字符，长则8字符
    return {
        #办公类型文件
        "255044462D312E": ["Adobe Acrobat", [".pdf"]],
        "D0CF11E0": ["Microsoft Office Word/Excel", [".xls",".doc"]],
        "0902060000001000B9045C00": ["Microsoft Office Excel V2", [".xls"]],
        "0904060000001000F6055C00": ["Microsoft Office Excel V4", [".xls"]],
        "7FFE340A": ["Microsoft Office Word", [".doc"]],
        "1234567890FF": ["Microsoft Office Word V6.0", [".doc"]],
        "31BE000000AB0000": ["Microsoft Office Word For DOS 6.0", [".doc"]],
        "5374616E64617264204A": ["Microsoft Access", [".mdb"]],
        #压缩格式文件
        "52617221": ["RAR", [".rar"]],
        "504B0304": ["ZIP", [".zip"]],
        "504B3030504B0304": ["ZIP", [".zip"]],
        #图片格式文件
        "7E424B00": ["PaintShop Pro Image File", [".psp"]],
        "41433130": ["CAD", [".dwg"]],
        "FFD8FF": ["JPEG", [".jpg"]],
        "89504E47": ["PNG", [".png"]],
        "47494638": ["GIF", [".gif"]],
        "49492A00": ["TIFF", [".tif"]],
        #网页格式文件
        "3C3F786D6C": ["XML", [".xml"]],
        "3C21454E54495459": ["XML DTD", [".dtd"]],
        "68746D6C3E": ["HTML", [".html"]],
        #视频格式文档
        "57415645": ["Wave", [".wav"]],
        "41564920": ["AVI", [".avi"]],
        "2E7261FD": ["Real Audio", [".ram" ,".ra"]],
        "2E524D46": ["Real Media", [".rm"]],
        "000001BA": ["MPEG", [".mpg"]],
        "000001B3": ["MPEG", [".mpg"]],
        "6D6F6F76": ["Quicktime", [".mov"]],
        "3026B2758E66CF11": ["Windows Media", [".asf"]],
        "4D546864": ["MIDI", [".mid"]],
        #邮件格式文件
        "44656C69766572792D646174653A": ["Email [thorough only]", [".eml"]],
        "CFAD12FEC5FD746F": ["Outlook Express",[".dbx"]],
        "2142444E": ["Outlook", [".pst"]],
        #文本文档
        "7B5C727466": ["Rich Text Format", [".rtf"]],
        #可执行文件
        "vbxMZ": ["Win Executable", [".exe", ".dll", ".drv", ".vxd", ".sys", ".ocx"]],
    }



def bytes2hex(bytes):
    # 字节码转16进制字符串
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


def discern_zip_file(sfile,cfile,ex,filesize):
    # 细分ZIP类型的文件
    with ZipFile(cfile, "r") as zfile:
        dir = zfile.namelist()
        # print(dir)
        if "[Content_Types].xml" in dir:
            for file in dir:
                if file == "word/document.xml":
                    if ex == ".docx":
                        print("[*]文件类型为Microsoft Office Word")
                    else:
                        print("[!]%s,文件大小%.3f KB" % (sfile, filesize))
                        print("[!]文件后缀被篡改，文件类型为Microsoft Office Word")
                elif file == "ppt/styles.xml":
                    if ex == ".pptx":
                        print("[*]文件类型为Microsoft Office PowerPoint")
                    else:
                        print("[!]%s,文件大小%.3f KB" % (sfile, filesize))
                        print("[!]文件后缀被篡改，文件类型为Microsoft Office PowerPoint")
                elif file == "xl/styles.xml":
                    if ex == "xlsx":
                        print("[*]文件类型为Microsoft Office Excel")
                    else:
                        print("[!]%s,文件大小%.3f KB" % (sfile, filesize))
                        print("[!]文件后缀被篡改，文件类型为Microsoft Office Excel")
        else:
            print("[*]%s,文件大小%.3f KB" % (sfile, filesize))
            print("[*]文件类型为ZIP")


def filetype(filepath,filesize):
    global f_hcode
    # 获取文件类型
    with open(filepath, 'rb') as binfile:
        tl = typeList()
        ftype = '未知！'
        try:
            for hcode in tl.keys():
                numOfBytes = int(len(hcode) / 2)  # 需要读多少字节
                binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
                hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))  # 一个 "B"表示一个字节
                f_hcode = bytes2hex(hbytes)
                if f_hcode == hcode:
                    ftype = tl[hcode][0]
                    break
        except struct.error:
            print("[!]%s,文件大小%.3f KB" % (filepath, filesize))
            print("[!]文件头部缺失")
            pass
        except KeyError:
            print("[!]%s,文件大小%.3f KB" % (filepath, filesize))
            print("[!]文件类型未知")
            pass

    # 判断zip类型文件做进一步细分
    sfile = filepath
    (filepath, tempfilename) = os.path.split(filepath)
    (filename, extension) = os.path.splitext(tempfilename)
    cfile = filepath + "\\" + filename + ".zip"
    ex = extension
    if ftype == "ZIP":
        os.rename(sfile, cfile)
        discern_zip_file(sfile, cfile, ex, filesize)
        os.rename(cfile, sfile)
    else:
        if ex in tl[f_hcode][1]:
            # print("[*]%s,文件大小%.3f KB" % (sfile, filesize))
            # print("[*]文件类型为%s" % ftype)
            pass
        else:
            filelist.append(filepath)
            # print("[!]%s,文件大小%.3f KB" % (sfile, filesize))
            # print("[!]文件后缀被篡改，文件类型为%s" % ftype)
    return ftype


def bianli(rootDir):
    #遍历目录
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            filesize = os.path.getsize(os.path.join(root,file))/1024
            path = os.path.join(root, file)
            print(path)
            try:
                f_type = filetype(path,filesize)
                print(f_type)
                if f_type == 'Adobe Acrobat':
                    os.rename(path, path + '.pdf')
            except:
                print("this is a error...")


def count(rootDir):
    #统计文件数量
    count1 = 0  # 计数大文件夹下共有多少个小文件夹
    for root,dirs,fs in os.walk(rootDir):
        for f in fs:
            path = os.path.join(root, f)
            count1 += 1
    print("[*]目录中文件数量为%s" %count1)



if __name__ == '__main__':

    # rootdir = input("./filespdf/")
    count = count("./file/")
    bianli("./file/")