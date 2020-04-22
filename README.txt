CS 122 W’20 Final Project:

README.txt: This file 

data_process.py: Data cleaning

basic_algorithm.py: Text Analysis

find_tweets.py: Twitter crawling process using the Tweepy api

metoo_gui.py: User interface using Tkinter, where users can explore what words people 
              used on Twitter during the MeToo movement
            
twitter_mask: A png that used for the word cloud mask

cleandata.csv: Preprocessed dataset(contains 89,109 rows)

metootweets.csv: Approximately 350,000 row tweet data downloaded from data.world(https://data.world/rdeeds/350k-metoo-tweets)

metootweets_api.csv:13,487 row tweet data crawled from Twitter API




Instructions:
In the terminal, run the python file named metoo_gui. There will be a user interface. 
Users can enter the date they would like to search and different plots associated with 
the dates will be displayed.

i.e. $python3 metoo_gui.py
     

Note that all the data has been process in advanced (cleandata.csv) because the API is 
not stable and need to crawl the data in advanced. The metoo_gui.py could be used with 
any kind of data set with date and text of the Tweets.

Libraries required:
boto3==1.12.22
botocore==1.15.22
cachetools==4.0.0
certifi==2019.11.28
chardet==3.0.4
cycler==0.10.0
docutils==0.15.2
gensim==3.8.1
google-api-core==1.16.0
google-auth==1.11.3
google-cloud-core==1.3.0
google-cloud-storage==1.26.0
google-resumable-media==0.5.0
googleapis-common-protos==1.51.0
idna==2.9
jmespath==0.9.5
joblib==0.14.1
kiwisolver==1.1.0
matplotlib==3.2.0
nltk==3.4.5
numpy==1.18.1
pandas==1.0.2
Pillow==7.0.0
protobuf==3.11.3
pyasn1==0.4.8
pyasn1-modules==0.2.8
pyparsing==2.4.6
python-dateutil==2.8.1
pytz==2019.3
requests==2.23.0
rsa==4.0
s3transfer==0.3.3
scikit-learn==0.22.2.post1
scipy==1.4.1
six==1.14.0
sklearn==0.0
smart-open==1.10.0
urllib3==1.25.8
wordcloud==1.6.0
sudo apt-get install python3-pil.imagetk



