#import threading
import queue
import tweepy
from tweepy.api import API
from datetime import datetime
import time
import pymongo
import json
#import clustering_RealTime as CR
import clustering_RealTime_10min as CR10min
import os
#import cosine_sim as cosine_sim
import cosine_sim10min as cosine_sim10min
#import preprocessing as pre
import preprocessing_10min as pre10min
from collections import Counter
import summary_RealTime as sR
import shutil
from keras.engine.saving import load_model
import virality_checker as virality_checker



myclient = [ pymongo.MongoClient("mongodb://localhost:2017/"),pymongo.MongoClient("mongodb://localhost:2018/"),pymongo.MongoClient("mongodb://localhost:2019/"),pymongo.MongoClient("mongodb://localhost:2020/"),pymongo.MongoClient("mongodb://localhost:2021/") ]

mydb = []

for temp in myclient:
    mydb.append(temp["RealData"])


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["RealData"]

# mycol10min = mydb["test10min"]
# #mycol2hour= mydb["test2hour"]
# mycol_virality=mydb["virality"]

path_10min='data/Event_data_10min'
path='data/Event_data'
paths = 'data/single_keywords.txt'

path_top_5_events='data/top_5_events'
path_top_5_events_images='data/top_5_events_images'
path_top_5_events_summary='data/top_5_events_summary'




