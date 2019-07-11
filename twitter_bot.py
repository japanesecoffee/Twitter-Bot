import tweepy

print("testing bot")

#assigning Twitter keys to variables
CONSUMER_KEY = "CbQBaHTweTSxOb2ss0pyx3am4"
CONSUMER_SECRET = "wFhobn6SRuXl052vtBbr0KWsOJ8LjMPXHVLRbHfFFT3gCZZx4b"
ACCESS_KEY = "1148796843553435651-fiIeADuxfmJlpMEtDVJs0NmT1XhGUI"
ACCESS_SECRET = "zvGVdz1CHOv27PKvI99HE2vml8NYH2N4h0BMSiZNbowpa"

#using api object to communicate with Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)#mentions_timeline() returns a list of 20 most recent mentions
mentions = api.mentions_timeline()

for mention in mentions:
    print(str(mention.id) + " - " + mention.text)
    if "@7elevenroast" in mention.text.lower():
        print("found @ mention")