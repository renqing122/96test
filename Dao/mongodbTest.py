from pymongo import MongoClient

host = '121.199.55.52'  # 服务器url
client = MongoClient(host, 27017)  # 服务器端口
db = client.test  # 数据库=test
db.authenticate("man", "233")  # 账号密码
collectionTest = db.test  # collection=test


# 插入文档
def insert(collection, document):
    try:
        collection.insert(document)
    except Exception as e:
        print(e)
        print("success")


# 获取所有文档
def findAll(collection):
    try:
        results = collection.find()  # 获取为cursor
        x = []
        for i in results:  # i为document
            # print(i)
            i.pop("_id")  # 去除_id，否则无法序列化
            x.append(i)  # 将cursor转化为一个字典
        # print(type(results)) <class 'pymongo.cursor.Cursor'>
        return x  # 返回这个字典
    except Exception as e:
        print(e)
        print("success")


# 获取单个文档
def findOne(collection, condition):
    try:
        result = collection.find_one(condition)  # 查询条件
    # print(type(result)) <class 'dict'>
        result.pop("_id")
        return result
    except Exception as e:
        print(e)
        print("success")


# 修改单个文档
def revOne(collection, condition, reset):
    try:
        collection.update_one(condition, reset)
        # print(result)
        # < pymongo.results.UpdateResult object at 0x0000022485BE3FC8 >
    except Exception as e:
        print(e)
        print("success")


# 向tokenList中添加一个token
def addToken(collection, condition, token):
    try:
        collection.update_one(condition, {"$addToSet": {"tokenList": token}})
    except Exception as e:
        print(e)
        print("success")


# tokenList中删除一个token
def deleteToken(collection, condition, token):
    try:
        collection.update_one(condition, {"$pull": {"tokenList": token}})
    except Exception as e:
        print(e)
        print("success")


# tokenList中修改一个token
def deleteToken(collection, condition, token):
    try:
        collection.update_one(condition, {"$pull": {"tokenList": token}})
        collection.update_one(condition, {"$addToSet": {"tokenList": token}})
    except Exception as e:
        print(e)
        print("success")

