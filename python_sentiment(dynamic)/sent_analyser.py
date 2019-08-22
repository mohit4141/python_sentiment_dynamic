import twint
from textblob import TextBlob
import time
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator 
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np
import re
# import enchant
import twint_demo #import scraper
import preprocessor
import vadersentiment
import wcloud

hashtag=input("Please enter the topic you want to search for: ")
twint_demo.scraper(hashtag)
preprocessor.prepper(hashtag)
vadersentiment.vader_sent(hashtag)
wcloud.cloud(hashtag)