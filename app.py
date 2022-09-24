'''
please check size of jsonify content 
if content is empty do not replace current summary
if content is not empty then replace summary to current event

'''
from operator import *
import os
import glob
import json
from flask import Flask, render_template, jsonify, request
import json
import time
import os
import shutil
from datetime import datetime
app = Flask(__name__)
from lexrank import STOPWORDS,LexRank
from path import Path
import json
import pandas as pd
#import json_csv as js
import base64
import matplotlib.pyplot as plt
import io
import numpy as np
from nltk.corpus import stopwords
import re
import tweepy
from joblib import dump, load
from tweepy.api import API

import pymongo

myclient = [ pymongo.MongoClient("mongodb://localhost:2017/"),pymongo.MongoClient("mongodb://localhost:2018/"),pymongo.MongoClient("mongodb://localhost:2019/"),pymongo.MongoClient("mongodb://localhost:2020/"),pymongo.MongoClient("mongodb://localhost:2021/") ]

mydb = []

for temp in myclient:
    mydb.append(temp["RealData"])


# API_KEY="msH9Y1pg3zQOUjATGpkrWcALP"
# API_SECRET="LTdgEns9v07a7bvv6DYNMwHO8O9GjnEXMNhNunjcVmSQ11UkHi"
# ACCESS_TOKEN="917327613009346561-J0NzqeUwrM6CSyO5PFGPJXuxTg9tiE0"
# ACCESS_TOKEN_SECRET="NcySnBrdMtjbhZ7EMeKAZY84n88FMZxzjyFKATNxQpJh3"

API_KEY = '4aaZYPDMP7xhhBFK0NKt61022'
API_SECRET = 'ubcWRJ8guHFByAikjsf06wtzObLCkKv21U4RJZlwpOyXPxAuvT'
ACCESS_TOKEN = '917327613009346561-hoaFNO7SHmSQvsICN9hDCvPobLObGWl'
ACCESS_TOKEN_SECRET = 'PjKYTDs0SVT2CleePMg9NLNsAAixivmafamqf17Mb3YZi'

key = tweepy.OAuthHandler(API_KEY, API_SECRET)
key.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["RealData"]

# mycol10min = mydb["test10min"]
# mycol2hour= mydb["test2hour"]

# mycol_ve = mydb["ve"]
# mycol_nve = mydb["nve"]
# mycol_rv = mydb["rv"]
# mycol_nrv = mydb["nrv"]
# mycol_virality_keyword = mydb["virality_keyword"]
# mycol_total_keyword=mydb["all_data_keyword"]


def make_lexrank(df):
	
	
	print("i am here")
	print(df.shape)
	# remove existing active window summary file
	d = "data/active_window_summary"
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	'''
	list_ids,list_text=[],[]
	with open('data/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
			
	'''
	
	
	
	documents = []
	documents_dir = Path('bbc/politics')
	for file_path in documents_dir.files('*.txt'):
		with file_path.open(mode='rt', encoding='utf-8') as fp:
			documents.append(fp.readlines())
	
	lxr = LexRank(documents, stopwords=STOPWORDS)
	#df=js.make_csv("all_json.json")
	#df=df[:60000]
	list_text,list_ids=[],[]
	for i,row in df.iterrows():
		list_text.append(row["full_text"])
		list_ids.append(row["id_str"])
	scores_cont = lxr.rank_sentences(list_text,threshold=None,fast_power_method=False,)
	tuples=list(zip(list_ids,scores_cont))
	tuples_sorted=sorted(tuples,key=lambda x: x[1], reverse=True)
	
	list_summary_top=[]
	
	if len(tuples_sorted)>10:
		for i in range(0,10):
			list_summary_top.append(tuples_sorted[i][0])
			
	else:	
		for i in range(0,len(tuples_sorted)):
			list_summary_top.append(tuples_sorted[i][0])

			
	df_summary=df[df["id_str"].isin(list_summary_top)]
	#print(list_ids)
	#print(list_summary_top)
	#print(type(list_ids[0]))
	#print(type(list_summary_top[0]))
	#print(df_summary.shape)
	#print(df_summary)

	dictionary_temporary={}
	for i,row in df_summary.iterrows():
		dictionary_temporary[row["id_str"]]={"id_str":row["id_str"],"text":row["full_text"],"created_at":row["created_at"],"user_name":row["user_name"],"user_location":row["user_location"],"follower_count":row["follower_count"],"retweet_count":row["retweet_count"]}

	with open("data/active_window_summary/summary.json","a") as f:
		json.dump(dictionary_temporary,f)


def make_lexrank1(df):
	
	
	print("i am here")
	print(df.shape)
	# remove existing active window summary file
	d = "data/active_window_summary"
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	'''
	list_ids,list_text=[],[]
	with open('data/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
			
	'''
	
	
	
	documents = []
	documents_dir = Path('bbc/politics')
	for file_path in documents_dir.files('*.txt'):
		with file_path.open(mode='rt', encoding='utf-8') as fp:
			documents.append(fp.readlines())

	lxr = LexRank(documents, stopwords=STOPWORDS['en'])
	#df=js.make_csv("all_json.json")
	#df=df[:60000]
	list_text,list_ids=[],[]
	for i,row in df.iterrows():
		list_text.append(row["full_text"])
		list_ids.append(row["id_str"])
	scores_cont = lxr.rank_sentences(list_text,threshold=None,fast_power_method=False,)
	tuples=list(zip(list_ids,scores_cont))
	tuples_sorted=sorted(tuples,key=lambda x: x[1], reverse=True)
	
	
	list_summary_top=[]
	
	if len(tuples_sorted)>10:
		for i in range(0,10):
			list_summary_top.append(tuples_sorted[i][0])
			
	else:	
		for i in range(0,len(tuples_sorted)):
			list_summary_top.append(tuples_sorted[i][0])
			
	df_summary=df[df["id_str"].isin(list_summary_top)]
	#print(list_ids)
	#print(list_summary_top)
	#print(type(list_ids[0]))
	#print(type(list_summary_top[0]))
	#print(df_summary.shape)
	#print(df_summary)

	dictionary_temporary={}
	for i,row in df_summary.iterrows():
		dictionary_temporary[row["id_str"]]={"id_str":row["id_str"],"text":row["full_text"],"created_at":row["created_at"],"user_name":row["user_name"],"user_location":row["user_location"],"follower_count":row["follower_count"],"retweet_count":row["retweet_count"],"image":row["image_url"]}

	with open("data/active_window_summary/summary.json","a") as f:
		json.dump(dictionary_temporary,f)	




#==================================================================================
# generate summary of all tweets
#==================================================================================

def make_lexrank_summary_all_tweets(df):
	print(df.shape)
	# remove existing all tweets summary file
	#d = "imp/active_window_summary"
	if os.path.exists("imp/summary_all.json"):
		os.remove("imp/summary_all.json")
	
	
	documents = []
	documents_dir = Path('bbc/politics')
	for file_path in documents_dir.files('*.txt'):
		with file_path.open(mode='rt', encoding='utf-8') as fp:
			documents.append(fp.readlines())

	lxr = LexRank(documents, stopwords=STOPWORDS['en'])
	#df=js.make_csv("all_json.json")
	#df=df[:60000]
	list_text,list_ids=[],[]
	for i,row in df.iterrows():
		list_text.append(row["full_text"])
		list_ids.append(row["id_str"])
	scores_cont = lxr.rank_sentences(list_text,threshold=None,fast_power_method=False,)
	tuples=list(zip(list_ids,scores_cont))
	tuples_sorted=sorted(tuples,key=lambda x: x[1], reverse=True)
	
	
	list_summary_top=[]
	
	if len(tuples_sorted)>10:
		for i in range(0,10):
			list_summary_top.append(tuples_sorted[i][0])
			
	else:	
		for i in range(0,len(tuples_sorted)):
			list_summary_top.append(tuples_sorted[i][0])
			
	df_summary=df[df["id_str"].isin(list_summary_top)]
	#print(list_ids)
	#print(list_summary_top)
	#print(type(list_ids[0]))
	#print(type(list_summary_top[0]))
	#print(df_summary.shape)
	#print(df_summary)

	dictionary_temporary={}
	for i,row in df_summary.iterrows():
		dictionary_temporary[row["id_str"]]={"id_str":row["id_str"],"text":row["full_text"],"created_at":row["created_at"],"user_name":row["user_name"],"user_location":row["user_location"],"follower_count":row["follower_count"],"retweet_count":row["retweet_count"],"image_url":row["image_url"]}

	with open("imp/summary_all.json","a") as f:
		json.dump(dictionary_temporary,f)	



