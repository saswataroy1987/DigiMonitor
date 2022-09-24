#!/bin/sh

screen -dmS Mongo_start sh -c 'sudo service mongod start; exec bash'


screen -dmS Mongo_start1 sh -c 'docker run -p 2017:27017 --name mongo1 -d mongo; exec bash'
screen -dmS Mongo_start2 sh -c 'docker run -p 2018:27017 --name mongo2 -d mongo; exec bash'
screen -dmS Mongo_start3 sh -c 'docker run -p 2019:27017 --name mongo3 -d mongo; exec bash'
screen -dmS Mongo_start4 sh -c 'docker run -p 2020:27017 --name mongo4 -d mongo; exec bash'
screen -dmS Mongo_start5 sh -c 'docker run -p 2021:27017 --name mongo5 -d mongo; exec bash'



screen -dmS RealTime_Data_collection sh -c 'python RealTime_Data_collection_Docker.py; exec bash'

#screen -dmS FACEBOOK_Data_collection sh -c 'python facebook_data_col.py; exec bash'


screen -dmS 10min sh -c 'python RealTime_10min.py; exec bash' 

screen -dmS 2hour sh -c 'python RealTime_2hour.py; exec bash'

screen -dmS ve sh -c 'python RealTime_ve.py; exec bash'

screen -dmS nve sh -c 'python RealTime_nve.py; exec bash'

screen -dmS rv sh -c 'python RealTime_rv.py; exec bash'

screen -dmS nrv sh -c 'python RealTime_nrv.py; exec bash'

screen -dmS potential_viral_stat sh -c 'python potential_viral_stat.py; exec bash'

screen -dmS event_stat sh -c 'python event_stat_ash.py; exec bash'

#screen -dmS dynamic_query_expansion sh -c 'python dynamic_query_expansion.py; exec bash'

# screen -dmS get_trending sh -c 'python get_trending.py; exec bash'

#screen -dmS merge_all_three sh -c 'python merge_all_three.py; exec bash'