def remove10min():
	print("i am under remove...................")
	#print("length of documents till now:  ",mydb.test10min.count())
	sum_10min =0
	for i in range(5):
		mycol10min=mydb[i]["test10min"]
		sum_10min = sum_10min + mycol10min.count()
	print("length of documents till now:  ",sum_10min)
	#cursor = mycol10min.find(no_cursor_timeout=True)
	cursor = []
	for i in range(5):
		mycol10min=mydb[i]["test10min"]
		cursor10min = list(mycol10min.find(no_cursor_timeout=True))
		cursor.extend(cursor10min)

	for ele in cursor:
		start_time=ele["created_at"]
		break
	datetime_object = datetime.strptime(str(start_time), '%a %b %d %H:%M:%S +0000 %Y')
	x = time.mktime(datetime_object.timetuple())
		
	delta=600
	req_time=x+delta

	for ele in cursor:
		try:
			datetime_object = datetime.strptime(str(ele["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
			tweet_time = time.mktime(datetime_object.timetuple())
				
			if tweet_time <= req_time:
				#result_del = mydb.test10min.delete_one(ele)
				for i in range(5):
					mycol10min=mydb[i]["test10min"]
					result_del=mycol10min.delete_one(ele)
		except:
			continue
	#cursor.close()

ijk10min=1
def incremental_clus_10min(tweet,id_virality):
	#print("i am in incremental_clus")
	global ijk10min
	dict_similarity={}
	max=0.0
	threshold=0.2
	with open("location_dictionary.json","r") as file:
		di=json.load(file)
	location=tweet["user"]["location"]

	if 'media' in tweet['entities']:
		media=(tweet['entities']['media'])
		media=media[0]
		url=media['media_url']

	else:
		url="none"

	if location:
		for key in di:
			if key in location:
				lat_long=di[key]
	
		list_files=os.listdir(path_10min)
		for single_file in list_files:
			with open("data/Event_data_10min/%s"%single_file,"r") as f:
				for line in f:
					single_file_di=json.loads(line)
				if len(single_file_di) == 0:
					#print("File empty")
					dict_similarity[single_file]=0.0
				else:
					all_tweets=""
					for key,val in single_file_di.items():
						all_tweets=val["text"]+" "+all_tweets
					cosine=cosine_sim10min.cosine_similarity(all_tweets,tweet["text"])
					dict_similarity[single_file]=cosine
				if cosine>max:
					max=cosine
		#print("max_sim: ",max)
		#print("dict similarity: ",dict_similarity)
		#print(tweet["id_str"])
		if max>= threshold:
			#print("existing clus")
			for key,val in dict_similarity.items():
				if val==max:
					#print(key)
					event_name=key.split(".")[0]
					with open("data/Event_data_10min/%s"%key,"r") as f1:
						for line in f1:
							event_file=json.loads(line)
							event_file[tweet["id_str"]]={"id_str":tweet["id_str"],"latitude":lat_long[0],"longitude":lat_long[1],"ename":event_name,"created_at":tweet["created_at"],"user_location":location,"text":tweet["text"],"main_event":0,"user_name":tweet["user"]["name"],"follower_count":tweet["user"]["followers_count"],"retweet_count":tweet["retweet_count"],"image_url":url,"id_virality":id_virality}
					
					#print(event_file)
					with open("data/Event_data_10min/%s"%key,"w") as f2:
						json.dump(event_file,f2)
		elif max < threshold:
			#print("new clus")
			event_file_new_clus={}
			event_name="new_clus"+str(ijk10min)
			event_file_new_clus[tweet["id_str"]]={"id_str":tweet["id_str"],"latitude":lat_long[0],"longitude":lat_long[1],"ename":event_name,"created_at":tweet["created_at"],"user_location":location,"text":tweet["text"],"main_event":0,"user_name":tweet["user"]["name"],"follower_count":tweet["user"]["followers_count"],"retweet_count":tweet["retweet_count"],"image_url":url,"id_virality":id_virality}
			#print(event_file_new_clus)
			with open("data/Event_data_10min/new_clus{0}.json".format(ijk10min),"w") as f3:
				json.dump(event_file_new_clus,f3)
			ijk10min=ijk10min+1

last_time=0.0
def removeTweets_after10min():
	global last_time
	
	i=1
	while True:
		print("i m gonna sleep..................")
		time.sleep(600)
		sum_10min_initial =0
		for i in range(5):
			mycol10min=mydb[i]["test10min"]
			sum_10min_initial = sum_10min_initial + mycol10min.count()
		#if mydb.test10min.count() > 0:
		if sum_10min_initial >0:
			
			if os.listdir(path_10min) == []:
			
				last_time=CR10min.clus()
				print("k meanslast_time",last_time)
				print("Clustering is done..now we wil delete test10min.json")
				if os.path.exists("test10min.json"):
					os.remove("test10min.json")
				else:
					print("The file does not exist") 

			else:
				#print("incremental_clus10min")
				delta=600
				print("last_time",last_time)
				req_time=last_time+delta
				#cursor = mycol10min.find(no_cursor_timeout=True)
				cursor = []
				for i in range(5):
					mycol10min=mydb[i]["test10min"]
					cursor10min = list(mycol10min.find(no_cursor_timeout=True))
					cursor.extend(cursor10min)


				list_created_at=[]
				for ele in cursor:
					try:
						del ele['_id']
						if "retweeted_status" in ele:
							id_virality= ele["retweeted_status"]["id_str"]
						else:
							id_virality= ele["id_str"]
						datetime_object = datetime.strptime(str(ele["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
						tweet_time = time.mktime(datetime_object.timetuple())
						
						list_created_at.append(tweet_time)

						if tweet_time >=last_time and tweet_time <= req_time:
							incremental_clus_10min(ele,id_virality)
						elif tweet_time > req_time:
							print("Done similarity of all tweets")
					except:
						continue
				#cursor.close()
				list_created_at.sort(reverse=True)
				last_time=list_created_at[0]
				#<--------rename events----------->				
				list_files=os.listdir(path_10min)
				for single_file in list_files:
					with open("data/Event_data_10min/%s"%single_file,"r") as f:
						for line in f:
							single_file_di=json.loads(line)
							if len(single_file_di) == 0:
								os.remove("data/Event_data_10min/%s"%single_file)
				
							else:
								all_tweets=""
								for key,val in single_file_di.items():
									all_tweets=val["text"]+" "+all_tweets
								#<--preprocess all tweets---->
								all_tweets=pre10min.preprocessing_tweets(all_tweets)

								if not all_tweets:
									os.remove("data/Event_data_10min/%s"%single_file)
					
								else: 
									list_words=all_tweets.split()
									x=Counter(list_words)
									y=x.most_common(3)
									#print(y)
									if len(y)==3:
										event_name=y[0][0]+" "+y[1][0]+" "+y[2][0]
									elif len(y)==2:
										event_name=y[0][0]+" "+y[1][0]
									elif len(y)==1:
										event_name=y[0][0]
									elif len(y)==0:
										event_name="Empty"

									print("#################   Event name:   ",event_name)
									os.rename("data/Event_data_10min/%s"%single_file,"data/Event_data_10min/%s.json"%event_name) 
				#cursor.close()
			#<-----------------Virality Prediction---------------------------->
			sum_virality =0
			for i in range(5):
				mycol_virality=mydb[i]["virality"]
				sum_virality = sum_virality + mycol_virality.count()
			#if mydb.virality.count()>0:
			if sum_virality>0:
				virality_checker.virality_predictor()
				#mycol_virality.remove({})
				for i in range(5):
					mycol_virality=mydb[i]["virality"]
					mycol_virality.remove({})

			else:
				print("Unable to do virality ..collection empty")
			
		else:
			print("Unable to do CLUSTERING......Collection EMPTY :(")

		

		if i == 4:
			sum_10min =0
			for i in range(5):
				mycol10min=mydb[i]["test10min"]
				sum_10min = sum_10min + mycol10min.count()

			#if mydb.test10min.count() > 0:
			if sum_10min > 0:
				#print("Before deleting:....",mydb.test10min.count())
				print("Before deleting:....",sum_10min)
				#remove10min()
				for i in range(5):
					mycol10min=mydb[i]["test10min"]
					mycol10min.remove({})
				#print("After deleting:....",mydb.test10min.count())
				sum_10min_new =0
				for i in range(5):
					mycol10min=mydb[i]["test10min"]
					sum_10min_new = sum_10min_new + mycol10min.count()
				print("After deleting:....", sum_10min_new)
			else:
				print("Collection is EMPTY....... ### UNABLE to DELETE   SORRY   :(")

		if i >= 5:
			sum_10min =0
			for i in range(5):
				mycol10min=mydb[i]["test10min"]
				sum_10min = sum_10min + mycol10min.count()
			#if mydb.test10min.count() > 0:
			if sum_10min > 0:
				#print("Before deleting:....",mydb.test10min.count())
				print("Before deleting:....",sum_10min)
				#remove10min()
				for i in range(5):
					mycol10min=mydb[i]["test10min"]
					mycol10min.remove({})
				#print("After deleting:....",mydb.test10min.count())
				sum_10min_new =0
				for i in range(5):
					mycol10min=mydb[i]["test10min"]
					sum_10min_new = sum_10min_new + mycol10min.count()
				print("After deleting:....", sum_10min_new)
			else:
				print("Collection is EMPTY....... ### UNABLE to DELETE   SORRY.....")


		i=i+1

#def begin():
if __name__ == '__main__':
	removeTweets_after10min()