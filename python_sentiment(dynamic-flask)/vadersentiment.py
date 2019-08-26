import time
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def vader_sent(tag):
    sid = SentimentIntensityAnalyzer()

    sentiment_summary = dict()
    result=[]
    start_time=time.time()
    count=0
    comp=0
    pos=0
    neg=0
    neu=0


    with open('twitter{}/tweets.csv'.format(tag),'r',encoding='utf8') as file:

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