from get_data import *
from ml_utils import *
import time
import json

queries = ['machine+learning','data+science','kaggle']

def update_db():
  with open('novos_videos.json', 'w+') as output:
    for query in queries:
      for page in range(1,4):
        search_page = download_search_page(query, page)
        video_list = parse_search_page(search_page)

        for video in video_list:
          try:
            video_page = download_video_page(video['link'])
            video_json_data = parse_video_page(video_page)

            p = compute_prediction(video_json_data)

            url = 'https://www.youtube.com{link}'.format(link=video['link'])
            data_front = {'title': video_json_data['title'],
                          'score': float(p),
                          'url': url}

            data_front['update_time'] = time.time()
            show = json.dumps(data_front) 

            print(show)
            output.write('{}\n'.format(show))
          except Exception as e:
            print(e)

  return True