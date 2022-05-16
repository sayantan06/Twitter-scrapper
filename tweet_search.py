import tweepy as tw
import pandas as p
# import configparser
from nltk.tokenize import word_tokenize

#config = configparser.ConfigParser()
#config.read('configkeys.ini')

auth = tw.OAuthHandler('2JETAdAD5DDUnCpacvDI5GTgk','5SaPWrWb0xfEDeFHmjVPRdGHzJ41h7iSvrTf0TEu8KtWufrVeN')
auth.set_access_token('1518976185631657984-rqTrxoHRkjj3TxyxggBBTKeNHeALIS','nd1vXE5LrHFJqwKL62qtG719ZaQwzcUGUYXJxm93Mzyaw')
api = tw.API(auth)

tweets = tw.Cursor(api.search_tweets, q = '#NFTgiveaways -filter:retweets -filter:replies -is:quotetweet', tweet_mode = 'recent', result_type = 'recent', lang = 'en',count = 130).items(500)

def likes(tweets): 
    if 'Like' in tweets:
        return 1
    elif 'LIKE' in tweets:
        return 1
    elif 'like' in tweets:
        return 1
    elif '❤️' in tweets:
        return 1
    return 0

def follow(tweets):
    if 'follow' in tweets:
        return tweets.index('follow')
    elif 'Follow' in tweets:
        return tweets.index('Follow')
    elif 'FOLLOW' in tweets:
        return tweets.index('FOLLOW')
    return 0

def follow_user(index, tweet):
    if tweet[index+1].lower() == 'me':
        return '2'
    if tweet[index+1].startswith('@') == False:
        return '1'
    users = []
    for t in range(index,len(tweet)):
        if tweet[t].startswith('@') and tweet[t+1] not in users:
            users.append('@'+tweet[t+1])
    return users 

# def f_user(index,tweet):
#     users = []
#     if tweet[index+1].lower() == 'me':
#         users.append('2')
#     if tweet[index+1].startswith('@') == False:
#         return '1'


def retweet(tweets):
    if 'retweet' in tweets:
        return 1
    elif 'Retweet' in tweets:
        return 1
    elif 'RETWEET' in tweets:
        return 1
    elif 'RT' in tweets:
        return 1
    elif 'Rt' in tweets:
        return 1
    elif 'rt' in tweets:
        return 1
    elif '🔁' in tweets:
        return 1
    return 0

def find(word,t):
        if (t[t.index(word)+1]).isnumeric():
            return 'Tag {} people'.format(t[t.index(word)+1])
        return 'Tag people'

def tag(tweet):
        if 'tag' in tweet:
            return find('tag',tweet)
        elif 'Tag' in tweet:
            return find('Tag',tweet)
        return 0

columns = ['User','Hashtags','Like','Retweet','Follow','Tag','Link','Time']
data = []
for tweet in tweets:
    hashtags = []
    try:
        for hashtag in tweet.entities['hashtags']:
          hashtags.append(hashtag['text'])
    except:
        pass
    tweet_tokens = word_tokenize(tweet.text)
    follows = follow(tweet_tokens)
    users = '0'
    if follows:
        users = follow_user(follows,tweet_tokens)
        if users == '2' or users == '1':
            users ='@'+tweet.user.screen_name
    try:
        ','.join(users)
    except:
        pass
            
    #entering data 
    data.append([tweet.user.screen_name,
                ','.join(['#'+h for h in hashtags]),
                likes(tweet_tokens),
                retweet(tweet_tokens),
                users,
                tag(tweet_tokens),
                "https://twitter.com/twitter/statuses/"+str(tweet.id),
                tweet.created_at])
    

dataframe = p.DataFrame(data, columns= columns)
dataframe.to_csv('tweet1_data.csv')
    
import csv, mysql.connector

mydb = mysql.connector.connect(host = 'localhost', user = 'root', password ='', database = 'twitter')

cursor = mydb.cursor()
csv_data=csv.reader(open('tweet1_data.csv',encoding='utf8'))
for d in csv_data:
    cursor.execute('insert into twitter_data(users,Hashtags,likes,Retweet,Follow,Tag,Link,time) values(%s,%s,%s,%s,%s,%s,%s,%s)',d)

mydb.commit()
cursor.close()
