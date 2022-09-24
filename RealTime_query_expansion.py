import pymongo
import time
import os.path

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["RealData"]

mycol10min = mydb["test10min"]
mycol2hour= mydb["test2hour"]
mycol_virality=mydb["virality"]

mycol_ve = mydb["ve"]
mycol_nve = mydb["nve"]
mycol_rv = mydb["rv"]
mycol_nrv = mydb["nrv"]
mycol_total=mydb["all_data"]

def createDynamicKeywords():
	cursor = mycol2hour.find(no_cursor_timeout=True)
	hashtag=[]
	for ele in cursor:
		try:
			#del ele['_id']
			# tweet=ele["text"]
			# print(tweet)
			lis=ele["entities"]["hashtags"]
			for e in lis:
				hashtag.append(e["text"])
				
		except:
			continue

	#print(hashtag);input()
	from collections import Counter
	word_freq=Counter(hashtag)
	#print(word_freq)
	newKeywords=word_freq.most_common(4)
	
	return (newKeywords)

def getKeywords():
	i=0
	while True:
		print("Waiting...................")
		time.sleep(300)
		newKeywords=createDynamicKeywords()
		listKeywords=[]

		for ele in newKeywords:
			listKeywords.append(ele[0])

		print(listKeywords)

		existingKeywords=[]
		if os.path.isfile('DynamicKeywords.txt'):
			with open("DynamicKeywords.txt","r") as f1:
				for line in f1:
					line = line.strip()
					existingKeywords.append(line)

		
		with open("DynamicKeywords.txt","a") as f2:
			for keyword in listKeywords:
				if keyword not in existingKeywords:
					f2.write(keyword)
					f2.write("\n")

		i=i+1
		print("{0}th query expansion is DONE....!!!!!!!!!!!!!!!!".format(i))


if __name__== "__main__":
   getKeywords()
