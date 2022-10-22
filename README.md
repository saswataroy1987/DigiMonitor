# DigiMonitor
## Developers : __Saswata Roy, Brijendra Suman, Asutosh, Ravi__
Digimonitor is a Real-Time CyberSpace Monitoring tool that uses supervised and unsupervised techniques on social media data like Twitter and Facebook. It is an integrated Real Time DigiMonitor framework which performs three major tasks in parallel. Data Collection (Task I): Continuously crawling relevant tweets and classify the tweets before storing them in database (MongoDB). Identification of important events (Task II): Continuously monitoring the tweets (last 7 days) for detecting major events dynamically. Virality Prediction (Task III): Continuously monitor the tweets and predict whether any of these tweets would become viral.


## Steps
* We prepare a set of 232 riots/violence-provoking key phrases such as “jihad kill people”, “rally riots dead” (see "Keywords.txt" file) from various news articles and wikipedia.
* We then use the Twitter streaming API to collect real time tweets with the help of the above-mentioned keywords and store all the collected tweets under N different MongoDB. Each MongoDB is kept under different Docker Containers.


## Installation Guidelines



### Code Avaialability
~~~~
Code will only be made public for the research purpose. Contact at @saswataroy.1987@gmail.com and provide valid reasons 
~~~~

## DigiMonitor Architecture

![](DigiMonitor.png)


## DigiMonitor Demo

https://user-images.githubusercontent.com/99898404/192083381-b6fda5a3-ecdd-4ef2-b6e5-da0906db9c71.mp4
