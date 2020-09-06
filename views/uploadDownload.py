import json
import os
import time
from datetime import datetime
import zipfile
import xlrd

from flask import Blueprint
from xlrd import xldate_as_tuple

from Dao import mongodbTest
from support import basedir
from flask import jsonify, request, send_file
from werkzeug.utils import secure_filename

uploadDownload = Blueprint("uploadDownload", __name__, url_prefix="/uploadDownload")
UPLOAD_FOLDER = 'upload'  # 用于保存上传文件的文件夹名称
ZIP_FOLDER = 'zip'  # 用于保存zip文件的文件夹名称
ALLOWED_EXTENSIONS = {'txt', 'xls', 'xlsx'}  # 允许上传的文件格式
collectionTest = mongodbTest.db.textJob


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 上传文件
@uploadDownload.route('/upload', methods=['POST'], strict_slashes=False)
def upload():
    file_dir = os.path.join(basedir, UPLOAD_FOLDER)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值

    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fName = secure_filename(f.filename)
        ext = fName.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        print(new_filename)

        return jsonify({"errno": 0, "msg": "succeed ", "token": new_filename})
    else:
        return jsonify({"errno": 1001, "errmsg": u"failed"})


# 下载接口
@uploadDownload.route('/download/<fileName>', methods=['GET'])
def download(fileName):
    file_dir = os.path.join(basedir, UPLOAD_FOLDER, fileName)
    return send_file(file_dir, as_attachment=True, attachment_filename=fileName)

# 生成标注结果文件
@uploadDownload.route('/test', methods=['GET'])
def test():
    file_dir = os.path.join(basedir, UPLOAD_FOLDER) # 标注结果文件保存位置
    fileName = '1590310217.txt'  #原始文件文件名
    portion = os.path.splitext(fileName)  # 获取文件前缀名 如1590310217.txt   portion[0]则为1590310217
    new_name = portion[0] + 'result.txt'  # 新的文件名字 如1590310217result.txt
    full_path = os.path.join(file_dir, new_name) # 标注结果文件保存位置 + 标注结果文件名
    file = open(full_path, 'w',encoding='utf8')  #打开文件
    file.write("i am result 喵") #写入标注结果字符串
    file.close() #关闭文件
    return "true"

# 下载压缩包接口
@uploadDownload.route('/downloadZip/<fileName>', methods=['GET'])
def downloadZip(fileName):
    file_dir = os.path.join(basedir, UPLOAD_FOLDER) # 被压缩的文件所在文件夹路径  如 D:\learn\python-project\demo\upload
    zip_dir = os.path.join(basedir, ZIP_FOLDER) # 压缩后的文件所在文件夹路径 如 D:\learn\python-project\demo\zip
    portion = os.path.splitext(fileName) # 获取文件前缀名 如1590310217.txt   portion[0]则为1590310217
    new_name = portion[0] + '.zip' # 新的文件名字 如1590310217.zip
    zipname = os.path.join(zip_dir,new_name) # 压缩的文件夹名字及路径 如 D:\learn\python-project\demo\zip\1590310217.zip （这是我电脑上的路径）
    f = zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED) #创建压缩文件 'w'：写模式    ZIP_DEFLATED：设置压缩格式
    flist = os.listdir(file_dir) #找到被压缩的文件所在的地址
    basename = fileName  #压缩后文件的根目录叫啥
    for name in flist:  #我这个是遍历的 把upload全部压缩了
        fpath = os.path.join(file_dir, name)  # fpath就是被压缩的文件的路径的集合 file_dir代表被压缩的文件的路径 name是被压缩的文件的名字
        arcname = os.path.join(basename, name) # 这个不用管 是为了让压缩后的文件的根目录只有一层 不然会套娃n个文件夹（一层路径一个文件夹）
        f.write(fpath,arcname=arcname)  #写进去 压缩！
    f.close() #关闭
    return send_file(zipname, as_attachment=True, attachment_filename=new_name) #返回！


# 显示文档
@uploadDownload.route('/getfile/<path>', methods=['GET'])
def today(path):
    fileStr = open(os.path.join(basedir, UPLOAD_FOLDER, path), 'r', encoding='UTF-8').read()
    x1 = [{"file": fileStr}]
    x1 = [{"1":2}]
    return json.dumps(x1, ensure_ascii=False)


