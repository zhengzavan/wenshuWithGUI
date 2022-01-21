import os
import zipfile
from win32com import client as wc
def filesInFolder(folderpath, suffix):
    '''获取文件夹中指定后缀的文件名'''
    files = os.listdir(folderpath)
    filesNames = [name for name in files if name.endswith(suffix)]
    return filesNames

def unzip(filePath, decompressedFolderPath = 'docs'):
    '''解压文件'''
    if not os.path.isdir(decompressedFolderPath):
        os.mkdir(decompressedFolderPath)
    try:
        zip_file = zipfile.ZipFile(filePath)
        for name in zip_file.namelist():
            zip_file.extract(name, decompressedFolderPath)
    except Exception as e:
        print(e)
    finally:
        zip_file.close()
    return decompressedFolderPath

def transform(docsFolder, txtFolder = 'txts'):
    '''将制定文件夹中的doc转成txt'''
    if not os.path.isdir(txtFolder):
        os.mkdir(txtFolder)
    txtFolderTemp = txtFolder
    files = filesInFolder(docsFolder,'.doc')
    docsFolder = os.path.abspath(docsFolder)
    txtFolder = os.path.abspath(txtFolder)
    docsFolder.replace(r'/', r'//')
    txtFolder.replace(r'/', r'//')
    try:
        word = wc.Dispatch("Word.Application")
        for file in files:
            try:
                doc = word.Documents.Open(docsFolder + r'\\' + file)
                doc.SaveAs(txtFolder + r'\\' + file.replace('.doc', '.txt'), 4)
            except Exception as e:
                print('文件转换异常')
            finally:
                doc.Close()

    except Exception as e:
        print("转换异常")
        print(e)
    finally:
        word.Quit()
    return txtFolder

def run(zipsFolder):
    zips = filesInFolder(zipsFolder,'.zip')
    for zip in zips:
         docsFolderPath = unzip(zipsFolder + r'/' + zip)
    transform(docsFolderPath)

if __name__ == '__main__':
    run('zips')