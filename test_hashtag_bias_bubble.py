import test_user_bias_bubble
import numpy as np 
import json
from collections import defaultdict
from urllib.parse import urlparse
from collections import Counter
import pprint
import pandas as pd

#bias, according to pew research center
bias = np.array([0.6, 0.6, 0.6, 0.6, 0.6, 0.5, 0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2, -0.2, -0.3,
        -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.6, -0.6])

#news sources as defined by pew research center
news_sources = np.array(['breitbart', 'limbaugh', 'theblaze', 'hannity', 'glenbeck', 'drudgereport', 'fox',
                'wallstreetjournal', 'yahoo', 'usatoday', 'abc', 'bloomberg', 'google', 'cbs', 'nbc',
                'cnn', 'msnbc', 'buzzfeed', 'pbs', 'bbc', 'huffingtonpost', 'washingtonpost', 'economist', 'politico',
                'dailyshow', 'guardian', 'aljazeera', 'npr', 'colbertreport', 'nytimes', 'slate', 'newyorker'])


#determine which hashtags are more common with which biases
def define_hashtag_bias(user_hash_dict, user_list_biased):
    bias_tags = []
    all_tags = []

    for user in user_hash_dict:
        all_tags.append(user_hash_dict[user])

        if user in user_list_biased:
            bias_tags.append(user_hash_dict[user])
    return bias_tags

liberal_tags = define_hashtag_bias(user_hash_dict, liberal_users)
conservative_tags = define_hashtag_bias(user_hash_dict, conservative_users)
neutral_tags = define_hashtag_bias(user_hash_dict, neutral_users)
non_url_tags = define_hashtag_bias(user_hash_dict, non_url_users)

#create list of unique hashtags
def unique_tags(tag_list):
    unique = []

    for tag in tag_list:
        for item in tag:
            unique.append(item)

    unique = set(unique)
    return unique

liberal_unique = unique_tags(liberal_tags)
conservative_unique = unique_tags(conservative_tags)
neutral_unique = unique_tags(neutral_unique)

#associate screen names and user id's with bias
ids_and_sn =[[str(u),sn] for u,sn in zip(user_id_list,user_sn_list)]


#define users according to their potential bias based on tweeted sources
def potential_bias(ids_and_sn, user_list):
    screen_names = []

    for i, u in ids_and_sn:
        if i in user_list:
            screen_names.append(u)
    return screen_names

conservative_screen_names = potential_bias(ids_and_sn, conservative_users)
liberal_screen_names = potential_bias(ids_and_sn, liberal_users)
neutral_screen_names = potential_bias(ids_and_sn, neutral_users)
non_url_user_screen_names = potential_bias(ids_and_sn, non_url_users)


#see which non-url using users retweeted which biased users
#define potential bias of non_url users
def potential_bias_based_on_retweets(reply_to_sn_dict, non_url_users, screen_name_list):
    retweet_bias = []

    for user in reply_to_sn_dict:
        if user in non_url_users:
            rt = reply_to_sn_dict[user]
            for text in rt:
                if text in screen_name_list:
                    retweet_bias.append(user)

maybe_conservative_retweet_bias = potential_bias_based_on_retweets(reply_to_sn_dict, non_url_users, conservative_screen_names)
maybe_liberal_retweet_bias = potential_bias_based_on_retweets(reply_to_sn_dict, non_url_users, liberal_screen_names)
maybe_neutral_retweet_bias = potential_bias_based_on_retweets(reply_to_sn_dict, non_url_users, neutral_screen_names)

#see what hashtags non_url users are using
def non_url_user_hash(user_hash_dict, non_url_users, unique_hash_list):
    hash_users = []

    for user in user_hash_dict:
        if user in non_url_users:
            for text in user_hash_dict[user]:
                if text in unique_hash_list:
                    hash_users.append(user)
    return hash_users

liberal_hash_users = non_url_user_hash(user_hash_dict, non_url_users, liberal_unique)
conservative_hash_users = non_url_user_hash(user_hash_dict, non_url_users, conservative_unique)
neutral_hash_users = non_url_user_hash(user_hash_dict, non_url_users, neutral_unique)
unknown_hash = []
uncertain_users = []

#match hashtag bias with sources bias and try to confirm source bias- are they the same?
liberal_positive_results = []
conservative_positive_results = []
neutral_positive_results = []

liberal_negative_results = []
conservative_negative_results = []
neutral_negative_results = []

for user in liberal_hash_users:
    if user in maybe_liberal_retweet_bias:
        liberal_positive_results.append(user)
    else:
        liberal_negative_results.append(user)


for user in conservative_hash_users:
    if user in maybe_conservative_retweet_bias:
        conservative_positive_results.append(user)
    else:
        conservative_negative_results.append(user)

for user in neutral_hash_users:
    if user in maybe_neutral_retweet_bias:
        neutral_positive_results.append(user)
    else:
        neutral_negative_results.append(user)

# def check_results(user_with_bias, user_maybe):
# 	positive_results = []
# 	negative_results = []

# 	for user in user_with_bias:
# 		if user in user_maybe:
# 			positive_results.append(user)
# 		else:
# 			negative_results.append(user)
# 	#check code can probs do this in one line 

print(len(liberal_positive_results))
print(len(conservative_positive_results))
print(len(neutral_positive_results))

print(len(liberal_negative_results))
print(len(conservative_negative_results))
print(len(neutral_negative_results))

print(len(uncertain_users))

def main():

    # define input data file
    input_data_file = '/Users/Kellie/Desktop/sep_tweets.json'
    
    # import user bias from test_user_bias_bubble
    test_user_bias_bubble.create_and_test_user_bias_matrix(input_data_file)

if __name__ == "__main__":
    main()