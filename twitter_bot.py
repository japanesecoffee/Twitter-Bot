import tweepy
import time

#assigning Twitter keys to variables
CONSUMER_KEY = "CbQBaHTweTSxOb2ss0pyx3am4"
CONSUMER_SECRET = "wFhobn6SRuXl052vtBbr0KWsOJ8LjMPXHVLRbHfFFT3gCZZx4b"
ACCESS_KEY = "1148796843553435651-fiIeADuxfmJlpMEtDVJs0NmT1XhGUI"
ACCESS_SECRET = "zvGVdz1CHOv27PKvI99HE2vml8NYH2N4h0BMSiZNbowpa"

#using api object to communicate with Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
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
        if "@7elevenroast" in mention.full_text.lower():
            print("found @ mention")
            #responding to tweet mention
            api.update_status("@" + mention.user.screen_name +
                              " Come to 7-Eleven to enjoy a nice cup of roasted hot coffee! I'll pay :)",
                              mention.id)

#loop to reply every 60 seconds
while True:
    reply_to_tweet()
    time.sleep(60)