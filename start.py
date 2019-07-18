#!/usr/bin/env python3
import sys, os
import eyed3
import requests
import math
import json
import acoustid
import pprint
# files = os.listdir(sys.argv[1])

genres = set()

# for f in files:
#     pat = os.path.abspath(f)
#     audiofile = eyed3.load(sys.argv[1] + "/" +f)
#     genre = str(audiofile.tag.genre)
#     genres.add(genre)

# for genre in genres:
#     print(genre)


my_file = sys.argv[1]
duration, fp_encoded = acoustid.fingerprint_file(my_file)
key = 'd6nRzqa53O'

audiofile = eyed3.load(sys.argv[1])

duration = math.floor(audiofile.info.time_secs)

#url = 'https://api.acoustid.org/v2/lookup?client={}&meta=recordings+recordingids+releases+releaseids+releasegroups+releasegroupids+tracks+compress+usermeta+sources&duration={}&fingerprint={}'.format(key,duration,fp_encoded.decode())
url = 'https://api.acoustid.org/v2/lookup?client={}&meta=recordings+sources+compress&duration={}&fingerprint={}'.format(key,duration,fp_encoded.decode())

results = requests.get(url)
json_result = json.loads(results.content.decode())
pp = pprint.PrettyPrinter(indent=4)
score = {'value':0,'itr':0}

for itr,result in enumerate(json_result['results']):
    # print(result['score'])
    if result['score'] > score['value']:
        score['value'] =  result['score']
        score['itr'] = itr

    # print('*********************************')
    # for recording in result['recordings']:
    #     pp.pprint(recording)
    #     print()

sources ={'value':0,'itr':0}
for itr,recording in enumerate(json_result['results'][score['itr']]['recordings']):
    if recording['sources'] > sources['value']:
        sources['value'] = recording['sources']
        sources['itr'] = itr

print(json_result['results'][score['itr']]['recordings'][sources['itr']])