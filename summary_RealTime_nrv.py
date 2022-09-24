from lexrank import STOPWORDS, LexRank
from path import Path
import json
import pandas as pd
import json_csv as js
import os
documents = []
documents_dir = Path('bbc/politics')

path_top_5_events='data/non_radical_violence_events/top_5_events'

def summary_Generation(filename):
	for file_path in documents_dir.files('*.txt'):
		with file_path.open(mode='rt', encoding='utf-8') as fp:
			documents.append(fp.readlines())

	lxr = LexRank(documents, stopwords=STOPWORDS['en'])


	list_text,list_ids=[],[]
	with open("data/non_radical_violence_events/top_5_events/%s"%filename,"r") as f:
		for line in f:
			tweet=json.loads(line)	
			for key,val in tweet.items():
				list_text.append(val["text"])
				list_ids.append(val["id_str"])





	scores_cont = lxr.rank_sentences(list_text,threshold=None,fast_power_method=False,)


	#tuples = [tuple((x, y)) for x, y in zip(list_ids,scores_cont)]
	tuples=list(zip(list_ids,scores_cont))

	tuples_sorted=sorted(tuples,key=lambda x: x[1], reverse=True)
	if len(tuples_sorted)>=10:
		list_summary_top=[]
		for i in range(0,10):
			list_summary_top.append(tuples_sorted[i][0])
			#print(list_summary_top[i])
			#print(type(list_summary_top[i])) 
	

	else:	
		list_summary_top=[]
		for i in range(0,len(tuples_sorted)):
			list_summary_top.append(tuples_sorted[i][0])


	dictionary_temporary={}

	#for i in range(0,len(list_summary_top)):
	#	print(list_summary_top[i]);input()


	i=0
	with open("data/non_radical_violence_events/top_5_events/%s"%filename,"r") as f:
		for line in f:
			tweet=json.loads(line)
			for key,val in tweet.items():		
				if val["id_str"] in list_summary_top:
					i=i+1
					dictionary_temporary[val["id_str"]]=val
				

	with open("data/non_radical_violence_events/top_5_events_summary/%s"%filename,"a") as f:
		json.dump(dictionary_temporary,f)

def start():
	list_files_top_5_events=os.listdir(path_top_5_events)
	for single_file in list_files_top_5_events:
	 	summary_Generation(single_file)






