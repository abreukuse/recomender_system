import os.path
from flask import Flask
import os
import json
import run_backend
import time

app = Flask(__name__)

def get_predictions():

  novos_videos_json = 'novos_videos.json'
  if not os.path.exists(novos_videos_json):
    run_backend.update_db()

  last_update = os.path.getmtime(novos_videos_json)

  with open('novos_videos.json', 'r') as lines:
    videos = [json.loads(line) for line in lines]

  predictions = []
  for video in videos:
    predictions.append((video['url'],video['title'],float(video['score'])))

  predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]

  predictions_formated = []
  for prediction in predictions:
    predictions_formated.append("<tr><th><a href=\"{link}\">{title}</a></th><th>{score}</th></tr>".format(title=prediction[1],link=prediction[0],score=prediction[2]))

  return '\n'.join(predictions_formated), last_update

@app.route('/')
def main_page():
  preds, last_update, = get_predictions()
  return """<head><h1>Recomendador de Vídeos do Youtube</h1></head>
  <body>
  Segundos desde a última atualização: {}
  <table>
          {}
  </table>
  </body>""".format((time.time() - last_update), preds)

if __name__ == '__main__':
  app.run()