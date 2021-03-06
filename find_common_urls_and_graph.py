import numpy as np 
import json
from collections import defaultdict
from urllib.parse import urlparse
from collections import Counter
import matplotlib.pyplot as plt


# define input data file
input_data_file = '/Users/Kellie/Desktop/sep_tweets.json'

# load tweet data as an object
with open(input_data_file, 'rb') as tweets:

    # generate python dict from raw json data
    tweet_dict = json.load(tweets)

user_url_hash = {}

for user in tweet_dict:

    if user not in user_url_hash:
        user_url_hash[user] = []

    for item in tweet_dict[user]:
        entities = item['entities']

        user_urls = []

        for url in entities['urls']:
            url_item = url['expanded_url']
            o = urlparse(url_item)
            user_urls.append(o.hostname)

        user_url_hash[user].extend(user_urls)

        user_hash = []
        for tag in entities['hashtags']:
            user_hash.append(tag['text'])

        user_url_hash[user].extend([user_hash])

news_sources = np.array(['breitbart', 'limbaugh', 'theblaze', 'hannity', 'glenbeck', 'drudgereport', 'fox',
                'wallstreetjournal', 'yahoo', 'usatoday', 'abc', 'bloomberg', 'google', 'cbs', 'nbc',
                'cnn', 'msnbc', 'buzzfeed', 'pbs', 'bbc', 'huffingtonpost', 'washingtonpost', 'economist', 'politico',
                'dailyshow', 'guardian', 'aljazeera', 'npr', 'colbertreport', 'nytimes', 'slate', 'newyorker'])


# user_bias = []

# root_urls = []

# for item in big_urls:
#     url_item = item
#     o = urlparse(url_item)
#     root_urls.append(o.hostname)

# #root_urls_without_nonetypes = filter(None, root_urls)

# dict_of_url_counts = {}

# freqs = Counter(root_urls)

# dict_of_url_counts.update(freqs)

# for word in freqs.most_common(10):
#     print(word)

# most_common_urls = (defaultdict(list))

# # print(most_common_urls)
# for word in freqs:
    
#     most_common_urls[word].append(count)
#     for url in most_common_urls: 
#         if 'breitbart' in url: 
#             bias = 0.6
#             most_common_urls[url].append(bias)
#         elif 'limbaugh' in url:
#             bias = 0.6
#             most_common_urls[url].append(bias)
#         elif 'theblaze' in url:
#             bias = 0.6
#             most_common_urls[url].append(bias)
#         elif 'hannity' in url:
#             bias = 0.6
#             most_common_urls[url].append(bias)
#         elif 'glenbeck' in url:
#             bias = 0.6
#             most_common_urls[url].append(bias)
#         elif 'drudge report' in url:
#             bias = 0.5
#             most_common_urls[url].append(bias)
#         elif 'fox' in url: 
#             bias = 0.2
#             most_common_urls[url].append(bias)
#         elif 'wallstreetjournal' in url:
#             bias = -0.1
#             most_common_urls[url].append(bias)
#         elif 'yahoo' in url:
#             bias = -0.1
#             most_common_urls[url].append(bias)
#         elif 'usatoday' in url:
#             bias = -0.1
#             most_common_urls[url].append(bias)
#         elif 'abc' in url:
#             bias = -0.1
#             most_common_urls[url].append(bias)
#         elif 'bloomberg' in url:
#             bias = -0.1
#             most_common_urls[url].append(bias)
#         elif 'google' in url:
#             bias = -0.1
#             most_common_urls[url].append(bias)
#         elif 'cbs' in url:
#             bias = -0.1
#             most_common_urls[url].append(bias)
#         elif 'nbc' in url:
#             bias = -0.2
#             most_common_urls[url].append(bias)
#         elif 'cnn' in url:
#             bias = -0.2
#             most_common_urls[url].append(bias)
#         elif 'msnbc' in url:
#             bias = -0.3
#             most_common_urls[url].append(bias)
#         elif 'buzzfeed' in url:
#             bias = -0.4
#             most_common_urls[url].append(bias)
#         elif 'pbs' in url:
#             bias = -0.4
#             most_common_urls[url].append(bias)
#         elif 'bbc' in url:
#             bias = -0.4
#             most_common_urls[url].append(bias)
#         elif 'huffingtonpost' in url:
#             bias = -0.4
#             most_common_urls[url].append(bias)
#         elif 'washingtonpost' in url:
#             bias = -0.4
#             most_common_urls[url].append(bias)
#         elif 'economist' in url:
#             bias = -0.4
#             most_common_urls[url].append(bias)
#         elif 'politico' in url:
#             bias = -0.4
#             most_common_urls[url].append(bias)
#         elif 'dailyshow' in url: 
#             bias = -0.5
#             most_common_urls[url].append(bias)
#         elif 'guardian' in url: 
#             bias = -0.5
#             most_common_urls[url].append(bias)
#         elif 'aljazeera' in url: 
#             bias = -0.5
#             most_common_urls[url].append(bias)
#         elif 'npr' in url: 
#             bias = -0.5
#             most_common_urls[url].append(bias)
#         elif 'colbertreport' in url: 
#             bias = -0.5
#             most_common_urls[url].append(bias)
#         elif 'nytimes' in url: 
#             bias = -0.5
#             most_common_urls[url].append(bias)
#         elif 'slate' in url:
#             bias = -0.6
#             most_common_urls[url].append(bias)
#         elif 'newyorker' in url:
#             bias = -0.6
#             most_common_urls[url].append(bias)
#         else: 
#             bias = 0
#             most_common_urls[url].append(bias)

# print(most_common_urls)

# import matplotlib.pylab as plt


# for item in most_common_urls.items():
#     label = item[0]
#     data = item[1]
#     for i in data: 
#         x = data[0]
#         y = data[1]
#         plt.scatter(x, y, color='blue', marker='*')
        
# plt.xlabel('Frequency of Tweets')
# plt.ylabel('Bias: Conservative to Liberal')

# plt.savefig('./data/common_urls.png')
# #plt.show()

# for item in most_common_urls.items():
#     label = item[0]
#     data = item[1]
#     for i in data:
#         if data[1]>0: 
#             x = data[0]
#             y = data[1]
#             plt.scatter(x, y, color='blue', marker='*')
#         plt.annotate(label, xy = (x, y))
        
# plt.xlabel('Frequency of Tweets')
# plt.ylabel('Bias: Conservative')
# plt.title('Conservative Tweets')

# plt.savefig('./data/conservative_urls.png')
# #plt.show()

# for item in most_common_urls.items():
#     label = item[0]
#     data = item[1]
#     for i in data:
#         if data[1]<0: 
#             x = data[0]
#             y = data[1]
#             plt.scatter(x, y, color='blue', marker='*')
#     plt.annotate(label, xy = (x, y))
        
# plt.xlabel('Frequency of Tweets')
# plt.ylabel('Bias: Liberal')
# plt.title('Liberal Tweets')

# plt.savefig('./data/liberal_urls.png')
# #plt.show()

# for item in most_common_urls.items():
#     label = item[0]
#     data = item[1]
#     for i in data:
#         #excludes twitter bc there are too many links // messes w graph
#         if data[1]==0 and data[0]<40000: 
#             x = data[1]
#             y = data[0]
#             plt.scatter(x, y, color='blue', marker='*')
#     plt.annotate(label, xy = (x, y))
        
# plt.xlabel('Frequency of Tweets')
# plt.ylabel('Bias = 0')
# plt.title('UnBiased Tweets')

# plt.savefig('./data/unbiased_urls.png')
# #plt.show()

