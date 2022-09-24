#import threading
import queue
import tweepy
from tweepy.api import API
from datetime import datetime
import time
import pymongo
import json
import clustering_RealTime_nrv as CR
#import clustering_RealTime_10min as CR10min
import os
import cosine_sim as cosine_sim
#import cosine_sim10min as cosine_sim10min
import preprocessing as pre
import preprocessing_10min as pre10min
from collections import Counter
import summary_RealTime_nrv as sR
import tweet_with_images_RealTime_nrv as iR
import shutil


myclient = [ pymongo.MongoClient("mongodb://localhost:2017/"),pymongo.MongoClient("mongodb://localhost:2018/"),pymongo.MongoClient("mongodb://localhost:2019/"),pymongo.MongoClient("mongodb://localhost:2020/"),pymongo.MongoClient("mongodb://localhost:2021/") ]

mydb = []

for temp in myclient:
    mydb.append(temp["RealData"])


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["RealData"]

# mycol_nrv = mydb["nrv"]
#path_10min='data/Event_data_10min'
path='data/non_radical_violence_events/Event_data_nrv'


path_top_5_events='data/non_radical_violence_events/top_5_events'
path_top_5_events_images='data/non_radical_violence_events/top_5_events_images'
path_top_5_events_summary='data/non_radical_violence_events/top_5_events_summary'

def remove2hour():
	print("i am under remove...................")
	#print("length of documents till now:  ",mydb.nrv.count())
	sum_nrv =0
	for i in range(5):
		mycol_nrv=mydb[i]["nrv"]
		sum_nrv = sum_nrv + mycol_nrv.count()	
	print("length of documents till now:  ",sum_nrv)

	#cursor = mycol_nrv.find(no_cursor_timeout=True)
	cursor = []
	for i in range(5):
		mycol_nrv=mydb[i]["nrv"]
		cursor_nrv = list(mycol_nrv.find(no_cursor_timeout=True))
		cursor.extend(cursor_nrv)

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
				#result_del = mydb.nrv.delete_one(ele)
				for i in range(5):
					mycol_nrv=mydb[i]["nrv"]
					result_del=mycol_rv.delete_one(ele)
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
			with open("data/non_radical_violence_events/Event_data_nrv/%s"%single_file,"r") as f:
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
					with open("data/non_radical_violence_events/Event_data_nrv/%s"%key,"r") as f1:
						for line in f1:
							event_file=json.loads(line)
							event_file[tweet["id_str"]]={"id_str":tweet["id_str"],"latitude":lat_long[0],"longitude":lat_long[1],"ename":event_name,"created_at":tweet["created_at"],"user_location":location,"text":tweet["text"],"main_event":0,"user_name":tweet["user"]["name"],"follower_count":tweet["user"]["followers_count"],"retweet_count":tweet["retweet_count"],"image_url":url}
					
					#print(event_file)
					with open("data/non_radical_violence_events/Event_data_nrv/%s"%key,"w") as f2:
						json.dump(event_file,f2)
		elif max < threshold:
			#print("new clus")
			event_file_new_clus={}
			event_name="new_clus"+str(ijk)
			event_file_new_clus[tweet["id_str"]]={"id_str":tweet["id_str"],"latitude":lat_long[0],"longitude":lat_long[1],"ename":event_name,"created_at":tweet["created_at"],"user_location":location,"text":tweet["text"],"main_event":0,"user_name":tweet["user"]["name"],"follower_count":tweet["user"]["followers_count"],"retweet_count":tweet["retweet_count"],"image_url":url}
			#print(event_file_new_clus)
			with open("data/non_radical_violence_events/Event_data_nrv/new_clus{0}.json".format(ijk),"w") as f3:
				json.dump(event_file_new_clus,f3)
			ijk=ijk+1


