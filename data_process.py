'''
Preprocess the data for later calculation and data visualization.
'''

import numpy
import pandas
import os
import pandas
import re
import nltk
import wordcloud
import langdetect

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets') 
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from gensim import corpora, models
from langdetect import detect
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from datetime import datetime as dt


def read_data(csv):
    '''
    Read csv file into pandas dataframe
    
    Inputs:
      two csv files

    Outputs:
      df1: dataframe consists of data crawled from twitter api
      df2: dataframe consists of existed data
    '''
    
    df1 = pandas.read_csv('/Users/hejielu/Desktop/final/metootweets_api.csv',\
                          usecols=[0,2], names=['dateoftweet','text'], 
                          skiprows=1)
    df2 = pandas.read_csv('/Users/hejielu/Desktop/final/metootweets.csv', 
                          usecols=[6,7])
    
    return df1,df2


def preprocess(df):
    '''
    Preprocess the tweet data
    
    Inputs:
      dataframe

    Outputs:
      a cleaned dataframe
    '''
    for row in df.itertuples():
        #format the 'dateoftweet' column value into mm/dd/yyyy
        if len(str(row[1])) > 20:
            temp_month = str(row[1])[4:7]
            date = str(row[1])[8:10]
            year = str(row[1])[26:30]
            months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', \
                      'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', \
                      'Sept': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
            month = ''
            for key,value in months.items():
                if temp_month == key:
                    month = value
            dt = str(month) + '/' + date + '/' + year
        else:
            dt = str(row[1])[5:7] + '/' + str(row[1])[8:10] + '/' + \
            str(row[1])[0:4]
        df.at[row.Index, 'dateoftweet'] = dt
            
        #use regular expression in 'text' column
        txt = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",\
        str(row[2]))
        p = re.compile(r'\<http.+?\>', re.DOTALL)
        txt = re.sub(p, '', txt)
        txt = txt.lower()
        txt = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ", txt)
        txt = re.sub("(\\d|\\W)+"," ",txt)
        txt = re.sub('rt', '', txt)
        txt = re.sub('amp', '', txt)
        txt = txt.split()
        lemm = WordNetLemmatizer()
        txt = [lemm.lemmatize(word) for word in txt if not word in STOPWORDS] 
        txt = " ".join(txt)
        df.at[row.Index, 'text'] = txt
    return df

    
def merge(df1,df2):
    '''
    Merge two dataframe
    
    Inputs:
      df1: dataframe consists of existed data
      df2: dataframe consists of data crawled from twitter api

    Outputs:
      a cleaned dataframe
    '''
    df1_cleaned = preprocess(df1)
    df2_cleaned = preprocess(df2)
    df_total = pandas.concat([df2_cleaned, df1_cleaned], axis=0, \
        ignore_index=True)
    df_total.replace('', np.nan, inplace=True)
    for row in df_total.itertuples(index=False):
        if detect(str(row[1])) != 'en':
            df_total['text'].replace(row[1], np.nan, inplace=True)
    df_total.drop_duplicates(subset='text', keep="first")
    df_total.dropna(how='all', subset=['text'], inplace=True)
    return df_total


def get_csv(df1,df2):
    '''
    Read dataframe as a csv file
    '''
    df_total = merge(df1, df2)
    df_total.to_csv('/Users/hejielu/Desktop/data.csv', encoding='utf-8')


