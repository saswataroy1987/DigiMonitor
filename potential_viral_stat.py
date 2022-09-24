import time
import os
import json
from datetime import datetime



while True:
	
	di={}
	src_files = os.listdir("data/potential_viral")
	for file_name in src_files:
		full_file_name = os.path.join("data/potential_viral", file_name)
		with open(full_file_name,'r') as file:
			tweets=json.load(file)
			
			for key in tweets:
				di[key]=tweets[key]
	now = datetime.now()
	now = str(now)

	with open("potential_viral_history_ra/history_ra_current.json",'a') as f4:
			f4.write("\n\n")
			f4.write(now)
			f4.write(json.dumps(di))
			f4.flush()
	time.sleep(600)