def removeTweets_after2hrs():
	#global p
	i=1
	while True:
		print("i m gonna sleep..................")
		time.sleep(600)
		sum_nrv_initial =0
		for i in range(5):
			mycol_nrv=mydb[i]["nrv"]
			sum_nrv_initial = sum_nrv_initial + mycol_nrv.count()

		#if mydb.nrv.count() > 0:
		if sum_nrv_initial > 0:
			if os.listdir(path) == []:
			
				last_time=CR.clus()
				print("Clustering is done..now we wil delete test_nrv.json")
				if os.path.exists("test_nrv.json"):
					os.remove("test_nrv.json")
				else:
					print("The file does not exist") 
				#<--------deleting required files----->

				list_files_top_5_events=os.listdir(path_top_5_events)
				list_files_event_images=os.listdir(path_top_5_events_images)
				list_files_event_summary=os.listdir(path_top_5_events_summary)

				for single_file in list_files_top_5_events:
					os.remove('data/non_radical_violence_events/top_5_events/%s'%single_file)

				for single_file in list_files_event_images:
					os.remove('data/non_radical_violence_events/top_5_events_images/%s'%single_file)

				for single_file in list_files_event_summary:
					os.remove('data/non_radical_violence_events/top_5_events_summary/%s'%single_file)

				#<-----summary generation initializaion---->
				

				list_files=os.listdir(path)
				list_tuples=[]
				for single_file in list_files:
					with open("data/non_radical_violence_events/Event_data_nrv/%s"%single_file,"r") as f:
						for line in f:
							di=json.loads(line)
							tuple1=(single_file,len(di))
							list_tuples.append(tuple1)

				tuples_sorted=sorted(list_tuples,key=lambda x: x[1], reverse=True)
				tuples_sorted=tuples_sorted[:5]

				#<copy top5 events--------------------->
				for single_file in tuples_sorted:
					newPath = shutil.copy('data/non_radical_violence_events/Event_data_nrv/%s'%single_file[0], 'data/non_radical_violence_events/top_5_events/%s'%single_file[0])	

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
				delta=600
				req_time=last_time+delta
				#cursor = mycol_nrv.find(no_cursor_timeout=True)
				cursor = []
				for i in range(5):
					mycol_nrv=mydb[i]["nrv"]
					cursor_nrv = list(mycol_nrv.find(no_cursor_timeout=True))
					cursor.extend(cursor_nrv)
				
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
					with open("data/non_radical_violence_events/Event_data_nrv/%s"%single_file,"r") as f:
						for line in f:
							single_file_di=json.loads(line)
							if len(single_file_di) == 0:
								os.remove("data/non_radical_violence_events/Event_data_nrv/%s"%single_file)
				
							else:
								all_tweets=""
								for key,val in single_file_di.items():
									all_tweets=val["text"]+" "+all_tweets
								#<--preprocess all tweets---->
								all_tweets=pre.preprocessing_tweets(all_tweets)

								if not all_tweets:
									os.remove("data/non_radical_violence_events/Event_data_nrv/%s"%single_file)
					
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
									os.rename("data/non_radical_violence_events/Event_data_nrv/%s"%single_file,"data/non_radical_violence_events/Event_data_nrv/%s.json"%event_name) 
	
				#<--------deleting required files----->

				list_files_top_5_events=os.listdir(path_top_5_events)
				list_files_event_images=os.listdir(path_top_5_events_images)
				list_files_event_summary=os.listdir(path_top_5_events_summary)

				for single_file in list_files_top_5_events:
					os.remove('data/non_radical_violence_events/top_5_events/%s'%single_file)

				for single_file in list_files_event_images:
					os.remove('data/non_radical_violence_events/top_5_events_images/%s'%single_file)

				for single_file in list_files_event_summary:
					os.remove('data/non_radical_violence_events/top_5_events_summary/%s'%single_file)


				#<-----summary generation initializaion---->
				

				list_files=os.listdir(path)
				list_tuples=[]
				for single_file in list_files:
					with open("data/non_radical_violence_events/Event_data_nrv/%s"%single_file,"r") as f:
						for line in f:
							di=json.loads(line)
							tuple1=(single_file,len(di))
							list_tuples.append(tuple1)

				tuples_sorted=sorted(list_tuples,key=lambda x: x[1], reverse=True)
				tuples_sorted=tuples_sorted[:5]

				#<copy top5 events--------------------->
				for single_file in tuples_sorted:
					newPath = shutil.copy('data/non_radical_violence_events/Event_data_nrv/%s'%single_file[0], 'data/non_radical_violence_events/top_5_events/%s'%single_file[0])	

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
			
			sum_nrv =0
			for i in range(5):
				mycol_nrv=mydb[i]["nrv"]
				sum_nrv = sum_nrv + mycol_nrv.count()
			#if mydb.rv.count() > 0:
			if sum_nrv > 0:
				#print("Before deleting:....",mydb.rv.count())
				print("Before deleting:....",sum_nrv)
				#remove2hour()
				for i in range(5):
					mycol_nrv=mydb[i]["nrv"]
					mycol_nrv.remove({})
				#print("After deleting:....",mydb.rv.count())
				sum_nrv_new =0
				for i in range(5):
					mycol_nrv=mydb[i]["nrv"]
					sum_nrv_new = sum_nrv_new + mycol_nrv.count()
				print("After deleting:....",sum_nrv_new)
			else:
				print("Collection is EMPTY....... ### UNABLE to DELETE   SORRY   :(")

		if i >= 5:
			sum_nrv =0
			for i in range(5):
				mycol_nrv=mydb[i]["nrv"]
				sum_nrv = sum_nrv + mycol_nrv.count()
			#if mydb.rv.count() > 0:
			if sum_nrv > 0:
				#print("Before deleting:....",mydb.rv.count())
				print("Before deleting:....",sum_nrv)
				#remove2hour()
				for i in range(5):
					mycol_nrv=mydb[i]["nrv"]
					mycol_nrv.remove({})
				#print("After deleting:....",mydb.rv.count())
				sum_nrv_new =0
				for i in range(5):
					mycol_nrv=mydb[i]["nrv"]
					sum_nrv_new = sum_nrv_new + mycol_nrv.count()
				print("After deleting:....",sum_nrv_new)
			else:
				print("Collection is EMPTY....... ### UNABLE to DELETE   SORRY.....")


		i=i+1

#def begin():
if __name__ == '__main__':
	removeTweets_after2hrs()
    