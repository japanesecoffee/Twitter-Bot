import tweepy
import time
#removed keys and generated new keys in keys.py
#keys.py added to gitignore, so view sample_keys.py to see format
import keys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from googlesearch import search

#using api object to communicate with Twitter
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_KEY, keys.ACCESS_SECRET)
api = tweepy.API(auth)

#this text file stores the id of the last tweet responded to
FILE_NAME = "last_seen_tweet.txt"

def retrieve_last_seen_tweet(file_name):
    f_read = open(file_name, "r")
    last_seen_tweet = int(f_read.read().strip())
    f_read.close()
    return last_seen_tweet

def store_last_seen_tweet(last_seen_id, file_name):
    f_write = open(file_name, "w")
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweet():
    print("retrieving and replying to tweets...")
    last_seen_tweet = retrieve_last_seen_tweet(FILE_NAME)
    #mentions_timeline() returns a list of 20 most recent mentions
    mentions = api.mentions_timeline(last_seen_tweet, tweet_mode="extended")

    #reversing to read old tweets first
    for mention in reversed(mentions):
        print(str(mention.id) + " - " + mention.full_text)
        last_seen_tweet = mention.id
        store_last_seen_tweet(last_seen_tweet, FILE_NAME)
        if "#" in mention.full_text.lower():
            print("found #")
            
            location = get_location(mention.full_text)
            weather = get_weather(location)

            #responding to tweet mention
            api.update_status("@" + mention.user.screen_name +
                              weather,
                              mention.id)

def get_location(tweet):
    #takes tweet and returns only the substring attached to hashtag
    tweet_location = [i.strip("#") for i in tweet.split() if i.startswith("#")][0]
    tweet_location += " today weather.com"
    return tweet_location

def get_weather(query):
    for url in search(query, stop=1):
        print("Result is " + url)

    #this code sends a request and reads the webpage enclosed in response to the request
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

    webpage = urlopen(request).read()
    soup = BeautifulSoup(webpage, "html.parser")

    try:
        title = soup.findAll("span", "today-daypart-title")[0].string
        phrase = soup.findAll("span", "today-daypart-wxphrase")[0].string        
    except IndexError as e:
        forecast = (" could not find the weather, check back later")
        print(e)
    else:
        forecast = (" forecast for " + title + " is " + phrase)
        print(forecast)
    
    return forecast
    

#loop to reply every 30 seconds
while True:
    reply_to_tweet()
    time.sleep(30)