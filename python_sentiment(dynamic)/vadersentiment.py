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


    with open('twitter{}/tweets.csv'.format(tag),'r',encoding='utf8') as file:
        # f=open("tweet_tokens.txt","r")

        for line in file:
            # i+=1
            score = sid.polarity_scores(line)
            # print(type(score))
            comp+=score['compound']
            # print("{:-<40} {}".format(line, str(score)))
            # print(str(result))

        
            count+=1
        



        # f.close()
    # sentiment=''
    comp/=count
    if(comp>=0.05):    
        print("The overall sentiment of the topic is POSITIVE with a compound value of: ",comp)
    elif(comp>-0.05 and comp<0.05):
        print("The overall sentiment of the topic is NEUTRAL with a compound value of: ",comp)
    else:
        print("The overall sentiment of the topic is NEGATIVE with a compound value of: ",comp)
    print("The execution time is: {} seconds ".format(time.time()-start_time))