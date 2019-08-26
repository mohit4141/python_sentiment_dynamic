# python_sentiment_dynamic
python_sentiment_dynamic-flask-->
replace the run.py file in your twint library to use twint inside flask.

#changes made to run.py
# get_event_loop().run_until_complete(Twint(config).main(callback))  --> line 213 in original run.py
   #replace with following:
    loop = new_event_loop()
    set_event_loop(loop)
    loop.run_until_complete(Twint(config).main(callback))
