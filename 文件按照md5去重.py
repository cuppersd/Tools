import hashlib
import os
import shutil
 
def calculate_file_md5(file_path):
    try:
        md5 = hashlib.md5()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                md5.update(chunk)
        return md5.hexdigest()
    except IOError:
        print("文件读取错误")
        return None

md5_list = []


for fn in os.listdir("./0606/"):
    f_p = "./0606/" + fn
    v_md5 = calculate_file_md5(f_p)
    if v_md5 in md5_list:
        os.remove(f_p)
    else:
        md5_list.append(v_md5)