#============================================================================================================================
























@app.route('/')
def index():
	return render_template("exp_ra.html")


	
# summary of current active content
@app.route('/active_window_summary', methods=['GET', 'POST'])
def active_window_summary():
	di={}
	with open('data/active_window_summary/summary.json','r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
					tdict={}
					tdict["tweet_id"]=val["id_str"]
					tdict["text"]=val["text"]
					tdict["created_at"]=val["created_at"]
					tdict["location"]=val["user_location"]
					tdict["user_name"]=val["user_name"]
					tdict["retweet_count"]=val["retweet_count"]
					tdict["followers_count"]=val["follower_count"]
						
					di[key]=tdict

	return jsonify(di)	
	

	
@app.route('/top_5_events', methods=['GET', 'POST'])
def top_5_events():

	file_dict={}
	print(os.path)
	tweetPath = os.path.join("data/top_5_events_analysis")
	tweetFiles = {"time01": os.path.join(tweetPath, "*.json")}
	index=1
	for (key, path) in tweetFiles.items():
		for filePath in glob.glob(path):
			#print("filePAth",filePath)
			head,tail=os.path.split(filePath)
			filepath = tail.split(".")
			#filepath = filepath[0].split("_")
			#index=filepath[0].split("event")[1]	
			print("ind",index)		
			filepath = filepath[0]
			print("filepath",filepath)
			file_dict[index]=filepath
			index=index+1

	file_dict1=dict(sorted(file_dict.items()))			
	print("dict:",file_dict1)
	
	
	return jsonify(file_dict1)
	
	
@app.route('/event', methods=['GET', 'POST'])
def event():


	d = "data/top_5_events_analysis"
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	
	'''
	d_image= "data/top_5_events_images_analysis"
	for path in os.listdir(d_image):
		full_path = os.path.join(d_image, path)
		if os.path.isfile(full_path):
			os.remove(full_path)

	d_summary= "data/top_5_events_summary_analysis"
	for path in os.listdir(d_summary):
		full_path = os.path.join(d_summary, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	'''

	time.sleep(1)
	src_files = os.listdir("data/top_5_events")
	for file_name in src_files:
		full_file_name = os.path.join("data/top_5_events", file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, "data/top_5_events_analysis")
	
	
	'''
	src_files = os.listdir("data/top_5_events_images")
	for file_name in src_files:
		full_file_name = os.path.join("data/top_5_events_images", file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, "data/top_5_events_images_analysis")

	src_files = os.listdir("data/top_5_events_summary")
	for file_name in src_files:
		full_file_name = os.path.join("data/top_5_events_summary", file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, "data/top_5_events_summary_analysis")
	'''				

	with open('data/events.json', 'r') as file:
		event = json.load(file)
	return jsonify(event)

	
	
# plot all events on the map
	
@app.route('/top_5_plot', methods=['GET', 'POST'])
def top_5_plot():
	di={}
	
	event_name = request.form['data']
	no = request.form['count']
	print("event_name,no",event_name,no)
	with open('data/top_5_events_analysis/%s.json'%(event_name), 'r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
						continue
	
	return jsonify(di)	
	

# call to get event of each individual events
@app.route('/events_information', methods=['GET', 'POST'])
def events_information():
	current_event_name = request.form['data']
	no = request.form['count']
	di={}
	
	with open('data/top_5_events_analysis/%s.json'%(current_event_name), 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
					continue
	
	return jsonify(di)	

	

# call to provide tweets with images in each event	
	
@app.route('/event_images', methods=['GET', 'POST'])
def event_images():
	current_event_name = request.form['data']
	no = request.form['count']
	di={}
	if os.path.exists('data/top_5_events_images/%s.json'%(current_event_name)):
		with open('data/top_5_events_images/%s.json'%(current_event_name), 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
						tdict={}
						tdict["tweet_id"]=val["tweet_id"]
						tdict["text"]=val["text"]
						tdict["image_url"]=val["image_url"]
						tdict["location"]=val["location"]
						tdict["class"]=val["class"]
						di[key]=tdict
	
		return jsonify(di)	
	else:
		return jsonify(di)	
	
	
	

# call to get result for searcing with keyword in event	
@app.route('/event_keyword_search_url', methods=['GET', 'POST'])
def event_keyword_search_url():
	current_event_name = request.form['data']
	search_keyword = request.form['keyword_entered']
	class_type = request.form['class_type']
	no=request.form['count']
	di={}
	dataframe_dict=[]
	
	if class_type=='all_class':

		with open('data/top_5_events_analysis/%s.json'%(current_event_name), 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						tweet=val["text"]
						tweet=tweet.lower()
						if search_keyword in tweet:
							dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
							
							di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
					except:
						continue

	if class_type=='violence_extremism':

		with open('data/violence_extremism_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						tweet=val["text"]
						tweet=tweet.lower()
						if search_keyword in tweet:
							dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})

							di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
						
					except:
						continue


	if class_type=='non_violence_extremism':

		with open('data/non_violence_extremism_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						tweet=val["text"]
						tweet=tweet.lower()
						if search_keyword in tweet:
							di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
							dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
					except:
						continue
		
		
		
	if class_type=='radical_violence':

		with open('data/radical_violence_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						tweet=val["text"]
						tweet=tweet.lower()
						if search_keyword in tweet:
							di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
							dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
					except:
						continue
		
		
		
	if class_type=='non_radical_violence':

		with open('data/non_radical_violence_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						tweet=val["text"]
						tweet=tweet.lower()
						if search_keyword in tweet:
							di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
							dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
					except:
						continue
			
	
	if len(di)>0:
			df=pd.DataFrame(dataframe_dict)
			make_lexrank(df)
		
	return jsonify(di)
	
# call to get result for searcing with time in event		
@app.route('/event_time_search_url', methods=['GET', 'POST'])
def event_time_search_url():
	current_event_name = request.form['data']
	start_time = request.form['time1']
	end_time = request.form['time2']
	class_type = request.form['class_type']
	no=request.form['count']
	di={}
	dataframe_dict=[]
	if class_type=='all_class':
		with open('data/top_5_events_analysis/%s.json'%(current_event_name), 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						t1=val["created_at"]
						main_event=	val["main_event"]
						if main_event==0:
							datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
							x = time.mktime(datetime_object.timetuple())
							if int(x)>=int(start_time) and int(x)<=int(end_time):
								dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})

								di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
					except:
						continue
		
	if class_type=='violence_extremism':
		with open('data/violence_extremism_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						t1=val["created_at"]
						main_event=	val["main_event"]
						if main_event==0:
							datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
							x = time.mktime(datetime_object.timetuple())
							if int(x)>=int(start_time) and int(x)<=int(end_time):
								di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
								dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})

					except:
						continue
	
	if class_type=='non_violence_extremism':
		with open('data/non_violence_extremism_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						t1=val["created_at"]
						main_event=	val["main_event"]
						if main_event==0:
							datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
							x = time.mktime(datetime_object.timetuple())
							if int(x)>=int(start_time) and int(x)<=int(end_time):
								di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
								dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
					except:
						continue
	
	if class_type=='radical_violence':
		with open('data/radical_violence_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						t1=val["created_at"]
						main_event=	val["main_event"]
						if main_event==0:
							datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
							x = time.mktime(datetime_object.timetuple())
							if int(x)>=int(start_time) and int(x)<=int(end_time):
								di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
								dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
					except:
						continue
	
	if class_type=='non_radical_violence':
		with open('data/non_radical_violence_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						t1=val["created_at"]
						main_event=	val["main_event"]
						if main_event==0:
							datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
							x = time.mktime(datetime_object.timetuple())
							if int(x)>=int(start_time) and int(x)<=int(end_time):
								di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
								dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
					except:
						continue
	if len(di)>0:
			df=pd.DataFrame(dataframe_dict)
			make_lexrank(df)	
		
	return jsonify(di)		
		
		
		
# call to get result for searcing with location in event		
@app.route('/event_location_search_url', methods=['GET', 'POST'])
def event_location_search_url():
	current_event_name = request.form['data']
	selected_location = request.form['location']
	no=request.form['count']
	with open("all_states_json/%s.json"%selected_location, 'r') as file:
			location = json.load(file)
	
	class_type = request.form['class_type']
	di={}
	dataframe_dict=[]
	if class_type=='all_class':
		with open('data/top_5_events_analysis/%s.json'%(current_event_name), 'r') as f:
			for line in f:
				z=json.loads(line)
				
				for key,val in z.items():
					try:
						loc=val["user_location"]
						loc=loc.lower()
						main_event=val["main_event"]
						for key1 in location:
							if key1 in loc:
								if main_event==0:
									di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
									dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
									break
					except:
						continue
	
	if class_type=='violence_extremism':
		
		with open('data/violence_extremism_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				
				for key,val in z.items():
					try:
						loc=val["user_location"]
						loc=loc.lower()
						main_event=val["main_event"]
						for key1 in location:
							if key1 in loc:
								if main_event==0:
									di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
									dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
									break
			
					except:
						continue
	if class_type=='non_violence_extremism':
		with open('data/non_violence_extremism_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						loc=val["user_location"]
						loc=loc.lower()
						main_event=val["main_event"]
						for key1 in location:
							if key1 in loc:
								if main_event==0:
									di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
									dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
									break
				
					except:
						continue
	if class_type=='radical_violence':
		with open('data/radical_violence_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						loc=val["user_location"]
						loc=loc.lower()
						main_event=val["main_event"]
						for key1 in location:
							if key1 in loc:
								if main_event==0:
									di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
									dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
									break
					except:
						continue
	
	if class_type=='non_radical_violence':
		with open('data/non_radical_violence_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
			for line in f:
				z=json.loads(line)
				for key,val in z.items():
					try:
						loc=val["user_location"]
						loc=loc.lower()
						main_event=val["main_event"]
						for key1 in location:
							if key1 in loc:
								if main_event==0:
									di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
									dataframe_dict.append({"id_str":val["id_str"],"full_text":val["text"],"created_at":val["created_at"],"user_name":val["user_name"],"user_location":val["user_location"],"follower_count":val["follower_count"],"retweet_count":val["retweet_count"]})
									break
					except:
						continue
	print(len(di))
	print(len(dataframe_dict))
	if len(di)>0:
			df=pd.DataFrame(dataframe_dict)
			
			make_lexrank(df)	
		
	return jsonify(di)	



		
#summary of event related tweets	
@app.route('/event_important_tweets', methods=['GET', 'POST'])
def event_important_tweets():

	di={}
	
	summary_name=request.form['data']
	no=request.form['count']
	print("summary_name",summary_name)
	print("no",no)


	if os.path.exists('data/top_5_events_summary/%s.json'%(summary_name)):
		with open('data/top_5_events_summary/%s.json'%(summary_name), 'r') as f:
			for line in f:
				z=json.loads(line)

				for key,val in z.items():
						tdict={}
						tdict["tweet_id"]=val["id_str"]
						tdict["text"]=val["text"]
						tdict["created_at"]=val["created_at"]
						tdict["location"]=val["user_location"]
						tdict["user_name"]=val["user_name"]
						tdict["retweet_count"]=val["retweet_count"]
						tdict["followers_count"]=val["follower_count"]
						
						di[key]=tdict

			
			
					#di[key]=[val["id_str"],val["text"],val["created_at"],val["user_location"],val["user_name"],val["follower_count"]]

	
		return jsonify(di)	

	else:
		return jsonify(di)	





#==============================================================================================================================	
# read data of each type and plot on map

# call for ve data to plot on map
# read ve collection and get required information	
@app.route('/violence_extremism', methods=['GET', 'POST'])
def violence_extremism():
	ve={}
	with open("location_dictionary.json", 'r') as file:
			di = json.load(file)
				
	#read ve collection
	#cursor_ve = mycol_ve.find(no_cursor_timeout=True)
	cursor_ve = []
	for i in range(5):
		mycol_ve=mydb[i]["ve"]
		cursor_veL = list(mycol_ve.find(no_cursor_timeout=True))
		cursor_ve.extend(cursor_veL)

	#print("Ve count..........",mydb.ve.count())	
	sum_ve =0
	for i in range(5):
		mycol_ve=mydb[i]["ve"]
		sum_ve = sum_ve + mycol_ve.count()
	print("Ve count..........",sum_ve)	
	for obj in cursor_ve:
		try:
			#print("getting.....")
			
			del obj['_id']				
			tweet=obj['text']
			
						
			location = (obj['user']['location']).rstrip()
			
			location = location.split("\n")
			l = ' '.join(location)
			l = l.lower()

			t1=obj['created_at']
			datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
			x = time.mktime(datetime_object.timetuple())
			for key1 in di:
				if key1 in l:
					lat_log = di[key1]
					lat = lat_log[0]						
					longi = lat_log[1]
					ve[obj['id']] = [lat, longi, "ve",obj['user']['screen_name'],[obj['id'], x],obj['created_at'],l,obj["text"]]
					break
		except:
			continue
	
	return jsonify(ve)
	#cursor_ve.close()


# call for nve data to plot on map
@app.route('/non_violence_extremism', methods=['GET', 'POST'])
def non_violence_extremism():
	nve={}
	with open("location_dictionary.json", 'r') as file:
			di = json.load(file)
				
	#read ve collection
	#cursor_nve = mycol_nve.find(no_cursor_timeout=True)
	cursor_nve = []
	for i in range(5):
		mycol_nve=mydb[i]["nve"]
		cursor_nveL = list(mycol_nve.find(no_cursor_timeout=True))
		cursor_nve.extend(cursor_nveL)


	#print("nve count..........",mydb.nve.count())
	sum_nve =0
	for i in range(5):
		mycol_nve=mydb[i]["nve"]
		sum_nve = sum_nve + mycol_nve.count()

	print("nve count..........",sum_nve)

	for obj in cursor_nve:
		try:
			del obj['_id']				
			tweet=obj['text']
			location = (obj['user']['location']).rstrip()
			location = location.split("\n")
			l = ' '.join(location)
			l = l.lower()

			t1=obj['created_at']
			datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
			x = time.mktime(datetime_object.timetuple())

			for key1 in di:
				if key1 in l:
					lat_log = di[key1]
					lat = lat_log[0]
					longi = lat_log[1]
					nve[obj['id']] = [lat, longi, "nve",obj['user']['screen_name'],[obj['id'], x],obj['created_at'],l,obj["text"]]
					break
		except:
			continue
	
	return jsonify(nve)
	#cursor_nve.close()

# call for rv data to plot on map
@app.route('/radical_violence', methods=['GET', 'POST'])
def radical_violence():
	rv={}
	with open("location_dictionary.json", 'r') as file:
			di = json.load(file)
				
	#read ve collection
	#cursor_rv = mycol_rv.find(no_cursor_timeout=True)
	cursor_rv = []
	for i in range(5):
		mycol_rv=mydb[i]["rv"]
		cursor_rvL = list(mycol_rv.find(no_cursor_timeout=True))
		cursor_rv.extend(cursor_rvL)

	#print("rv count..........",mydb.rv.count())
	sum_rv =0
	for i in range(5):
		mycol_rv=mydb[i]["rv"]
		sum_rv = sum_rv + mycol_rv.count()

	print("rv count..........",sum_rv)
	for obj in cursor_rv:
		try:
			del obj['_id']				
			tweet=obj['text']
			location = (obj['user']['location']).rstrip()
			location = location.split("\n")
			l = ' '.join(location)
			l = l.lower()

			t1=obj['created_at']
			datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
			x = time.mktime(datetime_object.timetuple())
			for key1 in di:
				if key1 in l:
					lat_log = di[key1]
					lat = lat_log[0]
					longi = lat_log[1]
					rv[obj['id']] = [lat, longi, "rv",obj['user']['screen_name'],[obj['id'], x],obj['created_at'],l,obj["text"]]
					break
		except:
			continue
	
	return jsonify(rv)
	#cursor_rv.close()


# call for nrv data to plot on map
@app.route('/non_radical_violence', methods=['GET', 'POST'])
def non_radical_violence():
	nrv={}
	with open("location_dictionary.json", 'r') as file:
			di = json.load(file)
				
	#read ve collection
	#cursor_nrv = mycol_nrv.find(no_cursor_timeout=True)
	cursor_nrv = []
	for i in range(5):
		mycol_nrv=mydb[i]["nrv"]
		cursor_nrvL = list(mycol_nrv.find(no_cursor_timeout=True))
		cursor_nrv.extend(cursor_nrvL)

	sum_nrv =0
	for i in range(5):
		mycol_nrv=mydb[i]["nrv"]
		sum_nrv = sum_nrv + mycol_nrv.count()
	print("nrv count..........",sum_nrv)
	for obj in cursor_nrv:
		try:
			del obj['_id']				
			tweet=obj['text']
			location = (obj['user']['location']).rstrip()
			location = location.split("\n")
			l = ' '.join(location)
			l = l.lower()

			t1=obj['created_at']
			datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
			x = time.mktime(datetime_object.timetuple())
			for key1 in di:
				if key1 in l:
					lat_log = di[key1]
					lat = lat_log[0]
					longi = lat_log[1]
					nrv[obj['id']] = [lat, longi, "nrv",obj['user']['screen_name'],[obj['id'], x],obj['created_at'],l,obj["text"]]
					break
		except:
			continue
	
	return jsonify(nrv)
	#cursor_nrv.close()





#==============================================================================================================================
# function to generate output when search with keyword
@app.route('/keyword', methods=['GET', 'POST'])
def keyword():
	'''
	 if file exists in the folder then return data of it
	 else create data related to the file and then return the keword related file
	'''
	d = "data/keyword"
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	
	
	search_keyword = request.form['data']
	
	dataframe_dict=[]
	nrv_temp = {}
	if os.path.exists("data/keyword/%s.json"%search_keyword):
		with open("data/keyword/%s.json"%search_keyword, 'r') as file:
			nrv_temp = json.load(file)
		
		return jsonify(nrv_temp)
	else:
		dictionary={}
		with open("location_dictionary.json", 'r') as file:
			di = json.load(file)
				
		#read ve collection
		#cursor_ve = mycol_ve.find(no_cursor_timeout=True)

		cursor_ve = []
		for i in range(5):
			mycol_ve=mydb[i]["ve"]
			cursor_veL = list(mycol_ve.find(no_cursor_timeout=True))
			cursor_ve.extend(cursor_veL)

		for obj in cursor_ve:
		
			try:
				del obj['_id']				
				tweet=obj['text']
				location = (obj['user']['location']).rstrip()
				location = location.split("\n")
				l = ' '.join(location)
				l = l.lower()
				
				if search_keyword in tweet:
					
					
					dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"],"image":obj["user"]["profile_image_url"]})	
					
					if obj["geo"]:
						
						geo_location = obj['geo']['coordinates']
						dictionary[obj['id']]=[geo_location[0], geo_location[1],"ve", obj['user']['screen_name'], [obj['id'], 1519866536.0],obj['created_at'],l,obj["text"],obj["user"]["profile_image_url"]]
					else:
						for key1 in di:
							
							if key1 in l:
								lat_log = di[key1]
								lat = lat_log[0]
								longi = lat_log[1]
								dictionary[obj['id']] = [lat, longi, "ve",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"],obj["user"]["profile_image_url"]]
								break
			except:
				
				continue

		#cursor_ve.close()				
		#read nve collection
		#cursor_nve = mycol_nve.find(no_cursor_timeout=True)
		cursor_nve = []
		for i in range(5):
			mycol_nve=mydb[i]["nve"]
			cursor_nveL = list(mycol_nve.find(no_cursor_timeout=True))
			cursor_nve.extend(cursor_nveL)
		for obj in cursor_nve:
			try:
				del obj['_id']
				tweet=obj['text']
				location = (obj['user']['location']).rstrip()
				location = location.split("\n")
				l = ' '.join(location)
				l = l.lower()
				if search_keyword in tweet:
					dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"],"image":obj["user"]["profile_image_url"]})		
					if obj["geo"]:
						geo_location = obj['geo']['coordinates']
						dictionary[obj['id']]=[geo_location[0], geo_location[1],"nve", obj['user']['screen_name'], [obj['id'], 1519866536.0],obj['created_at'],l,obj["text"],obj["user"]["profile_image_url"]]
					else:
						for key1 in di:
							if key1 in l:
								lat_log = di[key1]
								lat = lat_log[0]
								longi = lat_log[1]
								dictionary[obj['id']] = [lat, longi, "nve",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"],obj["user"]["profile_image_url"]]
								break
			except:
				continue		

		#cursor_nve.close()
		#read rv collection
		#cursor_rv = mycol_rv.find(no_cursor_timeout=True)
		cursor_rv = []
		for i in range(5):
			mycol_rv=mydb[i]["rv"]
			cursor_rvL = list(mycol_rv.find(no_cursor_timeout=True))
			cursor_rv.extend(cursor_rvL)


		for obj in cursor_rv:
			try:
				del obj['_id']				
				tweet=obj['text']
				location = (obj['user']['location']).rstrip()
				location = location.split("\n")
				l = ' '.join(location)
				l = l.lower()
				if search_keyword in tweet:
					dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"],"image":obj["user"]["profile_image_url"]})		
					if obj["geo"]:
						geo_location = obj['geo']['coordinates']
						dictionary[obj['id']]=[geo_location[0], geo_location[1],"rv", obj['user']['screen_name'], [obj['id'], 1519866536.0],obj['created_at'],l,obj["text"],obj["user"]["profile_image_url"]]
					else:
						for key1 in di:
							if key1 in l:
								lat_log = di[key1]
								lat = lat_log[0]
								longi = lat_log[1]
								dictionary[obj['id']] = [lat, longi, "rv",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"],obj["user"]["profile_image_url"]]
								break
			except:
				continue		

		#cursor_rv.close()
		#read nrv collection
		#cursor_nrv = mycol_nrv.find(no_cursor_timeout=True)
		cursor_nrv = []
		for i in range(5):
			mycol_nrv=mydb[i]["nrv"]
			cursor_nrvL = list(mycol_nrv.find(no_cursor_timeout=True))
			cursor_nrv.extend(cursor_nrvL)

		for obj in cursor_nrv:
			try:
				del obj['_id']				
				tweet=obj['text']
				location = (obj['user']['location']).rstrip()
				location = location.split("\n")
				l = ' '.join(location)
				l = l.lower()
				
				if search_keyword in tweet:
					
					dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"],"image":obj["user"]["profile_image_url"]})		
					if obj["geo"]:
						
						geo_location = obj['geo']['coordinates']
						dictionary[obj['id']]=[geo_location[0], geo_location[1],"nrv", obj['user']['screen_name'], [obj['id'], 1519866536.0],obj['created_at'],l,obj["text"],obj["user"]["profile_image_url"]]
					else:
						for key1 in di:
							if key1 in l:
								lat_log = di[key1]
								lat = lat_log[0]
								longi = lat_log[1]
								dictionary[obj['id']] = [lat, longi, "nrv",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"],obj["user"]["profile_image_url"]]
								break
			except:
				continue		

		#cursor_nrv.close()




		#call lex_rank
		#if len(dictionary)>0:
			#df=pd.DataFrame(dataframe_dict)
			#make_lexrank1(df)
			

		with open("data/keyword/%s.json"%search_keyword, 'w') as file:
			json.dump(dictionary,file)

		time.sleep(1)
		di_temp = {}

		with open("data/keyword/%s.json"%search_keyword, 'r') as file:
			di_temp = json.load(file)
		print("done")
		return jsonify(di_temp)




@app.route('/keyword1', methods=['GET', 'POST'])
def keyword1():
	
	
	search_keyword = request.form['data']
	print("search_keyword app",search_keyword)
	print("len of key",len(search_keyword))	
	list_=search_keyword.split()
	print("list_ :",list_)
	pid = os.fork()
	if pid == 0: # pid is only equal to 0 in the child process
		# os.system('python try_keyword.py --keyword {} '.format(search_keyword))
		os.system('bash try_keyword.sh {}'.format(search_keyword))
	
	# subprocess.Popen(["python.exe", "try_keyword.py --keyword {} '.format(search_keyword)"])
		
	return search_keyword;	


clf = load('logistic_regression.joblib')

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    """
        text: a string

        return: modified initial string
    """
    #text = BeautifulSoup(text, "lxml").text  # HTML decoding
    text = text.lower()  # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text)  # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)  # delete stopwors from text
    return text

@app.route('/violent_keyword1', methods=['GET', 'POST'])
def violent_keyword1():
	
	di={}
	search_keyword = request.form['data']
	print("search_keyword inside all tweets ",search_keyword)
	
	str = 'python Data_collect3.py '+search_keyword

	if os.path.exists("Data_collect/realtime_violent_tweets.json")==True :
		os.remove("Data_collect/realtime_violent_tweets.json")

	os.system(str)

	with open("Data_collect/realtime_violent_tweets.json","r") as f:
		for line in f:
			tweet = json.loads(line)

			try :
				text=clean_text(tweet["text"])
				result=clf.predict([text])
				if result[0]=='ve' or result[0]=='rv' :
					tdict={}
					tdict["tweet_id"]=tweet["id_str"]
					tdict["text"]=tweet["text"]
					# datetime_object = datetime.strptime(str(tweet["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
					# tweet_time = time.mktime(datetime_object.timetuple())
					tdict["created_at"]=tweet["created_at"]
					# tdict["tweet_time"]=tweet_time
					tdict["tweet_time"]=tweet["created_at"]
					tdict["location"]=tweet["user"]["location"]
					tdict["user_name"]=tweet["user"]["name"]
					tdict["retweet_count"]=tweet["retweet_count"]
					tdict["followers_count"]=tweet["user"]["followers_count"]
					di[tweet["id_str"]]=tdict
			except:
				continue

	return jsonify(di)


# status_count=0
# file_count=0
# class Stream2Screen(tweepy.StreamListener):
#     def on_status(self, status):
#         print(status._json)
#         with open('Data_collect/realtime_tweets.json', 'a') as file:
#             json.dump(status._json, file)
#             file.write('\n')

@app.route('/all_keyword1', methods=['GET', 'POST'])
def all_button_keyword():
	
	# class Stream2Screen(tweepy.StreamListener):
	#     def on_status(self, status):
	#         print(status._json)
	#         with open('Data_collect/realtime_tweets.json', 'a') as file:
	#             json.dump(status._json, file)
	#             file.write('\n')

	di={}
	search_keyword = request.form['data']
	print("search_keyword inside all tweets ",search_keyword)
	
	str = 'python Data_collect2.py '+search_keyword

	if os.path.exists("Data_collect/realtime_tweets.json")==True :
		os.remove("Data_collect/realtime_tweets.json")

	os.system(str)

	with open("Data_collect/realtime_tweets.json","r") as f:
		for line in f:
			tweet = json.loads(line)

			tdict={}
			tdict["tweet_id"]=tweet["id_str"]
			tdict["text"]=tweet["text"]
			# datetime_object = datetime.strptime(str(tweet["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
			# tweet_time = time.mktime(datetime_object.timetuple())
			tdict["created_at"]=tweet["created_at"]
			# tdict["tweet_time"]=tweet_time
			tdict["tweet_time"]=tweet["created_at"]
			tdict["location"]=tweet["user"]["location"]
			tdict["user_name"]=tweet["user"]["name"]
			tdict["retweet_count"]=tweet["retweet_count"]
			tdict["followers_count"]=tweet["user"]["followers_count"]
			di[tweet["id_str"]]=tdict
	#cursor = mycol_total_keyword.find(no_cursor_timeout=True)
	# cursor = []
	# for i in range(5):
	# 	mycol_total_keyword=mydb[i]["all_data"]
	# 	cursor_all_data = list(mycol_total_keyword.find(no_cursor_timeout=True))
	# 	cursor.extend(cursor_all_data)
	# for ele in cursor:
	# 	try:
	# 		del ele['_id']

			# tdict={}
			# tdict["tweet_id"]=ele["id_str"]
			# tdict["text"]=ele["text"]
			# datetime_object = datetime.strptime(str(ele["created_at"]), '%a %b %d %H:%M:%S +0000 %Y')
			# tweet_time = time.mktime(datetime_object.timetuple())
			# tdict["created_at"]=ele["created_at"]
			# tdict["tweet_time"]=tweet_time
			# tdict["location"]=ele["user"]["location"]
			# tdict["user_name"]=ele["user"]["name"]
			# tdict["retweet_count"]=ele["retweet_count"]
			# tdict["followers_count"]=ele["user"]["followers_count"]
			# di[ele["id_str"]]=tdict

	# 	except:
	# 		continue
	# di=sorted(di.items(), key=lambda x:getitem(x[1],'tweet_time'), reverse=True)
	# print("len of di : ",len(di))
	# x=0	
	# if(len(di)>50) :
	# 	di_2={}
	# 	for key,val in di :
	# 		if(x<50) :
	# 			di_2[key]=val
	# 			x=x+1
	# 		else:
	# 			break
	# 	di=sorted(di_2.items(), key=lambda x:getitem(x[1],'tweet_time'), reverse=True)		
	# 	print("len of new dict",len(di))

	return jsonify(di)












#==============================================================================================================================
# function to generate output when search with location
	
@app.route('/location', methods=['GET', 'POST'])
def location():
	'''
	 if file exists in the folder then return data of it
	 else create data related to the file and then return the keword related file
	'''
	d = "data/states"
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	
	
	selected_state = request.form['data']
	print(selected_state)
	
	dataframe_dict=[]
	if os.path.exists("data/states/%s.json"%selected_state):
		with open("data/states/%s.json"%selected_state, 'r') as file:
			state_data = json.load(file)
		return jsonify(state_data)
	else:
		dictionary={}
		with open("all_states_json/%s.json"%selected_state, 'r') as file:
			di = json.load(file)


		#read ve collection
		#cursor_ve = mycol_ve.find(no_cursor_timeout=True)
		cursor_ve = []
		for i in range(5):
			mycol_ve=mydb[i]["ve"]
			cursor_veL = list(mycol_ve.find(no_cursor_timeout=True))
			cursor_ve.extend(cursor_veL)

		for obj in cursor_ve:
			try:
				del obj['_id']	
				location = (obj['user']['location']).rstrip()
				location = location.split("\n")
				l = ' '.join(location)
				l = l.lower()			
				for key1 in di:
					if key1 in l:
						dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"]})

						lat_log = di[key1]
						lat = lat_log[0]
						longi = lat_log[1]
						dictionary[obj['id']] = [lat, longi, "ve",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]					
						break
			except:
				continue

		#cursor_ve.close()			
		
		#read nve collection
		#cursor_nve = mycol_nve.find(no_cursor_timeout=True)

		cursor_nve = []
		for i in range(5):
			mycol_nve=mydb[i]["nve"]
			cursor_nveL = list(mycol_nve.find(no_cursor_timeout=True))
			cursor_nve.extend(cursor_nveL)
		for obj in cursor_nve:
			try:
				del obj['_id']	
				location = (obj['user']['location']).rstrip()
				location = location.split("\n")
				l = ' '.join(location)
				l = l.lower()			
				for key1 in di:
					if key1 in l:
						dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"]})

						lat_log = di[key1]
						lat = lat_log[0]
						longi = lat_log[1]
						dictionary[obj['id']] = [lat, longi, "nve",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]					
						break
			except:
				continue

		#cursor_nve.close()	

		#read rv collection
		#cursor_rv = mycol_rv.find(no_cursor_timeout=True)
		cursor_rv = []
		for i in range(5):
			mycol_rv=mydb[i]["rv"]
			cursor_rvL = list(mycol_rv.find(no_cursor_timeout=True))
			cursor_rv.extend(cursor_rvL)



		for obj in cursor_rv:
			try:
				del obj['_id']	
				location = (obj['user']['location']).rstrip()
				location = location.split("\n")
				l = ' '.join(location)
				l = l.lower()			
				for key1 in di:
					if key1 in l:
						dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"]})

						lat_log = di[key1]
						lat = lat_log[0]
						longi = lat_log[1]
						dictionary[obj['id']] = [lat, longi, "rv",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]					
						break
			except:
				continue

		#cursor_rv.close()	


		#cursor_nrv = mycol_nrv.find(no_cursor_timeout=True)
		cursor_nrv = []
		for i in range(5):
			mycol_nrv=mydb[i]["nrv"]
			cursor_nrvL = list(mycol_nrv.find(no_cursor_timeout=True))
			cursor_nrv.extend(cursor_nrvL)

		for obj in cursor_nrv:
			try:
				del obj['_id']	
				location = (obj['user']['location']).rstrip()
				location = location.split("\n")
				l = ' '.join(location)
				l = l.lower()			
				for key1 in di:
					if key1 in l:
						dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"]})

						lat_log = di[key1]
						lat = lat_log[0]
						longi = lat_log[1]
						dictionary[obj['id']] = [lat, longi, "nrv",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]					
						break
			except:
				continue

		#cursor_nrv.close()	


		if len(dictionary)>0:
			df=pd.DataFrame(dataframe_dict)
			make_lexrank(df)
			
		with open("data/states/%s.json"%selected_state, 'w') as file:
			json.dump(dictionary,file)

		time.sleep(1)

		with open("data/states/%s.json"%selected_state, 'r') as file:
			state_data = json.load(file)
		return jsonify(state_data)		
		
		

#==============================================================================================================================
# function to generate output when search with time

@app.route('/time_analysis', methods=['GET', 'POST'])
def time_analysis():
	'''
	 if file exists in the folder then return data of it
	 else create data related to the file and then return the keword related file
	'''
	
	start_time = request.form['time1']
	end_time = request.form['time2']
	dictionary={}
	dataframe_dict=[]

	with open("location_dictionary.json", 'r') as file:
			di = json.load(file)
	
	#read ve collection
	#cursor_ve = mycol_ve.find(no_cursor_timeout=True)
	cursor_ve = []
	for i in range(5):
		mycol_ve=mydb[i]["ve"]
		cursor_veL = list(mycol_ve.find(no_cursor_timeout=True))
		cursor_ve.extend(cursor_veL)


	for obj in cursor_ve:
		try:
			del obj['_id']
			t1=obj['created_at']
					
			datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
			x = time.mktime(datetime_object.timetuple())
					
			location = (obj['user']['location']).rstrip()
			location = location.split("\n")
			l = ' '.join(location)
			l = l.lower()

			if int(x)>=int(start_time) and int(x)<=int(end_time):
				dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"]})

				if obj["geo"]:
					geo_location = obj['geo']['coordinates']
					dictionary[obj['id']]=[geo_location[0], geo_location[1],"ve", obj['user']['screen_name'], [obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]	
				else:
					for key1 in di:
						if key1 in l:
							lat_log = di[key1]
							lat = lat_log[0]
							longi = lat_log[1]
							dictionary[obj['id']] = [lat, longi, "ve",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]

							break		

		except:
			continue
	
		#cursor_ve.close()


	#read nve collection
	#cursor_nve = mycol_nve.find(no_cursor_timeout=True)
	cursor_nve = []
	for i in range(5):
		mycol_nve=mydb[i]["nve"]
		cursor_nveL = list(mycol_nve.find(no_cursor_timeout=True))
		cursor_nve.extend(cursor_nveL)



	for obj in cursor_nve:
		try:
			del obj['_id']
			t1=obj['created_at']
					
			datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
			x = time.mktime(datetime_object.timetuple())
					
			location = (obj['user']['location']).rstrip()
			location = location.split("\n")
			l = ' '.join(location)
			l = l.lower()

			if int(x)>=int(start_time) and int(x)<=int(end_time):
				dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"]})

				if obj["geo"]:
					geo_location = obj['geo']['coordinates']
					dictionary[obj['id']]=[geo_location[0], geo_location[1],"nve", obj['user']['screen_name'], [obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]	
				else:
					for key1 in di:
						if key1 in l:
							lat_log = di[key1]
							lat = lat_log[0]
							longi = lat_log[1]
							dictionary[obj['id']] = [lat, longi, "nve",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]

							break		

		except:
			continue
	
		#cursor_nve.close()



	#read ve collection
	#cursor_rv = mycol_rv.find(no_cursor_timeout=True)
	cursor_rv = []
	for i in range(5):
		mycol_rv=mydb[i]["rv"]
		cursor_rvL = list(mycol_rv.find(no_cursor_timeout=True))
		cursor_rv.extend(cursor_rvL)


	for obj in cursor_rv:
		try:
			del obj['_id']
			t1=obj['created_at']
					
			datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
			x = time.mktime(datetime_object.timetuple())
					
			location = (obj['user']['location']).rstrip()
			location = location.split("\n")
			l = ' '.join(location)
			l = l.lower()

			if int(x)>=int(start_time) and int(x)<=int(end_time):
				dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"]})

				if obj["geo"]:
					geo_location = obj['geo']['coordinates']
					dictionary[obj['id']]=[geo_location[0], geo_location[1],"rv", obj['user']['screen_name'], [obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]	
				else:
					for key1 in di:
						if key1 in l:
							lat_log = di[key1]
							lat = lat_log[0]
							longi = lat_log[1]
							dictionary[obj['id']] = [lat, longi, "rv",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]

							break		

		except:
			continue
	
		#cursor_rv.close()



	#read nrv collection
	#cursor_nrv = mycol_nrv.find(no_cursor_timeout=True)
	cursor_nrv = []
	for i in range(5):
		mycol_nrv=mydb[i]["nrv"]
		cursor_nrvL = list(mycol_nrv.find(no_cursor_timeout=True))
		cursor_nrv.extend(cursor_nrvL)

	for obj in cursor_nrv:
		try:
			del obj['_id']
			t1=obj['created_at']
					
			datetime_object = datetime.strptime(t1, '%a %b %d %H:%M:%S +0000 %Y')
			x = time.mktime(datetime_object.timetuple())
					
			location = (obj['user']['location']).rstrip()
			location = location.split("\n")
			l = ' '.join(location)
			l = l.lower()

			if int(x)>=int(start_time) and int(x)<=int(end_time):
				dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"]})

				if obj["geo"]:
					geo_location = obj['geo']['coordinates']
					dictionary[obj['id']]=[geo_location[0], geo_location[1],"nrv", obj['user']['screen_name'], [obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]	
				else:
					for key1 in di:
						if key1 in l:
							lat_log = di[key1]
							lat = lat_log[0]
							longi = lat_log[1]
							dictionary[obj['id']] = [lat, longi, "nrv",obj['user']['screen_name'],[obj['id'], 1519866536.0],obj['created_at'],l,obj["text"]]

							break		

		except:
			continue
	
		#cursor_nrv.close()



	if len(dictionary)>0:
		df=pd.DataFrame(dataframe_dict)
		make_lexrank(df)
	return jsonify(dictionary)	
	



		
#==============================================================================================================================

# violence extremism events

	
	
@app.route('/ve_event', methods=['GET', 'POST'])
def ve_event():


	d = "data/violence_extremism_events/top_5_events_analysis"
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	
	time.sleep(1)
	src_files = os.listdir("data/violence_extremism_events/top_5_events")
	for file_name in src_files:
		full_file_name = os.path.join("data/violence_extremism_events/top_5_events", file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, "data/violence_extremism_events/top_5_events_analysis")
	
	with open('data/events.json', 'r') as file:
		event = json.load(file)
	return jsonify(event)

	
@app.route('/ve_top_5_events', methods=['GET', 'POST'])
def ve_top_5_events():

	file_dict={}
	tweetPath = os.path.join("data/violence_extremism_events/top_5_events_analysis")
	tweetFiles = {"time01": os.path.join(tweetPath, "*.json")}
	count=0
	for (key, path) in tweetFiles.items():
		for filePath in glob.glob(path):
			head,tail=os.path.split(filePath)
			print("tail",tail)
			filepath = tail.split(".")		
			filepath = filepath[0]
			print("filepath",filepath)
			# filepath = filePath.split("\\")
			# filepath = filepath[1].split(".")
			# filepath = filepath[0]
			file_dict[count]=filepath
			count+=1
	
	return jsonify(file_dict)	
	
# plot all violence events on the map	
@app.route('/ve_top_5_plot', methods=['GET', 'POST'])
def ve_top_5_plot():

	di={}
	
	event_name = request.form['data']
	
	with open('data/violence_extremism_events/top_5_events_analysis/%s.json'%event_name, 'r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
					continue
	
	return jsonify(di)	
	

#-------------------------------------------------------------------------
# function to get information of each violence_extremism events seperately

@app.route('/ve_events_information', methods=['GET', 'POST'])
def ve_events_information():
	current_event_name = request.form['data']
	
	di={}
	
	with open('data/violence_extremism_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
					continue
	
	return jsonify(di)

# function to get tweets with images only
@app.route('/ve_event_images', methods=['GET', 'POST'])
def ve_event_images():
	current_event_name = request.form['data']
	di={}
	
	with open('data/violence_extremism_events/top_5_events_images/%s.json'%current_event_name, 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
					tdict={}
					tdict["tweet_id"]=val["tweet_id"]
					tdict["text"]=val["text"]
					tdict["image_url"]=val["image_url"]
					tdict["location"]=val["location"]
					tdict["class"]=val["class"]
					di[key]=tdict
	
	return jsonify(di)		

# summary of violence_extremism events
@app.route('/ve_events_summary', methods=['GET', 'POST'])
def ve_events_summary():
	di={}
	
	summary_name=request.form['data']
	with open('data/violence_extremism_events/top_5_events_summary/%s.json'%summary_name, 'r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
					tdict={}
					tdict["tweet_id"]=val["id_str"]
					tdict["text"]=val["text"]
					tdict["created_at"]=val["created_at"]
					tdict["location"]=val["user_location"]
					tdict["user_name"]=val["user_name"]
					tdict["retweet_count"]=val["retweet_count"]
					tdict["followers_count"]=val["follower_count"]
						
					di[key]=tdict

	return jsonify(di)	
	


#==============================================================================================================================
# non violence extremism events
@app.route('/nve_event', methods=['GET', 'POST'])
def nve_event():


	d = "data/non_violence_extremism_events/top_5_events_analysis"
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	
	time.sleep(1)
	src_files = os.listdir("data/non_violence_extremism_events/top_5_events")
	for file_name in src_files:
		full_file_name = os.path.join("data/non_violence_extremism_events/top_5_events", file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, "data/non_violence_extremism_events/top_5_events_analysis")
	
	with open('data/events.json', 'r') as file:
		event = json.load(file)
	return jsonify(event)

	
@app.route('/nve_top_5_events', methods=['GET', 'POST'])
def nve_top_5_events():

	file_dict={}
	tweetPath = os.path.join("data/non_violence_extremism_events/top_5_events_analysis")
	tweetFiles = {"time01": os.path.join(tweetPath, "*.json")}
	count=0
	for (key, path) in tweetFiles.items():
		for filePath in glob.glob(path):
			head,tail=os.path.split(filePath)
			print("tail",tail)
			filepath = tail.split(".")		
			filepath = filepath[0]
			print("filepath",filepath)
			# filepath = filePath.split("\\")
			# filepath = filepath[1].split(".")
			# filepath = filepath[0]
			file_dict[count]=filepath
			count+=1
	
	return jsonify(file_dict)	
	
# plot all non violence events on the map	
@app.route('/nve_top_5_plot', methods=['GET', 'POST'])
def nve_top_5_plot():
	
	di={}
	
	event_name = request.form['data']
	
	with open('data/non_violence_extremism_events/top_5_events_analysis/%s.json'%event_name, 'r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
					continue
	
	return jsonify(di)	


#-----------------------------------------------------------------------------
# function to get information of each non_violence_extremism events seperately

@app.route('/nve_events_information', methods=['GET', 'POST'])
def nve_events_information():
	current_event_name = request.form['data']
	
	di={}
	
	with open('data/non_violence_extremism_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
					continue
	
	return jsonify(di)

# function to get tweets with images only
@app.route('/nve_event_images', methods=['GET', 'POST'])
def nve_event_images():
	current_event_name = request.form['data']
	di={}
	
	with open('data/non_violence_extremism_events/top_5_events_images/%s.json'%current_event_name, 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
					tdict={}
					tdict["tweet_id"]=val["tweet_id"]
					tdict["text"]=val["text"]
					tdict["image_url"]=val["image_url"]
					tdict["location"]=val["location"]
					tdict["class"]=val["class"]
					di[key]=tdict
	
	return jsonify(di)		
	
	
	
	
	
	
# summary of violence_extremism events
@app.route('/nve_events_summary', methods=['GET', 'POST'])
def nve_events_summary():
	di={}
	
	summary_name=request.form['data']
	with open('data/non_violence_extremism_events/top_5_events_summary/%s.json'%summary_name, 'r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
					tdict={}
					tdict["tweet_id"]=val["id_str"]
					tdict["text"]=val["text"]
					tdict["created_at"]=val["created_at"]
					tdict["location"]=val["user_location"]
					tdict["user_name"]=val["user_name"]
					tdict["retweet_count"]=val["retweet_count"]
					tdict["followers_count"]=val["follower_count"]
						
					di[key]=tdict

	return jsonify(di)	
	
	
	
#==============================================================================================================================
	
# radical violence events
@app.route('/rv_event', methods=['GET', 'POST'])
def rv_event():


	d = "data/radical_violence_events/top_5_events_analysis"
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	
	time.sleep(1)
	src_files = os.listdir("data/radical_violence_events/top_5_events")
	for file_name in src_files:
		full_file_name = os.path.join("data/radical_violence_events/top_5_events", file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, "data/radical_violence_events/top_5_events_analysis")
	
	with open('data/events.json', 'r') as file:
		event = json.load(file)
	return jsonify(event)

	
@app.route('/rv_top_5_events', methods=['GET', 'POST'])
def rv_top_5_events():

	file_dict={}
	tweetPath = os.path.join("data/radical_violence_events/top_5_events_analysis")
	tweetFiles = {"time01": os.path.join(tweetPath, "*.json")}
	count=0
	for (key, path) in tweetFiles.items():
		for filePath in glob.glob(path):
			head,tail=os.path.split(filePath)
			print("tail",tail)
			filepath = tail.split(".")		
			filepath = filepath[0]
			print("filepath",filepath)
			# filepath = filePath.split("\\")
			# filepath = filepath[1].split(".")
			# filepath = filepath[0]
			file_dict[count]=filepath
			count+=1
	
	return jsonify(file_dict)	
	
# plot all radical violence events on the map	
@app.route('/rv_top_5_plot', methods=['GET', 'POST'])
def rv_top_5_plot():
	di={}
	
	event_name = request.form['data']
	
	with open('data/radical_violence_events/top_5_events_analysis/%s.json'%event_name, 'r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
					continue
	
	return jsonify(di)	
	
	
	
#-----------------------------------------------------------------------
# function to get information of each radical_violence events seperately


@app.route('/rv_events_information', methods=['GET', 'POST'])
def rv_events_information():
	current_event_name = request.form['data']
	
	di={}
	
	with open('data/radical_violence_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
					continue
	
	return jsonify(di)

# function to get tweets with images only
@app.route('/rv_event_images', methods=['GET', 'POST'])
def rv_event_images():
	current_event_name = request.form['data']
	di={}
	
	with open('data/radical_violence_events/top_5_events_images/%s.json'%current_event_name, 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
					tdict={}
					tdict["tweet_id"]=val["tweet_id"]
					tdict["text"]=val["text"]
					tdict["image_url"]=val["image_url"]
					tdict["location"]=val["location"]
					tdict["class"]=val["class"]
					di[key]=tdict
	
	return jsonify(di)	
	
	
# summary of radical_violence events
@app.route('/rv_events_summary', methods=['GET', 'POST'])
def rv_events_summary():
	di={}
	
	summary_name=request.form['data']
	with open('data/radical_violence_events/top_5_events_summary/%s.json'%summary_name, 'r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
					tdict={}
					tdict["tweet_id"]=val["id_str"]
					tdict["text"]=val["text"]
					tdict["created_at"]=val["created_at"]
					tdict["location"]=val["user_location"]
					tdict["user_name"]=val["user_name"]
					tdict["retweet_count"]=val["retweet_count"]
					tdict["followers_count"]=val["follower_count"]
						
					di[key]=tdict

	return jsonify(di)	
	
	
#==============================================================================================================================

# non radical violence events
@app.route('/nrv_event', methods=['GET', 'POST'])
def nrv_event():


	d = "data/non_radical_violence_events/top_5_events_analysis"
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			os.remove(full_path)
	
	time.sleep(1)
	src_files = os.listdir("data/non_radical_violence_events/top_5_events")
	for file_name in src_files:
		full_file_name = os.path.join("data/non_radical_violence_events/top_5_events", file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, "data/non_radical_violence_events/top_5_events_analysis")
	
	with open('data/events.json', 'r') as file:
		event = json.load(file)
	return jsonify(event)

	
@app.route('/nrv_top_5_events', methods=['GET', 'POST'])
def nrv_top_5_events():

	file_dict={}
	tweetPath = os.path.join("data/non_radical_violence_events/top_5_events_analysis")
	tweetFiles = {"time01": os.path.join(tweetPath, "*.json")}
	count=0
	for (key, path) in tweetFiles.items():
		for filePath in glob.glob(path):
			head,tail=os.path.split(filePath)
			print("tail",tail)
			filepath = tail.split(".")		
			filepath = filepath[0]
			print("filepath",filepath)
			# filepath = filePath.split("\\")
			# filepath = filepath[1].split(".")
			# filepath = filepath[0]
			file_dict[count]=filepath
			count+=1
	
	return jsonify(file_dict)	
	
# plot all non radical violence events on the map	
@app.route('/nrv_top_5_plot', methods=['GET', 'POST'])
def nrv_top_5_plot():

	di={}
	
	event_name = request.form['data']

	with open('data/non_radical_violence_events/top_5_events_analysis/%s.json'%event_name, 'r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
					continue
	
	return jsonify(di)	
	
	
	
#---------------------------------------------------------------------------
# function to get information of each non_radical_violence events seperately

@app.route('/nrv_events_information', methods=['GET', 'POST'])
def nrv_events_information():
	current_event_name = request.form['data']
	print("current_event_name",current_event_name)
	di={}
	
	with open('data/non_radical_violence_events/top_5_events_analysis/%s.json'%current_event_name, 'r') as f:
		print("file open")
		for line in f:
			z=json.loads(line)
			print("tweet",z)
			for key,val in z.items():
				try:
					di[key]=[val["latitude"],val["longitude"],val["ename"],val["created_at"],val["main_event"],val["user_location"],val['text'],val['user_name']]
				except:
					continue
	print("di",di)
	return jsonify(di)
	
# function to get tweets with images only
@app.route('/nrv_event_images', methods=['GET', 'POST'])
def nrv_event_images():
	current_event_name = request.form['data']
	di={}
	
	with open('data/non_radical_violence_events/top_5_events_images/%s.json'%current_event_name, 'r') as f:
		for line in f:
			z=json.loads(line)
			for key,val in z.items():
					tdict={}
					tdict["tweet_id"]=val["tweet_id"]
					tdict["text"]=val["text"]
					tdict["image_url"]=val["image_url"]
					tdict["location"]=val["location"]
					tdict["class"]=val["class"]
					di[key]=tdict
	
	return jsonify(di)	
	
# summary of non_radical_violence events
@app.route('/nrv_events_summary', methods=['GET', 'POST'])
def nrv_events_summary():
	di={}
	
	summary_name=request.form['data']
	with open('data/non_radical_violence_events/top_5_events_summary/%s.json'%summary_name, 'r') as f:
		for line in f:
			z=json.loads(line)

			for key,val in z.items():
					tdict={}
					tdict["tweet_id"]=val["id_str"]
					tdict["text"]=val["text"]
					tdict["created_at"]=val["created_at"]
					tdict["location"]=val["user_location"]
					tdict["user_name"]=val["user_name"]
					tdict["retweet_count"]=val["retweet_count"]
					tdict["followers_count"]=val["follower_count"]
						
					di[key]=tdict

	return jsonify(di)		
	
	
	
	
	
#=============================================================================================================================	
# important tweets or summary of classwise and summary of main classified contents
@app.route('/important_tweets', methods=['GET', 'POST'])
def important_tweets():

	di={}
	
	with open("location_dictionary.json", 'r') as file:
		di = json.load(file)

	dataframe_dict=[]
	
	summary_name=request.form['data']
			
	#cursor_all = mycol2hour.find(no_cursor_timeout=True)
	cursor_all = []
	for i in range(5):
		mycol2hour=mydb[i]["test2hour"]
		cursor2hour = list(mycol2hour.find(no_cursor_timeout=True))
		cursor_all.extend(cursor2hour)


	for obj in cursor_all:
		try:
			del obj['_id']	
			location = (obj['user']['location']).rstrip()
			location = location.split("\n")
			l = ' '.join(location)
			l = l.lower()			
			if 'media' in obj['entities']:
				media=(obj['entities']['media'])
				media=media[0]
				url=media['media_url']			

				for key1 in di:
					if key1 in l:
						dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"],"image_url":url})	
						break
		

			else:
				for key1 in di:
					if key1 in l:
						dataframe_dict.append({"id_str":obj["id_str"],"full_text":obj["text"],"created_at":obj["created_at"],"user_name":obj["user"]["name"],"user_location":obj["user"]["location"],"follower_count":obj["user"]["followers_count"],"retweet_count":obj["retweet_count"],"image_url":""})	
						break

		except:
			continue	

	#cursor_all.close()
	
	print(len(dataframe_dict))
	di={}	
	if len(dataframe_dict)>0:	
		#df=pd.DataFrame(dataframe_dict)
		#make_lexrank_summary_all_tweets(df)
	

		print("completed summary all")
		time.sleep(2)
		print(summary_name)
		with open('imp/%s.json'%summary_name, 'r') as f:
			for line in f:
				z=json.loads(line)

				for key,val in z.items():
					
						img=val["image_url"]
						if img=='none':
							tdict={}
							tdict["tweet_id"]=val["id_str"]
							tdict["text"]=val["text"]
							tdict["created_at"]=val["created_at"]
							tdict["location"]=val["user_location"]
							tdict["user_name"]=val["user_name"]
							tdict["retweet_count"]=val["retweet_count"]
							tdict["followers_count"]=val["follower_count"]
							tdict["images"]=[]	
							tdict["urls"]=val["urls"]
							di[key]=tdict
						else:
							tdict={}
							tdict["tweet_id"]=val["id_str"]
							tdict["text"]=val["text"]
							tdict["created_at"]=val["created_at"]
							tdict["location"]=val["user_location"]
							tdict["user_name"]=val["user_name"]
							tdict["retweet_count"]=val["retweet_count"]
							tdict["followers_count"]=val["follower_count"]
							tdict["images"]=[img]	
							tdict["urls"]=val["urls"]
							di[key]=tdict
			
			
					#di[key]=[val["id_str"],val["text"],val["created_at"],val["user_location"],val["user_name"],val["follower_count"]]

	
	return jsonify(di)
	
@app.route('/viral_events', methods=['GET', 'POST'])
def viral_events():
	# di={}

	# src_files = os.listdir("data/potential_viral")
	# for file_name in src_files:
	# 	full_file_name = os.path.join("data/potential_viral", file_name)
	# 	with open(full_file_name,'r') as file:
	# 		tweets=json.load(file)
		
	# 	for key in tweets:
	# 		di[key]=tweets[key]
		

	##### code change to save viral events in dict
	file_ob=open("potential_viral_dict/dict.json",'r')
	dict_old=json.load(file_ob)
	print("len old dict",len(dict_old))

	di={}
	new={}
	for key in dict_old:
		new[key]=dict_old[key]

	print("len of new dict",len(new))

	src_files = os.listdir("data/potential_viral")
	for file_name in src_files:
		full_file_name = os.path.join("data/potential_viral", file_name)
		with open(full_file_name,'r') as file:
			tweets=json.load(file)
			
			for key in tweets:
				di[key]=tweets[key]
				new[key]=tweets[key]

	with open("potential_viral_dict/dict.json", "w+") as f4:
			f4.write(json.dumps(new))
			f4.flush()

	return jsonify(di)			


#Adding function for facebook data fetch
#This function is for violent data
@app.route('/facebook_v_data',methods=['GET', 'POST'])
def facebook_v_data():
	di={}

	count=0
	with open("facebook_data/violence_provoking/VP.json",'r') as f:
		for line in f:
			z=json.loads(line)

			tdict={}
			tdict["fb_message"]=z["message"]
			tdict["fb_created_time"]=z["created_time"]
			tdict["fb_id"]=z["id"]

			key=str(count)
			di[key]=tdict
			count=count+1
	return jsonify(di)

#This function is for non-violent data
@app.route('/facebook_nv_data',methods=['GET', 'POST'])
def facebook_nv_data():
	di={}

	count=0
	with open("facebook_data/Not_violence/NV.json",'r') as f:
		for line in f:
			z=json.loads(line)

			tdict={}
			tdict["fb_message"]=z["message"]
			tdict["fb_created_time"]=z["created_time"]
			tdict["fb_id"]=z["id"]

			key=str(count)
			di[key]=tdict
			count=count+1
	return jsonify(di)	


@app.route('/build_plot', methods=['GET', 'POST'])
def build_plot():
	img = io.BytesIO()
	
	n_groups = 4
	v1 = 13
	v2 = 34
	v3 = 34
	v4 = 35

	means_ve = (v1, 55, 40, 65)
	means_nve = (v2, 62, 54, 20)
	means_rv = (v3, 13,32,32)
	means_nrv = (v4,12,32,43)

	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.15
	opacity = 0.8

	rects1 = plt.bar(index, means_ve, bar_width,
	alpha=opacity,
	color='r',
	label='ve')

	rects2 = plt.bar(index + bar_width, means_nve, bar_width,
	alpha=opacity,
	color='b',
	label='nve')

	rects3 = plt.bar(index + 2*bar_width, means_rv, bar_width,
	alpha=opacity,
	color='y',
	label='rv')

	rects4 = plt.bar(index + 3*bar_width, means_nrv, bar_width,
	alpha=opacity,
	color='m',
	label='nrv')

	plt.xlabel('Time')
	plt.ylabel('Count')
	plt.title('No of Tweets')
	plt.xticks(index + bar_width, ('1hr', '2hr', '3hr', '4hr'))
	plt.legend()

	plt.tight_layout()
	plt.savefig(img,format="png")

	plot_url = base64.b64encode(img.getvalue()).decode()

	return '<img src="data:image/png;base64,{}">'.format(plot_url)

if __name__ == "__main__":
	app.run()
