from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator 
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np
# import vadersentiment

def cloud(tag,com,neg,pos,neu):

    sid = SentimentIntensityAnalyzer()
    stopwords = set(STOPWORDS) 
    dset=[]
    pos_word_list=[]
    pos_words=''
    neu_word_list=[]
    neu_words=''
    neg_word_list=[]
    neg_words=''
    f=open("twitter{}/tweet_tokens.txt".format(tag),"r")
    for word in f.read().split('\n'):
        # print (word.split('\n'))
        # print(type(word))
        # exit()

        # dset.append(word)
        if (sid.polarity_scores(word)['compound']) >= 0.05:
            pos_word_list.append(word)
            # print(sid.polarity_scores(word)['compound'])
        elif (sid.polarity_scores(word)['compound']) <= -0.05:
            neg_word_list.append(word)
            # print(sid.polarity_scores(word)['compound'])

        else:
            neu_word_list.append(word)        
            # print(sid.polarity_scores(word)['compound'])
        # exit()
    f.close()           
    for w in pos_word_list:
        pos_words=pos_words + w + ' '
    for w in neg_word_list:
        neg_words=neg_words + w + ' '

    masked = np.array(Image.open("tlogo.png"))

    # print(masked[1])

    # print(type(masked))
    # exit()
        # if val == 242:
        #     return 255
        # else:
        #     return val
    # tmask= np.ndarray((masked.shape[0],masked.shape[1]), np.int32)

    # for i in range(len(masked)):
    #     tmask[i] = list(map(transform_format, masked[i]))
    # print(tmask)
    # exit()
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
    # plt.close()
    # plt.ion()            

    plt.figure(figsize = (10, 8), facecolor = 'grey',edgecolor='blue') 
    plt.imshow(negativecloud.recolor(color_func=image_colors),interpolation='bilinear') 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.show()     
    plt.pause(15)
    plt.close()
