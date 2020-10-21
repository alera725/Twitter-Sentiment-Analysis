#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:25:38 2019

@author: Alejandro Ramos
"""

import tweepy #The Twitter API
from tkinter import * #For the GUI
from time import sleep
from datetime import datetime
from textblob import TextBlob #For Sentiment Analysis
import matplotlib.pyplot as plt #For Graphing the Data
import pandas as pd

#%% Codigos de autorizacion
consumer_key = 'XXXX'
consumer_secret = 'XXXX'
access_token = 'XXXX'
access_token_secret = 'XXXX'

#%% Abrir conexion con la API de tweeter
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

user = api.me()
print (user.name)

#Data
keyword = "China" # Word we want analyze
numberOfTweets = 500 # Last number of tweets we want to take
polarity_list = []
numbers_list = []
number = 1

for tweet in tweepy.Cursor(api.search, keyword, lang="en").items(numberOfTweets): #Lan is Language of tweets
    try:
        analysis = TextBlob(tweet.text)
        analysis = analysis.sentiment
        polarity = analysis.polarity
        polarity_list.append(polarity)
        numbers_list.append(number)
        number = number + 1

    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break

num_pd = pd.DataFrame(numbers_list)


#%% Graficar
axes = plt.gca()
axes.set_ylim([-1, 2])
plt.scatter(numbers_list, polarity_list)
averagePolarity = (sum(polarity_list))/(len(polarity_list))
averagePolarity = "{0:.0f}%".format(averagePolarity * 100)
time  = datetime.now().strftime("At: %H:%M\nOn: %m-%d-%y")
plt.text(0, 1.25, "Average Sentiment:  " + str(averagePolarity) + "\n" + time, fontsize=12, bbox = dict(facecolor='none', edgecolor='black', boxstyle='square, pad = 1'))
plt.title("Sentiment of " + keyword + " on Twitter") 
plt.xlabel("Number of Tweets")
plt.ylabel("Sentiment")
plt.show()




