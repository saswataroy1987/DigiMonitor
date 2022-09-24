import threading
import queue
import tweepy
from tweepy.api import API
from datetime import datetime
import time
import pymongo
import json
import os
from joblib import dump, load
from nltk.corpus import stopwords
import re

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



myclient = [ pymongo.MongoClient("mongodb://localhost:2017/"),pymongo.MongoClient("mongodb://localhost:2018/"),pymongo.MongoClient("mongodb://localhost:2019/"),pymongo.MongoClient("mongodb://localhost:2020/"),pymongo.MongoClient("mongodb://localhost:2021/") ]

mydb = []

for temp in myclient:
    mydb.append(temp["RealData"])


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["RealData"]

# mycol10min = mydb["test10min"]
# mycol2hour= mydb["test2hour"]
# mycol_virality=mydb["virality"]

# mycol_ve = mydb["ve"]
# mycol_nve = mydb["nve"]
# mycol_rv = mydb["rv"]
# mycol_nrv = mydb["nrv"]
# mycol_total=mydb["all_data"]
# mycol_nr=mydb["nr"]


# API_KEY = 'J5gbq2RYbUrApGUfleIqh40wa'
# API_SECRET = 'skUaXgI5GEGnWRbSJ7AwQHXERFQL8f9UaYOBMPmzpj7mWV1LxA'
# ACCESS_TOKEN = '917327613009346561-UL0h721YdEhOg2nIkdQ9o8NFpHvWPcX'
# ACCESS_TOKEN_SECRET = 'dXHYIUqqPYqFS95tcG7IC9zJcoRfQ0pq8JUq19UY0M4yH'

# API_KEY = 'msH9Y1pg3zQOUjATGpkrWcALP'
# API_SECRET = 'LTdgEns9v07a7bvv6DYNMwHO8O9GjnEXMNhNunjcVmSQ11UkHi'
# ACCESS_TOKEN = '917327613009346561-6s8o5AoOKjlXbmEgdYtwmWqWMZ26erS'
# ACCESS_TOKEN_SECRET = 'yr6eBCunVPMN9v75q0ZeeOz8Ui66KxBgNRyjjdQEYY8OR'


# API_KEY = 'yhM1kZSDl1j3LTR170HQeyagH'
# API_SECRET = 'YJOtpnVXX77icmxouxxzUXYgrbnpTbFo1aOCngz0kCgcaZeQEE'
# ACCESS_TOKEN = '917327613009346561-Bq1Acg5QO2Z973e56Zu9B7nUz25hKf7'
# ACCESS_TOKEN_SECRET = 'HuSSHLuYXBWeXZ6Luvaxr2QQejqxQx3GYBa4oBWW0znBA'

# API_KEY = 'FbgDtBVv0XQIFYeIwIjVfA8uo'
# API_SECRET = 'ILdjEqWZl8dQQLGwle9dSrMMndOaHO7MsFhXsBr04mgBjhH3dN'
# ACCESS_TOKEN = '917327613009346561-KgdKwnE32th6gQuMTVQvy0Eegv1wooD'
# ACCESS_TOKEN_SECRET = 'PQ8Q18QlZSeIjeYn4XAd1rsosB2KDocvTPEW5XynygzXH'

#API_KEY = 'SZH0v370G1aB9f2YRjmhmhYbL'
#API_SECRET = 'QFg7SzFCYeDM71C0I6J4GphvdoQKdJpJJi7ZyyAr5UAVq9BFFv'
#ACCESS_TOKEN = '917327613009346561-fsgXMyIg9tsRoumlli651AbPql5icmG'
#ACCESS_TOKEN_SECRET = 'mkgJAbkeBwFQxRKkT9yI4NnIFjvyTZyY8AznqlZqEAoE6'


# API_KEY = "LTRIvXW6DF1VGndhhjUIQJPei"
# API_SECRET ='zu2XiN8JdHdvpH7SPadnd14d2LlosXmCZT6baEpQFefrgdrNi0'
# ACCESS_TOKEN = '917327613009346561-fsgXMyIg9tsRoumlli651AbPql5icmG'
# ACCESS_TOKEN_SECRET = 'mkgJAbkeBwFQxRKkT9yI4NnIFjvyTZyY8AznqlZqEAoE6'

API_KEY="msH9Y1pg3zQOUjATGpkrWcALP"
API_SECRET="LTdgEns9v07a7bvv6DYNMwHO8O9GjnEXMNhNunjcVmSQ11UkHi"
ACCESS_TOKEN="917327613009346561-J0NzqeUwrM6CSyO5PFGPJXuxTg9tiE0"
ACCESS_TOKEN_SECRET="NcySnBrdMtjbhZ7EMeKAZY84n88FMZxzjyFKATNxQpJh3"

key = tweepy.OAuthHandler(API_KEY, API_SECRET)
key.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

BUF_SIZE = 10000000000000
q = queue.Queue(BUF_SIZE)

paths = 'DynamicKeywords.txt'
#<--load classifier>
clf = load('logistic_regression.joblib')
clf_binary=load('logistic_regression_binary.joblib')

class Stream2Screen(tweepy.StreamListener):
    def on_data(self, data):
    	print("ty to put")
    	if not q.full():
    		#print("Producing")
    		q.put(data)
    		
    	else:
    		print("Queue is full now")

def produce():
    while True:
    	try:
            stream = tweepy.streaming.Stream(key, Stream2Screen())
            stream.filter(track=open(paths, 'r'), languages=['en'])
            
    	except:
    		continue

def consume():
    while True:
        if not q.empty():
            #print("Consuming")
            item = q.get()

            # with open('tweets.json', 'a') as file:
            #     json.dump(item._json, file)
            #     file.write('\n')
            #tweet=item._json
            itemjson = json.loads(item)
            
            print("popped")
            if "id" not in itemjson:
            	continue
            #if "media" not in itemjson['entities']:
            #	continue
           
            id_t = itemjson["id"]
            #id_t = int(itemjson["id_str"])
            try:
                text=clean_text(itemjson["text"])
                #result=clf.predict([itemjson["text"]])
                result=clf.predict([text])
                result_binary=clf_binary.predict([text])

                if result[0]=='ve':
                    #mydb.ve.insert(itemjson); 
                    mydb[id_t%5].ve.insert(itemjson)
                    
                if result[0]=='nve':
                    #mydb.nve.insert(itemjson)
                    mydb[id_t%5].nve.insert(itemjson)

                if result[0]=='rv':
                    #mydb.rv.insert(itemjson)
                    mydb[id_t%5].rv.insert(itemjson)

                if result[0]=='nrv':
                    #mydb.nrv.insert(itemjson)
                    mydb[id_t%5].nrv.insert(itemjson)

                if result[0] == 'nr':
                    #mydb.nr.insert(itemjson)
                    mydb[id_t%5].nr.insert(itemjson)
                    
                if result_binary[0]=='rel':
                	# mydb.test10min.insert(itemjson)
                	# mydb.test2hour.insert(itemjson)
                	# mydb.virality.insert(itemjson)
                    mydb[id_t%5].test10min.insert(itemjson)
                    mydb[id_t%5].test2hour.insert(itemjson)
                    mydb[id_t%5].virality.insert(itemjson)
                
                #mydb.all_data.insert(itemjson)
                #print(itemjson['entities'])
                mydb[id_t%5].all_data.insert(itemjson)
            except:
                continue
            
            
            
            #print(q.qsize())

#def begin():
if __name__ == '__main__':
    p = threading.Thread(target=produce)
    c = threading.Thread(target=consume)

    p.start()

    c.start()

    


















