'''
Basic_algorithm to calculate the tf-idf, draw a word cloud and plot a frequency 
table.
'''

import numpy as np 
import pandas as pd
import re
import nltk
import wordcloud
import math
from sklearn.feature_extraction.text import CountVectorizer
from gensim import corpora
from wordcloud import WordCloud
from os import path
from PIL import Image
import matplotlib.pyplot as plt
import datetime


def main(csv, start_date, end_date, n=25):
    '''
    Main function that plot graphs

    Inputs:
      csv: a csv file that contains data
      date: the date that a user want to search
      n: number of most frequent words to plot
    '''
    df = pd.read_csv(csv, dtype={'dateoftweet': str})
    df.dropna()
    text_lst = preprocess(df, start_date, end_date)
    tf_idf_dict = cal_tf_idf(text_lst)
    plot_wordcloud(tf_idf_dict)
    plot_top_n_word(text_lst, n)


def preprocess(df, start_date, end_date):
    '''
    Preprocess the data to a list of texts of specific dates

    Inputs:
      df: a dataframe
      date: the date that a user want to search

    Output:
      text_lst: a list of text
    '''
    text_lst = []
    format_str = '%m/%d/%Y'
    '''
    for row in df.itertuples(index=False):
        try:
            date = datetime.datetime.strptime(row[0], format_str)
            text = row[1]
            if date >= start_date and date <= end_date:
                text_lst.append([text])
        except:
            continue
    '''
    for row in df.itertuples(index=False):
        date = datetime.datetime.strptime(row[0], format_str)
        text = row[1]
        if date >= start_date and date <= end_date:
            text_lst.append([text])
            
    return text_lst


def sort_text(text):
    '''
    Count the frequency of words in a string of text

    Input：
      text: a string of text

    Output:
     sorted_lst: a list of tuples with words and their frequencies
    '''
    word_split = text.split()
    freq = {}
    for word in word_split:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    token = list(freq.items())
    sorted_lst = list(sorted(token, key=cmp_to_key(cmp_count_tuples)))

    return sorted_lst


def cal_tf_idf(docs):
    '''
    Calculate the term frequency–inverse document frequency

    Inputs:
        docs: (list of lists of strings) the collection of documents

    Returns:
        term_tf_idf: a dictionary that maps a string to its tf-idf score
    '''
    term_tf_idf = {}
    for doc in docs:
        count_list = sort_text(doc[0])
        for (term, count) in count_list:
            tf = 0.5 + 0.5 * (count / count_list[0][1])
            term_freq = 0

            if term in doc[0]:
                term_freq += 1

            idf = math.log(len(docs) / term_freq)
            tf_idf = tf * idf
            new_value = {term: tf_idf}
            term_tf_idf.update(new_value)

    return term_tf_idf


def cmp_to_key(mycmp):
    '''
    Convert a cmp= function into a key= function
    From: https://docs.python.org/3/howto/sorting.html
    '''

    class CmpFn:
        '''
        Compare function class.
        '''
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return CmpFn


def cmp_count_tuples(t0, t1):
    '''
    Compare pairs using the second value as the primary key and the
    first value as the secondary key.  Order the primary key in
    non-increasing order and the secondary key in non-decreasing
    order.

    Inputs:
        t0: pair
        t1: pair

    Returns: -1, 0, 1
    '''
    (key0, val0) = t0
    (key1, val1) = t1
    if val0 > val1:
        return -1

    if val0 < val1:
        return 1

    if key0 < key1:
        return -1

    if key0 > key1:
        return 1

    return 0


def plot_wordcloud(dict):
    '''
    Plot the word cloud according to tf-idf score and save it into a png file

    Input:
      dict: a dictionary that takes a string of tweet as the key and
            its tf-idf score as value
    '''
    twitter_mask = np.array(Image.open("twitter_mask.png"))
    wc = WordCloud(background_color="white", mask=twitter_mask,
                   width=1600, height=800).fit_words(dict)
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad=0)
    wc.to_file("wordcloud.png")


def find_top_words(text_lst, n):
    '''
    Find the top n words from all the tweets with frequencies

    Inputs:
      text_lst: a list of strings that contains all the tweets
      n: top n words

    Output:
      words_freq: a list of tuples with words and frequencies
    '''
    lst = []
    for text in text_lst:
        lst.append(text[0])
    vec = CountVectorizer().fit(lst)
    words_bag = vec.transform(lst)
    sum_words = words_bag.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)[:n]

    return words_freq


def plot_top_n_word(text_lst, n):
    '''
    Plot the histograms of top n words with their frequencies

    Inputs:
      text_lst: a list of strings that contains all the tweets
      n: top n words
    '''
    top_words = find_top_words(text_lst, n)
    top_df = pd.DataFrame(top_words)
    top_df.columns = ["Word", "Frequency"]
    ax = top_df.plot.bar(x='Word', y='Frequency', rot=0, figsize=(15,8))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
    ax.figure.savefig('frequency_plot.png')
    plot_df_table(top_df, header_columns=0, col_width=2.0)


def plot_df_table(data, col_width=3.0, row_height=0.625, font_size=14,
                  header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                  bbox=[0, 0, 1, 1], header_columns=0,
                  ax=None, **kwargs):
    '''
    Convert a data frame to a png
    '''
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        _, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    ax.figure.savefig('top_n_dataframe.png')

