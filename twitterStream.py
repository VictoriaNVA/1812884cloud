import socket
import requests
import requests_oauthlib
import json

# Twitter authentication
ACCESS_KEY = '1037390133073522688-EG9408FQ2A8VWEKOqF9bdmcYrZxH2S'
ACCESS_SECRET = 'pmOUiKeHS1ddkaqVEqSAVm6P3JuhlcwlrBYe1XKxkakxy'
CONSUMER_KEY = 'YeTT7S9kZPpU2AG5olSNqxgVG'
CONSUMER_SECRET = '5A56GEfzHur6ej8P4xHs8U2o9GUCb1CCkaT4bhuEeu6cmPSmZk'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)


# This method deals with requesting tweets from Twitter API
def get_tweets():
    # Twitter API resource URL for filtering statuses
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    # Query for location from Twitter API (currently San Francisco / New York City but could be changed for anything)
    # and for tracking tweets that include #
    query_data = [('locations', '-122.75,36.8,-121.75,37.8,-74,40,-73,41'), ('track', '#')]
    # Append query to the url and request data
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response


# This method forwards the tweets to Spark via tcp connection
def send_tweets(response, tcp):
    for line in response.iter_lines():
        try:
            # Load tweets as json and retrieve their text
            full_tweet = json.loads(line)
            tweet_text = str(full_tweet['text'])
            print("Tweet Text: " + tweet_text)
            print("------------------------------------------")
            # Send utf-8 encoded tweets to spark
            tcp.send((tweet_text+'\n').encode('utf-8'))
        except:
           pass


# Set host to local and any TCP port
host = 'localhost'
port = 5555
# Set up socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print("Waiting for TCP connection...")
connection, address = s.accept()
print("Connected... Starting getting tweets.")

# When successfully connected, request tweets and send to socket port
resp = get_tweets()
send_tweets(resp, connection)
