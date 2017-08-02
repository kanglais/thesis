import test_hashtag_bias_bubble
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

def create_and_test_user_bias_matrix(input_data_file):

	with open(input_data_file, 'rb') as raw_url_data:

		all_users_full_tweets_dict = json.load(raw_url_data)
	#list of all the user id's 
	user_ids = list(all_users_full_tweets_dict.keys())

	#break raw tweet dictionary into series of lists containing relevant info 
	#based on user ids (so order remains the same)

	created_at_list = []
	reply_to_sn_list = []
	hashtags_list = []
	url_full_list = []
	user_mentions_full_list = []
	user_id_list = []
	user_sn_list = []

	count = 0

	for user in user_ids:
		user_id_list.append(user)
		
		for doc in all_users_full_tweets_dict[user]:
			created_at_list.append(doc['created_at'])
			
			user_sn_list.append(doc['user']['screen_name'])

			reply_to_sn_list.append(doc['in_reply_to_screen_name'])

			hashtags_list.append(doc['entities']['hashtags'])

			url_full_list.append(doc['entities']['urls'])

			user_mentions_full_list.append(doc['entities']['user_mentions'])
			
			count+=1

	#create two lists, one of users who use urls as sources and one of users who don't use any urls
	non_url_users = []

	url_users = []

	#create dict with only expanded_url and user id
	expanded_url_dict_with_user = {}

	i = 0

	for item in url_full_list:
		if item == []:
			non_url_users.append(user_id_list[i])
		else:
			url_users.append(user_id_list[i])        
			for url in item:   
				expanded_url_dict_with_user.update({user_id_list[i] : [url['expanded_url']]})
		i+=1

	#create matrix using url dict
	bias_matrix = create_bias_matrix(expanded_url_dict_with_user, news_sources)

	# cooc_diag = diagonal_cooc_matrix(cooc_matrix)
	bias_number_user = pew_bias_matrix(bias_matrix)
	users_and_biases = user_ids_user_bias(url_users, bias_number_user)

	#determine bias based on positive or negative results
	liberal_users = []
	conservative_users = []
	neutral_users = []

	for user in users_and_biases:
		if user[1] > 0.3:
			conservative_users.append(user[0])
		elif user[1] < -0.3:
			liberal_users.append(user[0])
		else:
			neutral_users.append(user[0])
			
	print(len(conservative_users))
	print(len(liberal_users))
	print(len(neutral_users))


	liberal_tags = test_hashtag_bias_bubble.define_hashtag_bias(user_hash_dict, liberal_users)
	conservative_tags = test_hashtag_bias_bubble.define_hashtag_bias(user_hash_dict, conservative_users)
	neutral_tags = test_hashtag_bias_bubble.define_hashtag_bias(user_hash_dict, neutral_users)
	non_url_tags = test_hashtag_bias_bubble.define_hashtag_bias(user_hash_dict, non_url_users)

	print(len(liberal_tags))


def create_retweet_user_dict(user_id_list, reply_to_sn_dict, all_users_full_tweets_dict):
	#create a dict with reply_to screen names and user id's 
	#users that tweeted at other users

	count = 0

	reply_to_sn_dict = {}

	for user in user_id_list:
		
		if user not in reply_to_sn_dict:
			reply_to_sn_dict[user] = []
		
		for doc in all_users_full_tweets_dict[user]:
			reply_to_sn_dict[user].append(doc['in_reply_to_screen_name'])

	return reply_to_sn_dict

def create_hashtag_user_dict(user_id_list, all_users_full_tweets_dict):
	#create dict with user ids and full data of hashtags (includes indices, etc.)
	#note- should this be expanded to include mentions?

	hash_dict_with_user = {}

	i = 0

	for user in user_id_list:
		
		for doc in all_users_full_tweets_dict[user]:
			
			hash_dict_with_user.update({user : doc['entities']['hashtags']})


	#create cleaner dict with user ids and only text of hashtags as list 

	user_hash_dict = {}

	for user in hash_dict_with_user:
		
		if user not in user_hash_dict:
			user_hash_dict[user] = []
		
		for item in hash_dict_with_user[user]:        
			user_hash_dict[user].append(item['text'])

	return user_hash_dict	

#create cooccurence matrix 
def create_cooc_matrix(data, standardize = False):
	cooc_m = np.zeros((data.shape[1], data.shape[1]))
	for i, c1 in enumerate(data.T):
		for j, c2 in enumerate(data.T):
			cooc_m[i,j] = np.sum(c1*c2)
	if standardize:
		return cooc_m / data.shape[0]
	return cooc_m

def diagonal_cooc_matrix(matrix):

	new_matrix = (matrix/np.diagonal(matrix)).T

# create matrix of user bias using pew results:
def create_bias_matrix(expanded_url_dict_with_user, news_sources):
	bias_value_return_list = []
	user_sources = []
	
	count = 0

	for user_id in expanded_url_dict_with_user:

		sources = []

		#to create array of zeros:
		user_zero_vector_bias = list(np.zeros(len(news_sources)))
		
		# what sources *did* this user use        
		url_item = expanded_url_dict_with_user[user_id]
		for item in url_item:
			o = urlparse(item)
			root_url = o.hostname
			sources.append(root_url)
			root_url_split = root_url.split(".")
			
			if root_url_split[0] == "www":
				user_sources.append(root_url_split[1])
			else:
				user_sources.append(root_url_split[0])
									  
		for i, source in enumerate(news_sources):            
			#user_zero_vector_bias[i] = user_sources.count(source)
			if source in root_url_split:
				user_zero_vector_bias[i]+=1
			
		bias_value_return_list.append(user_zero_vector_bias)
		count +=1
		
	bias_value_return_list = np.array(bias_value_return_list)

	return bias_value_return_list

def pew_bias_matrix(bias_matrix):

	#multiply results by bias measure from pew
	user_bias_measure_pew = []

	for user in bias_matrix:
		user_bias_measure_pew.append(user*bias)

	# transform to matrix
	user_bias_measure_pew = np.array(user_bias_measure_pew)

	# transpose of matrix 
	user_bias_measure_pew = user_bias_measure_pew.T

	#sum columns (users) of matrix 
	i = 0

	while i < len(user_bias_measure_pew):
		
		bias_number_user = list(sum(user_bias_measure_pew))
		i+=1

	return(bias_number_user)

def user_ids_user_bias(url_users, bias_number_user):

	#associate user ID's with user bias again
	users_and_biases =[[str(u),b] for u,b in zip(url_users,bias_number_user)]

	return users_and_biases

def main():

	# define input data file
	input_data_file = '/Users/Kellie/Desktop/sep_tweets.json'
	
	# generate data structure
	create_and_test_user_bias_matrix(input_data_file)

if __name__ == "__main__":
	main()