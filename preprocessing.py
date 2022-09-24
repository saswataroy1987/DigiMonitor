# from collections import Counter

# list_words=[]		
# corpus=["hello world ","hello hii"]		
# for ele in corpus:
# 	for x in ele.split():
# 		list_words.append(x)
			
# x=Counter(list_words)
# y=x.most_common(3)	
# print(y)
# if len(y)==3:
# 	event_name=y[0][0]+" "+y[1][0]+" "+y[2][0]
# elif len(y)==2:
# 	event_name=y[0][0]+" "+y[1][0]
# else:
# 	event_name=y[0][0]

# print("#################   Event name:   ",event_name)
path='data/Event_data'
from collections import Counter
import os
import json
import preprocessor as p
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import re


def removepunc(s):
        #URLless_string = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', s)
        punctuations = '''-[]{}'"\,<>./?$%^&*_~'''
        no_punct = ""
        for char in s:
                if char not in punctuations:
                        no_punct = no_punct + char
        return no_punct
def preprocessing(tweet):
	text1=str(''.join([i if ord(i) < 128 else ' ' for i in tweet]))#remove characters having ACII values more than 127
	result = ''.join([i for i in text1 if not i.isdigit()])#remove digits
	#result= removepunc(result)
	result = re.sub("<.*?#@>","",result)
	result = re.sub(r"http\S+", "", result)
	#print result
	result=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",result).split())
	result= result.lstrip("RT")
	return result

def remove_stopwords(example_sent):
	stop_words = set(stopwords.words('english')) 
	word_tokens = word_tokenize(example_sent) 
	filtered_sentence = []
	filtered_sentence = [w for w in word_tokens if not w in stop_words] 
	filtered_sentence=' '.join(filtered_sentence)
	return filtered_sentence



articles = {'where': '', 'here':'', 'wherever':'', 'there':''}



def preprocessing_tweets(all_tweets):
		
	all_tweets=removepunc(all_tweets)
	all_tweets=preprocessing(all_tweets)
	all_tweets=remove_stopwords(all_tweets)
	all_tweets=all_tweets.lower()
	all_tweets=re.sub(r'\b\w{1,3}\b', '',all_tweets)
	for i, j in articles.items():
		all_tweets = all_tweets.replace(i, j)
			
	return all_tweets
