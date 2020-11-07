import tweepy
import json
from config import consumer_key
from config import consumer_secret
from config import access_secret
from config import access_token
from tweepy.streaming import StreamListener
class MyTweetListener(StreamListener):

    def __init__(self):
        self.number_of_teams = int(input("How many Teams will be participating? "))
        while type(self.number_of_teams) != int:
            self.number_of_teams = int(input("Please type an integer: "))
        
        self.team_hashtag_dict = dict()
        for i in range(self.number_of_teams):
            unconfirmed_hashtag = input(f"Enter the team {i + 1}'s hashtag: ")
            answer = input(f"Confirm that is the hashtag you would like for team {i + 1} with Y/N: ")
            while answer.lower() != 'y':
                unconfirmed_hashtag = input(f"Please enter another hashtag for team {i + 1}: ")
                answer = input(f"Confirm that is the hashtag you would like for team {i + 1} with Y/N: ")
                if answer.lower() == 'y' or answer.lower() == 'yes':
                    break
            self.team_hashtag_dict[i] = unconfirmed_hashtag
            
        
        self.team_tweet_count_dict = {i:0 for i in range(self.number_of_teams)}
    
    def on_data(self, data):
        
        twitter_json = json.loads(data)

        print(twitter_json["user"]["name"])
        print(twitter_json["text"])
        for team, hashtag in self.team_hashtag_dict.items():
            if "extended_tweet" in twitter_json: #and "hashtags" in twitter_json["extended_tweet"]

                if hashtag in twitter_json["extended_tweet"]["full_text"]:
                    self.team_tweet_count_dict[team] += 1
                    print(self.team_tweet_count_dict)

                
        return True
    
    def on_error(self, status):
        print("Error status:", status)



if __name__ == "__main__":
    listener = MyTweetListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    strem = tweepy.Stream(auth, listener)
    strem.filter(track=[el for el in listener.team_hashtag_dict.values()])

    print("You're all set. Filtering tweets now!!")