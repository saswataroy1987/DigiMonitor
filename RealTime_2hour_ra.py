#import threading

import queue
import tweepy
from tweepy.api import API
from datetime import datetime
import time
import pymongo
import json
import clustering_RealTime as CR
import clustering_RealTime_10min as CR10min
import os
import cosine_sim as cosine_sim
import cosine_sim10min as cosine_sim10min
import preprocessing as pre
import preprocessing_10min as pre10min
from collections import Counter
import summary_RealTime as sR
import tweet_with_images_RealTime as iR
import shutil
import sys



myclient = [ pymongo.MongoClient("mongodb://localhost:2017/"),pymongo.MongoClient("mongodb://localhost:2018/"),pymongo.MongoClient("mongodb://localhost:2019/"),pymongo.MongoClient("mongodb://localhost:2020/"),pymongo.MongoClient("mongodb://localhost:2021/") ]

mydb = []

for temp in myclient:
    mydb.append(temp["RealData"])




# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["RealData"]

# mycol10min = mydb["test10min"]
# mycol2hour= mydb["test2hour"]


path_10min='data/Event_data_10min'
path='data/Event_data'
paths = 'single_keywords.txt'

path_top_5_events='data/top_5_events'
path_top_5_events_images='data/top_5_events_images'
path_top_5_events_summary='data/top_5_events_summary'

