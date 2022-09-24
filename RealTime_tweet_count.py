import pymongo
import time
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["RealData"]
mycol_total=mydb["all_data"]
mycol_virality=mydb["virality"]
mycol_virality_keyword = mydb["virality_keyword"]
mycol_total_keyword=mydb["all_data_keyword"]

# while True:
# 	time.sleep(60)
print("Total no of tweets:    ",mycol_total.count())
print("Total no of tweets:    ",mycol_virality.count())
print("Total no of violent tweets keyword:    ",mycol_virality_keyword.count())
print("Total no of all tweets keyword:    ",mycol_total_keyword.count())
