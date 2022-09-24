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
import numpy as np
from operator import itemgetter


# model_10 = load_model('LSTM_BEST_10MIN.h5')
# model_30 = load_model('LSTM_BEST_30MIN.h5')
# model_60 = load_model('LSTM_BEST_60MIN.h5')	

model_10 = load_model('softmax_LSTM_BEST_10MIN.h5')
model_30 = load_model('softmax_LSTM_BEST_30MIN.h5')
model_60 = load_model('softmax_LSTM_BEST_60MIN.h5')

path_10min='data/Event_data_10min'
path='data/Event_data'
paths = 'data/single_keywords.txt'

path_top_5_events='data/top_5_events'
path_top_5_events_images='data/top_5_events_images'
path_top_5_events_summary='data/top_5_events_summary'
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["RealData"]
# mycol_virality=mydb["virality"]
# mycol10min = mydb["test10min"]

myclient = [ pymongo.MongoClient("mongodb://localhost:2017/"),pymongo.MongoClient("mongodb://localhost:2018/"),pymongo.MongoClient("mongodb://localhost:2019/"),pymongo.MongoClient("mongodb://localhost:2020/"),pymongo.MongoClient("mongodb://localhost:2021/") ]

mydb = []

for temp in myclient:
    mydb.append(temp["RealData"])