def remove2hour():
	print("i am under remove...................")
	#print("length of documents till now:  ",mydb.test2hour.count())
	sum_2hour =0
	for i in range(5):
		mycol2hour=mydb[i]["test2hour"]
		sum_2hour = sum_2hour + mycol2hour.count()
	print("length of documents till now:  ",sum_2hour)
	#cursor = mycol2hour.find(no_cursor_timeout=True)
	cursor = []
	for i in range(5):
		mycol2hour=mydb[i]["test2hour"]
		#print(mycol2hour.count())
		cursor2hour = list(mycol2hour.find(no_cursor_timeout=True))
		cursor.extend(cursor2hour)



	for ele in cursor:
		start_time=ele["created_at"]
		break
	datetime_object = datetime.strptime(str(start_time), '%a %b %d %H:%M:%S +0000 %Y')
	x = time.mktime(datetime_object.timetuple())
		
	delta=3600
	req_time=x+delta

	for ele in cursor:
		try:
			datetime_object = datetime.strptime(str(ele["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
			tweet_time = time.mktime(datetime_object.timetuple())
				
			if tweet_time <= req_time:
				#result_del = mydb.test2hour.delete_one(ele)
				for i in range(5):
					mycol2hour=mydb[i]["test2hour"]
					result_del=mycol2hour.delete_one(ele)
		except:
			continue
	#cursor.close()


ijk=1
def incremental_clus(tweet):
	#print("i am in incremental_clus")
	global ijk
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
	
		list_files=os.listdir(path)
		for single_file in list_files:
			with open("data/Event_data/%s"%single_file,"r") as f:
				for line in f:
					single_file_di=json.loads(line)
				if len(single_file_di) == 0:
					#print("File empty")
					dict_similarity[single_file]=0.0
				else:
					all_tweets=""
					for key,val in single_file_di.items():
						all_tweets=val["text"]+" "+all_tweets
					cosine=cosine_sim.cosine_similarity(all_tweets,tweet["text"])
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
					with open("data/Event_data/%s"%key,"r") as f1:
						for line in f1:
							event_file=json.loads(line)
							event_file[tweet["id_str"]]={"id_str":tweet["id_str"],"latitude":lat_long[0],"longitude":lat_long[1],"ename":event_name,"created_at":tweet["created_at"],"user_location":location,"text":tweet["text"],"main_event":0,"user_name":tweet["user"]["name"],"follower_count":tweet["user"]["followers_count"],"retweet_count":tweet["retweet_count"],"image_url":url}
					
					#print(event_file)
					with open("data/Event_data/%s"%key,"w") as f2:
						json.dump(event_file,f2)
		elif max < threshold:
			#print("new clus")
			event_file_new_clus={}
			event_name="new_clus"+str(ijk)
			event_file_new_clus[tweet["id_str"]]={"id_str":tweet["id_str"],"latitude":lat_long[0],"longitude":lat_long[1],"ename":event_name,"created_at":tweet["created_at"],"user_location":location,"text":tweet["text"],"main_event":0,"user_name":tweet["user"]["name"],"follower_count":tweet["user"]["followers_count"],"retweet_count":tweet["retweet_count"],"image_url":url}
			#print(event_file_new_clus)
			with open("data/Event_data/new_clus{0}.json".format(ijk),"w") as f3:
				json.dump(event_file_new_clus,f3)
			ijk=ijk+1

last_time=0.0
def removeTweets_after2hrs():
	#global p
	global last_time
	i=1
	while True:
		print("i m gonna sleep..................")
		time.sleep(600)
		sum_2hour_initial =0
		for i in range(5):
			mycol2hour=mydb[i]["test2hour"]
			sum_2hour_initial = sum_2hour_initial + mycol2hour.count()
		#if mydb.test2hour.count() > 0:
		if sum_2hour_initial > 0:
			if os.listdir(path) == []:
			
				last_time=CR.clus()
				print("Clustering is done..now we wil delete test.json")
				if os.path.exists("test.json"):
					os.remove("test.json")
				else:
					print("The file does not exist") 
				#<--------deleting required files----->

				list_files_top_5_events=os.listdir(path_top_5_events)
				list_files_event_images=os.listdir(path_top_5_events_images)
				list_files_event_summary=os.listdir(path_top_5_events_summary)

				for single_file in list_files_top_5_events:
					os.remove('data/top_5_events/%s'%single_file)

				for single_file in list_files_event_images:
					os.remove('data/top_5_events_images/%s'%single_file)

				for single_file in list_files_event_summary:
					os.remove('data/top_5_events_summary/%s'%single_file)

				#<-----summary generation initializaion---->
				

				list_files=os.listdir(path)
				list_tuples=[]
				for single_file in list_files:
					with open("data/Event_data/%s"%single_file,"r") as f:
						for line in f:
							di=json.loads(line)
							tuple1=(single_file,len(di))
							list_tuples.append(tuple1)

				tuples_sorted=sorted(list_tuples,key=lambda x: x[1], reverse=True)
				tuples_sorted=tuples_sorted[:int(sys.argv[1])]

				#<copy top5 events--------------------->
				for single_file in tuples_sorted:
					newPath = shutil.copy('data/Event_data/%s'%single_file[0], 'data/top_5_events/%s'%single_file[0])	

				#<----summary creation------------->
				time.sleep(1)
				print("<----summary creation------------->")
				start=time.time()
				sR.start()
				end=time.time()
				total=((end-start)*1.0)/60
				print("summary takes {0} minutes".format(total))
				# list_files_top_5_events=os.listdir(path_top_5_events)
				# for single_file in list_files_top_5_events:
				# 	sR.summary_Generation(single_file)
				#<----top_5_events_images-------------------->
				
				

			else:
				#print("incremental_clus")
				delta=3600
				req_time=last_time+delta
				#cursor = mycol2hour.find(no_cursor_timeout=True)
				cursor = []
				for i in range(5):
					mycol2hour=mydb[i]["test2hour"]
					#print(mycol2hour.count())
					cursor2hour = list(mycol2hour.find(no_cursor_timeout=True))
					cursor.extend(cursor2hour)
				
				list_created_at=[]
				for ele in cursor:
					try:
						del ele['_id']

						datetime_object = datetime.strptime(str(ele["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
						tweet_time = time.mktime(datetime_object.timetuple())
						
						list_created_at.append(tweet_time)

						if tweet_time >=last_time and tweet_time <= req_time:
							incremental_clus(ele)
						elif tweet_time > req_time:
							#print("Done similarity of all tweets")
							pass
					except:
						continue
				#cursor.close()
				list_created_at.sort(reverse=True)
				last_time=list_created_at[0]
				#<--------rename events----------->				
				list_files=os.listdir(path)
				for single_file in list_files:
					with open("data/Event_data/%s"%single_file,"r") as f:
						for line in f:
							single_file_di=json.loads(line)
							if len(single_file_di) == 0:
								os.remove("data/Event_data/%s"%single_file)
				
							else:
								all_tweets=""
								for key,val in single_file_di.items():
									all_tweets=val["text"]+" "+all_tweets
								#<--preprocess all tweets---->
								all_tweets=pre.preprocessing_tweets(all_tweets)

								if not all_tweets:
									os.remove("data/Event_data/%s"%single_file)
					
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

									#print("#################   Event name:   ",event_name)
									os.rename("data/Event_data/%s"%single_file,"data/Event_data/%s.json"%event_name) 
	
				#<--------deleting required files----->

				list_files_top_5_events=os.listdir(path_top_5_events)
				list_files_event_images=os.listdir(path_top_5_events_images)
				list_files_event_summary=os.listdir(path_top_5_events_summary)

				for single_file in list_files_top_5_events:
					os.remove('data/top_5_events/%s'%single_file)

				for single_file in list_files_event_images:
					os.remove('data/top_5_events_images/%s'%single_file)

				for single_file in list_files_event_summary:
					os.remove('data/top_5_events_summary/%s'%single_file)


				#<-----summary generation initializaion---->
				

				list_files=os.listdir(path)
				list_tuples=[]
				for single_file in list_files:
					with open("data/Event_data/%s"%single_file,"r") as f:
						for line in f:
							di=json.loads(line)
							tuple1=(single_file,len(di))
							list_tuples.append(tuple1)

				tuples_sorted=sorted(list_tuples,key=lambda x: x[1], reverse=True)
				tuples_sorted=tuples_sorted[:int(sys.argv[1])]

				#<copy top5 events--------------------->
				for single_file in tuples_sorted:
					newPath = shutil.copy('data/Event_data/%s'%single_file[0], 'data/top_5_events/%s'%single_file[0])	

				#<----summary creation------------->
				time.sleep(1)
				print("<----summary creation------------->")
				start=time.time()
				sR.start()
				end=time.time()
				total=((end-start)*1.0)/60
				print("summary takes {0} minutes".format(total))
				# list_files_top_5_events=os.listdir(path_top_5_events)
				# for single_file in list_files_top_5_events:
				# 	sR.summary_Generation(single_file)
				

				#<----top_5_events_images-------------------->
				

				

				print("Now Performing Operation for Tweet with Images")
				print("<----Tweet With Images Work Going On------------->")
				start=time.time()
				iR.start()
				end=time.time()
				total=((end-start)*1.0)/60
				print("Tweet with iamegs takes {0} minutes".format(total))

		


		else:
			print("Unable to do CLUSTERING......Collection EMPTY :(")

		

		if i == 4:
			sum_2hour =0
			for i in range(5):
				mycol2hour=mydb[i]["test2hour"]
				sum_2hour = sum_2hour + mycol2hour.count()
			
			#if mydb.test2hour.count() > 0:
			if sum_2hour > 0:
				#print("Before deleting:....",mydb.test2hour.count())
				print("Before deleting:....",sum_2hour)
				#remove2hour()
				for i in range(5):
					mycol2hour=mydb[i]["test2hour"]
					mycol2hour.remove({})
				#print("After deleting:....",mydb.test2hour.count())
				sum_2hour_new =0
				for i in range(5):
					mycol2hour=mydb[i]["test2hour"]
					sum_2hour_new = sum_2hour_new + mycol2hour.count()
				print("After deleting:....",sum_2hour_new)
			else:
				print("Collection is EMPTY....... ### UNABLE to DELETE   SORRY   :(")

		if i >= 5:
			sum_2hour =0
			for i in range(5):
				mycol2hour=mydb[i]["test2hour"]
				sum_2hour = sum_2hour + mycol2hour.count()
			
			#if mydb.test2hour.count() > 0:
			if sum_2hour > 0:
				#print("Before deleting:....",mydb.test2hour.count())
				print("Before deleting:....",sum_2hour)
				#remove2hour()
				for i in range(5):
					mycol2hour=mydb[i]["test2hour"]
					mycol2hour.remove({})
				#print("After deleting:....",mydb.test2hour.count())
				sum_2hour_new =0
				for i in range(5):
					mycol2hour=mydb[i]["test2hour"]
					sum_2hour_new = sum_2hour_new + mycol2hour.count()
				print("After deleting:....",sum_2hour_new)
			else:
				print("Collection is EMPTY....... ### UNABLE to DELETE   SORRY.....")


		i=i+1
#def begin():
if __name__ == '__main__':
	removeTweets_after2hrs()
    
