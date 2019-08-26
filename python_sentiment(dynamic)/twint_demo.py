import twint
from textblob import TextBlob
# Configure
def scraper(tag):

    c = twint.Config()
    # c.Username = " "
    c.Search = '#{}'.format(tag)
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
    c.Output = "twitter{}".format(tag)
    twint.run.Search(c)
# scraper('icc')    
