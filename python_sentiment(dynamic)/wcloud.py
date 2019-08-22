from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator 
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np

def cloud(tag):

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
        if (sid.polarity_scores(word)['compound']) >= 0.5:
            pos_word_list.append(word)
            # print(sid.polarity_scores(word)['compound'])
        elif (sid.polarity_scores(word)['compound']) <= -0.5:
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
                    background_color ='white', 
                    stopwords = stopwords, 
                    mask=masked,contour_color='red',contour_width=3,
                    min_font_size = 10).generate(neg_words)   
    # plot the WordCloud image  
    image_colors = ImageColorGenerator(masked)              
    plt.figure(figsize = (10, 8), facecolor = 'grey',edgecolor='blue') 
    plt.imshow(positivecloud.recolor(color_func=image_colors),interpolation='bilinear') 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.show()     