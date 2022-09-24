import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["RealData"]
mycol_virality=mydb["virality"]


def removeTweets_after10min():
	i=1
	while True:
		print("i m gonna sleep..................")
		time.sleep(600)

		if i >= 1:
			if mydb.test10min.count() > 0:
				print("Before deleting:....",mydb.test10min.count())
				remove10min()
				print("After deleting:....",mydb.test10min.count())
			else:
				print("Collection is EMPTY....... ### UNABLE to DELETE   SORRY.....")


		i=i+1






if __name__ == '__main__':
	removeTweets_after10min()
