import json
from flask import Blueprint
from flask import request
from Dao import mongodbTest

textAnnotation = Blueprint("textAnnotation", __name__, url_prefix="/textAnnotation")
collectionTest = mongodbTest.db.textJob
# token = {'entityId': "2", 'word': "滑坡2号", 'begin': "15", 'end': "18", 'attribute': "滑坡 基本信息 滑坡名称"}
# x = mongodbTest.revOne(collectionTest, {'annotatorId': "10"}, {"$set": {'fragmentId': "1000"}})
# x = mongodbTest.findAll(collectionTest)
# mongodbTest.insert(collectionTest, {'annotatorId': "11", 'fragmentId': "1001",
#                     'textUrl': "1593694770.xlsx", 'tokenList': []})
# mongodbTest.addToken(collectionTest, {'documentId': "1681f208a18a11ea86ae54e1ad87433a"}, token)
# mongodbTest.deleteToken(collectionTest, {'documentId': "53b32eee9f2911eab9dc54e1ad87433a"}, {'tokenId': "979433429f2911ea823554e1ad87433a"})

# token.update({'tokenId': "8a7bfd409f2a11eabcd454e1ad87433a"})
# mongodbTest.revToken(collectionTest, {'documentId': "53b32eee9f2911eab9dc54e1ad87433a"}, token)


# @textAnnotation.route("/")
# def hello_world():
#     return json.dumps(x, ensure_ascii=False)

# 获取所有Token
@textAnnotation.route("/getTokenList", methods=["POST"])
def getTokenList():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}

    # 判断传入的json数据是否为空
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

    return_dict['result'] = result.get('tokenList')
    return json.dumps(return_dict, ensure_ascii=False)


# 添加Token
@textAnnotation.route("/addToken", methods=["POST"])
def addToken():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空

    try:
        get_Data = request.get_data()
        get_Data = json.loads(get_Data)
    except Exception as e:
        return_dict['return_code'] = '201'
        return_dict['return_info'] = '请求参数有误'
        return json.dumps(return_dict, ensure_ascii=False)

    documentId = get_Data.get('documentId')
    token = get_Data.get('token')

    if mongodbTest.findOne(collectionTest, {"documentId": documentId}) is None:
        return_dict['return_code'] = '203'
        return_dict['return_info'] = '失败'
        return json.dumps(return_dict, ensure_ascii=False)

    result = mongodbTest.addToken(collectionTest, {"documentId": documentId}, token)

    # 判断是否返回结果
    if result is None:
        return_dict['return_code'] = '203'
        return_dict['return_info'] = '插入失败'
        return json.dumps(return_dict, ensure_ascii=False)

    return_dict['result'] = result
    return json.dumps(return_dict, ensure_ascii=False)


# 删除Token
@textAnnotation.route("/deleteToken", methods=["POST"])
def deleteToken():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空
    try:
        get_Data = request.get_data()
        get_Data = json.loads(get_Data)
    except Exception as e:
        return_dict['return_code'] = '201'
        return_dict['return_info'] = '请求参数有误'
        return json.dumps(return_dict, ensure_ascii=False)

    documentId = get_Data.get('documentId')
    tokenId = get_Data.get('tokenId')

    # document是否存在
    if mongodbTest.findOne(collectionTest, {"documentId": documentId}) is None:
        return_dict['return_code'] = '204'
        return_dict['return_info'] = '删除失败'
        return json.dumps(return_dict, ensure_ascii=False)

    # 判断token是否存在
    result = mongodbTest.findToken(collectionTest, {"documentId": documentId}, {"tokenId": tokenId})
    print(result)
    if result is None:
        return_dict['return_code'] = '205'
        return_dict['return_info'] = 'token不存在'
        return json.dumps(return_dict, ensure_ascii=False)

    mongodbTest.deleteToken(collectionTest, {"documentId": documentId}, {"tokenId": tokenId})

    # return_dict['result'] = result
    return json.dumps(return_dict, ensure_ascii=False)


# 修改token
@textAnnotation.route("/revToken", methods=["POST"])
def revToken():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}

    # 判断传入的json数据是否为空
    try:
        get_Data = request.get_data()
        get_Data = json.loads(get_Data)
    except Exception as e:
        return_dict['return_code'] = '201'
        return_dict['return_info'] = '请求参数有误'
        return json.dumps(return_dict, ensure_ascii=False)

    documentId = get_Data.get('documentId')
    token = get_Data.get('token')

    # document是否存在
    if mongodbTest.findOne(collectionTest, {"documentId": documentId}) is None:
        return_dict['return_code'] = '206'
        return_dict['return_info'] = '修改失败'
        return json.dumps(return_dict, ensure_ascii=False)

    # 判断token是否存在
    result = mongodbTest.findToken(collectionTest, {"documentId": documentId}, {"tokenId": token.get('tokenId')})
    print(result)
    if result is None:
        return_dict['return_code'] = '205'
        return_dict['return_info'] = 'token不存在'
        return json.dumps(return_dict, ensure_ascii=False)

    mongodbTest.revToken(collectionTest, {"documentId": documentId}, token)

    # return_dict['result'] = result
    return json.dumps(return_dict, ensure_ascii=False)