def first_time_tweet(file) :
	list_created_at=[]
	with open(file) as f:
		data = json.load(f)
		for key in data :
			tweet = data[key]
			date1=tweet['created_at']			
			datetime_object = datetime.strptime(str(tweet["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
			tweet_time = time.mktime(datetime_object.timetuple())
			list_created_at.append(tweet_time)

	list_created_at.sort()
	#print("list_created_at",list_created_at)
	first_time=list_created_at[0]
	return first_time


def virality_predictor():
	my_di={}
	event_cnt=0
	for filename in os.listdir(path_10min):
		event_cnt+=1
		file=path_10min+"/"+filename
		first_time=first_time_tweet(file)			
		now = datetime.utcnow()			
		current_time = time.mktime(now.timetuple())
		diff=current_time-first_time
		print(file)			
		sampling_time=0

		if diff<600:
			sampling_time=10

		elif diff>600 and diff<1800:
			sampling_time=30

		elif diff>1800:
			sampling_time=60


		di={}


		with open(file) as f:
			for line in f:
				data = json.loads(line)
				for key,val in data.items():
					datetime_object = datetime.strptime(str(val["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
					tweet_time = time.mktime(datetime_object.timetuple())
					di['%s'%val['id_virality']] = {'rate':[],'created_at':tweet_time}


		#cursor = mycol10min.find(no_cursor_timeout=True)
		#cursor = mycol_virality.find(no_cursor_timeout=True)
		cursor = []
		for i in range(5):
			mycol10min=mydb[i]["test10min"]
			cursor10min = list(mycol10min.find(no_cursor_timeout=True))
			cursor.extend(cursor10min)

		for ele in cursor:
			try:
				del ele['_id']
				if "retweeted_status" in ele:
					parent_id=ele['retweeted_status']['id_str']
					datetime_object = datetime.strptime(str(ele["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
					retweet_time = time.mktime(datetime_object.timetuple())

					if '%s'%parent_id in di:
						di['%s'%parent_id]['rate'].append(retweet_time)

			except:
				continue

		
		
		final_di={}

		for key in di:
		    rate = di[key]['rate']
		 
		    ls = []
		    for i in rate:
		    	ls.append(int(i))
		    ls.sort()
		    actual = di[key]['created_at']
		    time_list=[]
		    for i in range(0, sampling_time):
		        lower = (i * 60) + 1
		        upper = (i + 1) * 60
		        counter = 0
		        for j in rate:

		            t = (int(j) - int(actual)) + 1
		            if t >= lower and t < upper:
		                counter += 1
		        time_list.append(counter)
		    
		    final_di['%s'%key]=time_list
		

		print("final_di",len(final_di))


		retweet_history=[]
		for i in range(sampling_time):
			sum=0
			for key in final_di:
				sum=sum+final_di[key][i]

			retweet_history.append(sum)
		print("retweet_history",retweet_history)
		


		p=0
		X = []
		X.append(retweet_history)
		x=np.array(X)
		if diff<600:
			# pred=model_10.predict_classes(x)
			# p=pred[0][0]
			pred=model_10.predict(x)
			index_=np.argmax(pred)
			max_=str(np.max(pred))
		elif diff>600 and diff<1800:
			pred=model_30.predict(x)
			index_=np.argmax(pred)
			max_=str(np.max(pred))
		elif diff>1800:
			print("I am going to predict in 60 min")
			pred=model_60.predict(x)
			index_=np.argmax(pred)
			max_=str(np.max(pred))

		
		print(index_)
		if index_==1:

	                sum=0
	               
	                for k in range(len(retweet_history)):
	                    sum=sum+retweet_history[k]
	               
	                event_name=file.split(".")
	                event_name=event_name[0].split("/")
	                event_name=event_name[2]
	         
	                retweet_counter=sum

	                tweet1=''
	                event_time=''
	                prediction_time=''
	                locations=[]
	                media_url=[]

	                list_tweets = []
	                with open(file, "r") as f:
	                    for line in f:
	                        event = json.loads(line)
	                        for key, val in event.items():
	                            if len(locations)<=5:
	                                locations.append(val['user_location'])

	                            if val['image_url']!='none':
	                                if len(media_url)<3:
	                                    media_url.append(val['image_url'])



	                            list_tweets.append(val)




	                # list_tweets = sorted(list_tweets, key=itemgetter('created_at'))

	                # tweet1=list_tweets[0]['text']
	                # event_time=list_tweets[0]['created_at']
	                # prediction_time=datetime.fromtimestamp(current_time).strftime("%a %b %d %H:%M:%S +0000 %Y")
	                # #print(event_name)
	                # #print(tweet1)
	                # #print(locations)
	                # #print(media_url)
	                # #print(event_time)
	                # #print(datetime.fromtimestamp(prediction_time).strftime("%A, %B %d, %Y %I:%M:%S"))

	                
	                # my_di['%s'%event_cnt] = {'event_name': event_name, 'retweet_count': retweet_counter,'tweet1':tweet1,'start_time':event_time,'prediction_time':prediction_time,'prediction_score':max_,'top_5_locations':locations,'images':media_url}
	                list_tweets = sorted(list_tweets, key=itemgetter('retweet_count'),reverse=True)
	                list_tweets1 = sorted(list_tweets, key=itemgetter('created_at'))
	                event_time=list_tweets1[0]['created_at']
	                tweet_id=list_tweets[0]['id_str']
	                tweet_rt=list_tweets[0]['retweet_count']
	                tweet1=list_tweets[0]['text']
	                tweet_time=list_tweets[0]['created_at']
	                prediction_time=datetime.fromtimestamp(current_time).strftime("%a %b %d %H:%M:%S +0000 %Y")
	                #print(event_name)
	                #print(tweet1)
	                #print(locations)
	                #print(media_url)
	                #print(event_time)
	                #print(datetime.fromtimestamp(prediction_time).strftime("%A, %B %d, %Y %I:%M:%S"))

	                
	                my_di['%s'%event_cnt] = {'event_name': event_name, 'event_retweet_count': retweet_counter,'start_time':event_time,'tweet_id':tweet_id,'tweet1':tweet1,'tweet_time':tweet_time,'prediction_time':prediction_time,'prediction_score':max_,'top_5_locations':locations,'images':media_url}
	           

	if (len (my_di) > 0):
		with open('data/potential_viral/viral_events.json','w') as file:
			json.dump(my_di, file)
	if (len (my_di) > 0):
		with open('data/statistics_viral/stats_viral_events.json','a') as file:
			json.dump(my_di, file)
	              
				
