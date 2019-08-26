import sys, os
sys.path.insert(0, os.getcwd()+"/Subdirectory") 
import sent_analyser
import twint_demo
import vadersentiment
import wcloud
import preprocessor
import random1

from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def success():
   return render_template('index.html')

@app.route('/index',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      hashtag = request.form['message']
      # tw=twint_demo.scraper(hashtag)
      # pre=preprocessor.prepper(hashtag)
      # comp1,neg1,pos1,neu1 = vadersentiment.vader_sent(hashtag)
      # clo=wcloud.cloud(hashtag,comp1,neg1,pos1,neu1)
      var = sent_analyser.analyzer(hashtag)
      # print
      
      return render_template('index.html', cloud = var)  
   
     
if __name__ == '__main__':
   app.debug = True

   app.run()