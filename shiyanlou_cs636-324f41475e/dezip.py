#_*_coding=UTF-8_*_
import zipfile
try:
    with zipfile.ZipFile('deZip/1.zip') as zFile:#创建ZipFile对象
        #解压文件
        zFile.extractall(path='./deZip/', pwd=b'1314')
        print('Extract the Zip file successfully!')
except:
    print('Extract the Zip file failed!')
