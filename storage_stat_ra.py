import pymongo


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["RealData"]


myclient = [ pymongo.MongoClient("mongodb://localhost:2017/"),pymongo.MongoClient("mongodb://localhost:2018/"),pymongo.MongoClient("mongodb://localhost:2019/"),pymongo.MongoClient("mongodb://localhost:2020/"),pymongo.MongoClient("mongodb://localhost:2021/") ]

mydb = []

for temp in myclient:
    mydb.append(temp["RealData"])

for i in range(5):
	stat_dict = mydb[i].command("dbstats")
	size = stat_dict["storageSize"]
	size = round((float(size/1000000)),5)
	print("Container :")
	print(i+1)
	print("Size in  MB")
	print(size)



