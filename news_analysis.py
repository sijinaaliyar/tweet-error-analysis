import os
import gzip
import glob
import json

data_dir = "/content/drive/MyDrive/news/"

twitter_dir = os.path.join(data_dir, "live_twitter")
news_sources = os.listdir(twitter_dir)
print("%d news sources: %s" % (len(news_sources), news_sources))

num_tweets = {}

for ns in news_sources:
    print("Processing: %s" % ns)

    num_tweets[ns] = 0
    
    for filepath in glob.glob(os.path.join(twitter_dir, ns, "**/*[0-9][0-9].json.gz")):
        print('Filepath: %s' % filepath)
        with gzip.open(filepath, 'r') as fp:
            json_bytes = fp.read()
        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)

        for tweet in data:
            num_tweets[ns] += 1
    
for ns, value in num_tweets.items():
    print("%s: %d %d" % (ns, value, num_full_texts[ns]))
