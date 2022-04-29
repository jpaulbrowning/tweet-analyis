# Import functions.
import tweepy as tw
import pandas as pd

# Authenticate
my_api_key = "<Insert API key here>"
my_api_secret = "<Insert API secret here>"
auth = tw.OAuthHandler(my_api_key, my_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define function to retrieve replies (not original tweet)
def get_tweet_thread(user_id,tweet_id):
    replies = tw.Cursor(api.search_tweets, q='to:{}'.format(user_id), since_id=tweet_id, tweet_mode='extended').items()

    agg_replies = []
    for reply in replies:
        if(reply._json['in_reply_to_status_id_str'] == tweet_id):
             agg_replies.append(reply._json['full_text'])  
    return(agg_replies)

# Retrieve replies to specified original tweet.
user_id = 'cant_b'
tweet_id = '1518582614596145154'
responses = pd.DataFrame(get_tweet_thread(user_id, tweet_id), columns=['raw_tweet'])

# Clean the data.

# By default, replies reference original username; we want to remove that.
responses['raw_tweet'] = responses['raw_tweet'].str.replace('@'+user_id+' ','')
responses[['Q1','Q2','Q3','Q4','Misc']] = responses['raw_tweet'].str.split('\n', 4, expand=True)


#Output to CSV.
responses.to_csv('/hied-tweets.csv')
