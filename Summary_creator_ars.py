import pymongo
import pandas as pd
import json
from datetime import datetime
import time
import os
import numpy as np
from urlextract import URLExtract

myclient = [ pymongo.MongoClient("mongodb://localhost:2017/"),pymongo.MongoClient("mongodb://localhost:2018/"),pymongo.MongoClient("mongodb://localhost:2019/"),pymongo.MongoClient("mongodb://localhost:2020/"),pymongo.MongoClient("mongodb://localhost:2021/") ]

mydb = []

for temp in myclient:
    mydb.append(temp["RealData"])

start  = "Wed Mar 03 09:00:00 +0000 2020"
end  = "Wed Mar 03 09:30:00 +0000 2020"
day = "Wed"
month = "Mar"
date = "03"

file1 = open("thirty_min_window.txt","w")
viral_dict, non_viral_dict = {} , {}

extractor = URLExtract()

dictionary_temporary={}
def create_dict(df_ret,df_original):
	dict_virality={}

	for i, row in df_original.iterrows():
		id_org=row["tweetId"]
		
		#di={};
		dtemp= df_ret[( (df_ret["originatorId"]==id_org) )]


		
		if dtemp.empty != True:
			dict_virality["%s"%id_org]={}
			all_time= list(dtemp["created_at"])
			followers_L = list(dtemp["followers_count"])
			
			rate = []	
			for creationTime_ in all_time:
				datetime_object = datetime.strptime(str(creationTime_), '%a %b %d %H:%M:%S +0000 %Y')
				creationTime_sec = time.mktime(datetime_object.timetuple())
				rate.append(creationTime_sec)
				

			dict_virality["%s"%id_org]["rate"]=rate#dict_virality[id_org]["rate"]=rate
			originalTime=row["created_at"]
			datetime_object = datetime.strptime(str(originalTime), '%a %b %d %H:%M:%S +0000 %Y')
			originalTime_sec = time.mktime(datetime_object.timetuple())
			#dict_virality["%s"%id_org]["created"]= originalTime_sec
			dict_virality["%s"%id_org]["created"] = row["created_at"]
			dict_virality["%s"%id_org]["text"] = row["text"]
			dict_virality["%s"%id_org]["location"] = row["location"]
			dict_virality["%s"%id_org]["followers_count"] = row["followers_count"]
			dict_virality["%s"%id_org]["images"] = row["images"] 
			dict_virality["%s"%id_org]["username"] = row["username"] 
			dict_virality["%s"%id_org]["followers_count_list"] = followers_L

			dict_virality["%s"%id_org]["urls"] = ""
			urls = extractor.find_urls(row["text"])
			if len(urls)>0:
				if urls[0][0] == 'h':
					dict_virality["%s"%id_org]["urls"] =  urls[0]
			print(dict_virality["%s"%id_org]["urls"])

	for key,val in dict_virality.items():
		dictionary_temporary[key] = {"id_str":key,"text":val["text"],"created_at":val["created"],"user_name":val["username"],"user_location":val["location"],"follower_count":val["followers_count"],"retweet_count":len(val["rate"]),"image_url":val["images"],"urls":val["urls"]}
		# dictionary_temporary[key] = {"id_str":key,"text":val["text"],"created_at":val["created"],"user_name":val["username"],"user_location":val["location"],"follower_count":val["followers_count"],"retweet_count":len(val["rate"]),"image_url":val["images"]}

	with open("imp/summary_all.json","w") as f:
		json.dump(dictionary_temporary,f)

def prog():

	list_id_org, list_time_org, list_text_org, list_location_org, list_followers_count_org = [],[], [], [], []
	list_id_ret, list_id_org_ret, list_time_ret, list_followers_count, list_text_ret, list_location_ret = [],[],[],[], [], []

	list_images_ret, list_images_org = [], []
	list_user_name_org, list_user_name_ret = [], []

	cursor = []
	for i in range(5):
		mycol_all_ve=mydb[i]["ve"]
		#cursor  = mycol_all_ve.find({})
		cursor_ve = list(mycol_all_ve.find(no_cursor_timeout=True))
		cursor.extend(cursor_ve)


	# for i in range(5):
	# 	mycol_all_nve=mydb[i]["nve"]
	# 	#cursor  = mycol_all_ve.find({})
	# 	cursor_nve = list(mycol_all_nve.find(no_cursor_timeout=True))
	# 	cursor.extend(cursor_nve)

	for i in range(5):
		mycol_all_rv=mydb[i]["rv"]
		#cursor  = mycol_all_ve.find({})
		cursor_rv = list(mycol_all_rv.find(no_cursor_timeout=True))
		cursor.extend(cursor_rv)

	for ele in cursor:
		
		if 'retweeted_status' in ele:
			list_id_ret.append(ele['id_str'])
			list_id_org_ret.append(str(ele['retweeted_status']['id']))
			list_time_ret.append(ele['created_at'])
			list_followers_count.append(ele["user"]["followers_count"])
			list_text_ret.append(ele['text'])
			list_location_ret.append(ele['user']['location'])
			list_user_name_ret.append(ele['user']['screen_name'])

			if 'media' in ele['entities']:
				media=(ele['entities']['media'])
				media=media[0]
				image_url=media['media_url']

			else:
				image_url="none"
			list_images_ret.append(image_url)




		else:
			list_id_org.append(ele['id_str'])
			list_time_org.append(ele['created_at'])
			list_text_org.append(ele['text'])
			list_location_org.append(ele['user']['location'])
			list_followers_count_org.append(ele["user"]["followers_count"])
			list_user_name_org.append(ele['user']['screen_name'])
			if 'media' in ele['entities']:
				media=(ele['entities']['media'])
				media=media[0]
				image_url=media['media_url']

			else:
				image_url="none"
			list_images_org.append(image_url)

	
	

	df_org=pd.DataFrame(columns=["tweetId", "created_at"])
	df_org["tweetId"] = list_id_org
	df_org["created_at"] = list_time_org
	df_org["text"] = list_text_org
	df_org["location"] = list_location_org
	df_org["followers_count"] = list_followers_count_org
	df_org["images"] = list_images_org
	df_org["username"] = list_user_name_org
	# df_org.drop_duplicates(subset="tweetId", keep="last", inplace= True)
	# df_org=df_org.reset_index(drop=True)
	#df_org.to_csv("Data/original_tweets.csv", index = False)	

	df=pd.DataFrame(columns=["retweetID","originatorId", "created_at", "followers_count"])
	df["retweetID"] = list_id_ret
	df["originatorId"] = list_id_org_ret
	df["created_at"] = list_time_ret
	df["followers_count"] = list_followers_count
	df["text"] = list_text_ret
	df["location"] = list_location_ret
	df["images"] = list_images_ret
	df["username"] = list_user_name_ret
	# df.drop_duplicates(subset="retweetID", keep="last", inplace= True)
	# df=df.reset_index(drop=True)
	#df.to_csv("Data/retweetd_tweets.csv", index = False)

	create_dict(df,df_org)
prog()
