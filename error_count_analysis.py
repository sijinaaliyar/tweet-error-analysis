import os
import re
import glob
import gzip
import pandas as pd
import datetime as dt
import subprocess
from pathlib import Path
from collections import Counter

error_list = []
error_count = 1
error_count_in_news = dict()
news_base_path = "/content/drive/MyDrive/Twitter/live_news/"
#news_base_path = os.path.join(os.environ['HOME'], "projects", "news", "release", "data", "live_news")
news_agents = os.listdir(news_base_path)
# Drop Reuters
news_agents.remove('reuters')

# Today's date
end = dt.datetime.today()
end_timestamp = int(end.strftime("%Y%m%d"))
# More flexbility with date command if running on Linux
# date -d "-1 month" +%Y%m%d
# date -d "-1 week" +%Y%m%d
# date -d "-1 day" +%Y%m%d
start = subprocess.run(["date", "-d", "-1 day", "+%Y%m%d"], capture_output=True)
start_timestamp = int(start.stdout.decode('utf-8'))


# Read the content of the error file.
def readErrorContent(path):
  data = pd.read_csv(path, compression='gzip') 
  # Replacing 403 errors with the common error content
  return data["error"].str.replace(r'(403 Client Error: Forbidden for url:.*$)', '403 Client Error: Forbidden for url')


def extract_date(path):
    match_result = re.search(r'(20[0-9][0-9][0-9][0-9][0-9][0-9])', str(path))
    if match_result:
        return match_result.group(1)
    assert False, "Couldn't extract date"

    
# Check if the directory is in the wanted interval
def in_wanted_date_interval(path):
    data_date = int(extract_date(path))
    if data_date >= start_timestamp and data_date <= end_timestamp:
        return True
    return False

        
# Loop through the folders to find the error content from error file
for agent in news_agents:
    path = Path(os.path.join(news_base_path, agent))
    error_files = path.rglob('error_url.csv.gz')
    #print(error_files)
    error_list = []
    for ef in error_files:
        if in_wanted_date_interval(ef):
            error_list.append(readErrorContent(ef))
    if len(error_list) > 0:
        error_count_in_news[agent] = Counter(error_list[0])

        
for key, value in error_count_in_news.items():
    print("------------")
    print('\033[1m' +key + '\033[0m')
    print("------------")
    for item in value.most_common():
        print(item[0] + " : " + (str)(item[1]))
