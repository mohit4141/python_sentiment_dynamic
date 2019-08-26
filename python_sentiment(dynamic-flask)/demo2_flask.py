
from flask import Flask, redirect, url_for, request, render_template
import time
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator 
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np
import time
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import twint
from textblob import TextBlob

def analyzer(hashtag):
    start_time=time.time()
    # hashtag=input("Please enter the topic you want to search for: ")
    scraper(hashtag)
    prepper(hashtag)
    comp1,neg1,pos1,neu1 = vader_sent(hashtag)
    cloud(hashtag,comp1,neg1,pos1,neu1)
    print("The total execution time is:{}".format(time.time()-start_time))
    if comp1>=0.05:
        return("The sentiment of the topic is POSITIVE")
    if comp1<-0.05:
        return("The sentiment of the topic is NEGATIVE")
    else:
        return("The sentiment of the topic is NEUTRAL")

def scraper(hashtag):

    c = twint.Config()
    # c.Username = " "
    c.Search = '#{}'.format(hashtag)
    c.Limit = 100
    # c.Since = "2019-08-06"
    c.Format = "Tweet id: {id} | Tweet: {tweet}"
    c.Store_object = True
    tweets=[]
    c.Store_object_tweets_list = tweets
    # Run
    c.Store_csv = True
    # CSV Fieldnames
    c.Custom["tweet"] = ["tweet"]
    # Name of the directory
    c.Output = "twitter{}".format(hashtag)
    twint.run.Search(c)

def vader_sent(hashtag):
    sid = SentimentIntensityAnalyzer()

    sentiment_summary = dict()
    result=[]
    start_time=time.time()
    count=0
    comp=0
    pos=0
    neg=0
    neu=0


    with open('twitter{}/tweets.csv'.format(hashtag),'r',encoding='utf8') as file:

        for line in file:
            score = sid.polarity_scores(line)
            comp+=score['compound']
            if score['compound']>=0.05:
                pos+=1
            elif score['compound']<-0.05:
                neg+=1
            else:
                neu+=1

            

        
            count+=1
        



    comp/=count

    if(comp>=0.05):    
        print("The overall sentiment of the topic is POSITIVE with a compound value of: ",comp)
    elif(comp>-0.05 and comp<0.05):
        print("The overall sentiment of the topic is NEUTRAL with a compound value of: ",comp)
    else:
        print("The overall sentiment of the topic is NEGATIVE with a compound value of: ",comp)
    print("The execution time is: {} seconds ".format(time.time()-start_time))

    return comp,neg,pos,neu

def cloud(hashtag,com,neg,pos,neu):

    sid = SentimentIntensityAnalyzer()
    stopwords = set(STOPWORDS) 
    dset=[]
    pos_word_list=[]
    pos_words=''
    neu_word_list=[]
    neu_words=''
    neg_word_list=[]
    neg_words=''
    f=open("twitter{}/tweet_tokens.txt".format(hashtag),"r")
    for word in f.read().split('\n'):

        if (sid.polarity_scores(word)['compound']) >= 0.05:
            pos_word_list.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.05:
            neg_word_list.append(word)

        else:
            neu_word_list.append(word)        
    f.close()           
    for w in pos_word_list:
        pos_words=pos_words + w + ' '
    for w in neg_word_list:
        neg_words=neg_words + w + ' '

    masked = np.array(Image.open("tlogo.png"))

    positivecloud = WordCloud(width = 400, height = 400, 
                    background_color ='black', 
                    stopwords = stopwords,
                    mask=masked,contour_color='blue',contour_width=3, 
                    min_font_size = 10).generate(pos_words) 

    negativecloud = WordCloud(width = 800, height = 800, 
                    background_color ='black', 
                    stopwords = stopwords, 
                    mask=masked,contour_color='red',contour_width=3,
                    min_font_size = 10).generate(neg_words)   
    # plot the WordCloud image  
    image_colors = ImageColorGenerator(masked)  
    plt.ion()    

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Positive', 'Neutral', 'Negative'
    sizes = [pos, neu, neg]
    if max(sizes)==pos:
        explode = (0.03, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    elif max(sizes)== neu:
        explode = (0, 0.03, 0)
    elif max(sizes)==neg:
        explode = (0, 0, 0.03)    
    else:
        explode = (0, 0, 0)    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
    plt.pause(15)

    plt.figure(figsize = (10, 8), facecolor = 'grey',edgecolor='blue') 
    plt.imshow(positivecloud.recolor(color_func=image_colors),interpolation='bilinear') 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.show()     
    plt.pause(15)

    plt.figure(figsize = (10, 8), facecolor = 'grey',edgecolor='blue') 
    plt.imshow(negativecloud.recolor(color_func=image_colors),interpolation='bilinear') 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.show()     
    plt.pause(15)
    # plt.close()

def prepper(hashtag):
    result=[]
    lemmatizer = WordNetLemmatizer() 
    count=0
    start_time=time.time()
    pol=0
    sub=0
    # cloud=[]
    # d = enchant.Dict("en_US")
    with open('twitter{}/tweets.csv'.format(hashtag),'r',encoding='utf8') as file:
        f=open("twitter{}/tweet_tokens.txt".format(hashtag),"w+")

        for line in file:
            # i+=1
            twt = re.sub(r'^https?:\/\/.*[\r\n]*', '', line, flags=re.MULTILINE)
            twt = re.sub(r'^pic.twitter.com*', '', twt, flags=re.MULTILINE)
            twt = ' '.join(re.sub("(@[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)", " ", twt).split()) 
            
            

            twt = twt.lower()
            twt = word_tokenize(twt)
            # print(line)
            result.append(line)
            stop_words = list(set(stopwords.words('english')))
            
            stop_words.extend(["pic","twitter","com"])
            result=[]
            for l in twt :
                if l not in stop_words and len(l)>2:# and d.check(l):
                    l = lemmatizer.lemmatize(l,'v')
                    f.write((l+'\n'))
            count+=1


        f.close()

    print("Execution time is: {}".format(time.time()-start_time))

app = Flask(__name__)

@app.route('/')
def success():
   return render_template('index.html')

@app.route('/index',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      hashtag = request.form['message']
      print(type(hashtag))
      var = analyzer(hashtag)
      return render_template('index.html', cloud = hashtag)  
   
     
if __name__ == '__main__':
   app.debug = True

   app.run()