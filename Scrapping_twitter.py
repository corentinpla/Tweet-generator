import snscrape.modules.twitter as sntwitter
import pandas as pd


def get_tweet(twitter_account): #twitter_account : (str) twitter account from which we want to copy tweets
    
    query = "(from:"+twitter_account+") until:2022-02-27 since:2015-01-01"
    print(query)
    tweets = []
    limit = 20000


    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        
        # print(vars(tweet))
        # break
        if len(tweets) == limit:
            break
        else:
            tweets.append([tweet.date, tweet.username, tweet.content])
            
    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
    return(df)