# 显示表格
@uploadDownload.route('/getExcel/<path>', methods=['GET'])
def read_excel(path):
    # 打开文件
    workbook = xlrd.open_workbook(os.path.join(basedir, UPLOAD_FOLDER, path))
    statement = []

    # 遍历sheets
    sheets = len(workbook.sheets())
    data = {"numOfSheet": sheets}
    for sheet in range(sheets):
        d1 = {"sheetName": workbook.sheet_by_index(sheet).name}
        rows = workbook.sheet_by_index(sheet).nrows
        cols = workbook.sheet_by_index(sheet).ncols
        d1.update({"numOfRow": rows})
        d1.update({"numOfCol": cols})
        d2 = []
        for row in range(rows):
            for col in range(cols):
                ctype = workbook.sheet_by_index(sheet).cell(row, col).ctype
                cell = workbook.sheet_by_index(sheet).cell_value(row, col)
                if ctype == 2 and cell % 1 == 0.0:
                    cell = int(cell)
                    cell = str(cell)
                elif ctype == 3:
                    date = datetime(*xldate_as_tuple(cell, 0))
                    cell = date.strftime('%Y/%m/%d %H:%M:%S')
                d2.append({"value": cell})
        d1.update({"content": d2})
        statement.append(d1)
    data.update({"content": statement})
    return json.dumps(data, ensure_ascii=False)


# documentId获取文本内容
@uploadDownload.route('/getFileContent', methods=['POST'])
def getFileContent():
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    try:
        get_Data = request.get_data()
        get_Data = json.loads(get_Data)
    except Exception as e:
        return_dict['return_code'] = '201'
        return_dict['return_info'] = '请求参数有误'
        return json.dumps(return_dict, ensure_ascii=False)

    documentId = get_Data.get('documentId')
    result = mongodbTest.findOne(collectionTest, {"documentId": documentId})

    # 判断是否查询到结果
    if result is None:
        return_dict['return_code'] = '202'
        return_dict['return_info'] = '获取失败'
        return json.dumps(return_dict, ensure_ascii=False)

    url = result.get('textUrl')
    fileStr = open(os.path.join(basedir, UPLOAD_FOLDER, url), 'r', encoding='UTF-8').read()
    return_dict['result'] = fileStr

    return json.dumps(return_dict, ensure_ascii=False)


# documentId获取表格内容
@uploadDownload.route('/getExcelContent', methods=['POST'])
def getExcelContent():
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    try:
        get_Data = request.get_data()
        get_Data = json.loads(get_Data)
    except Exception as e:
        return_dict['return_code'] = '201'
        return_dict['return_info'] = '请求参数有误'
        return json.dumps(return_dict, ensure_ascii=False)

    documentId = get_Data.get('documentId')
    result = mongodbTest.findOne(collectionTest, {"documentId": documentId})

    # 判断是否查询到结果
    if result is None:
        return_dict['return_code'] = '202'
        return_dict['return_info'] = '获取失败'
        return json.dumps(return_dict, ensure_ascii=False)

    url = result.get('textUrl')

    # 打开文件
    workbook = xlrd.open_workbook(os.path.join(basedir, UPLOAD_FOLDER, url))
    statement = []

    # 遍历sheets
    sheets = len(workbook.sheets())
    data = {"numOfSheet": sheets}
    for sheet in range(sheets):
        d1 = {"sheetName": workbook.sheet_by_index(sheet).name}
        rows = workbook.sheet_by_index(sheet).nrows
        cols = workbook.sheet_by_index(sheet).ncols
        d1.update({"numOfRow": rows})
        d1.update({"numOfCol": cols})
        d2 = []
        for row in range(rows):
            for col in range(cols):
                ctype = workbook.sheet_by_index(sheet).cell(row, col).ctype
                cell = workbook.sheet_by_index(sheet).cell_value(row, col)
                if ctype == 2 and cell % 1 == 0.0:
                    cell = int(cell)
                    cell = str(cell)
                elif ctype == 3:
                    date = datetime(*xldate_as_tuple(cell, 0))
                    cell = date.strftime('%Y/%m/%d %H:%M:%S')
                d2.append({"value": cell})
        d1.update({"content": d2})
        statement.append(d1)
    data.update({"content": statement})
    return_dict["result"] = data
    return json.dumps(return_dict, ensure_ascii=False)
