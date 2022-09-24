from lexrank import STOPWORDS, LexRank
from path import Path
import json
import pandas as pd
import json_csv as js
import os
import urllib.request
import time
import pandas as pd

path_top_5_events='data/non_violence_extremism_events/top_5_events'
image_path='data/images_nve'
def tweet_images_Generation(filename):

	dictionary_temporary={}

	with open("data/non_violence_extremism_events/top_5_events/%s"%filename,"r") as f:
		for line in f:
			tweet=json.loads(line)	
			for key,val in tweet.items():
				try:
					image_url=val["image_url"]
					if image_url=='none':
						continue
					else:
						if os.path.exists('data/images_nve/%s.jpg'%val["id_str"]):
							#print("CONGRATS IMAGE EXISTS")
							continue
						else:
							urllib.request.urlretrieve(image_url, 'data/images_nve/%s.jpg'%val["id_str"])
				except:
					continue
	
				



def start():
	list_files_top_5_events=os.listdir(path_top_5_events)
	for single_file in list_files_top_5_events:
	 	tweet_images_Generation(single_file)
	#os.system('python Image_pred.py --img_dir data/images --output_csvpath result.csv --model model_best.pth.tar ')
	if os.listdir(image_path) == []:
		print("No image.................####################")
	else:
		os.system('python predicted_nve.py')
		#<decide top5 classes from dataframe>
		dictionary_temporary={}
		list_ids=[]
		di_image_classes={}
		df=pd.read_csv("result_nve.csv",delimiter=",")
		for i,row in df.iterrows():
			id_png=row["imgpath"].split("/")[2]
			id1=id_png.split(".")[0]
			list_ids.append(id1)
			list_class_name=["RV", "NRV", "VE", "NVE" ,"NONE"]
			list_class_prob=[row["RV"],row["NRV"],row["VE"],row["NVE"],row["NONE"]]
			tuples=list(zip(list_class_name,list_class_prob))
			tuples_sorted=sorted(tuples,key=lambda x: x[1], reverse=True)
			string=tuples_sorted[0][0]+" "+tuples_sorted[1][0]+" "+tuples_sorted[2][0]
			di_image_classes[id1]=string
		
		#print(list_ids)
		for single_file in list_files_top_5_events:
		 	with open("data/non_violence_extremism_events/top_5_events/%s"%single_file,"r") as f:
		 		for line in f:
		 			dict_event=json.loads(line)
		 			for key,val in dict_event.items():
		 					if key in list_ids:
		 						dictionary_temporary[key]={"tweet_id":val["id_str"],"text":val["text"],"image_url":val["image_url"],"location":val["user_location"],"class":di_image_classes[key]}
		 					else:
		 						continue
		 	with open("data/non_violence_extremism_events/top_5_events/%s"%single_file,"a") as f1:
		 		json.dump(dictionary_temporary,f1)
	
	
# start1=time.time()
# print("Start")
start()
# end1=time.time()
# print("Stop")
# print("total time",(end1-start1))




