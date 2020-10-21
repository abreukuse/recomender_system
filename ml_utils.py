import pandas as pd
import numpy as np
import re
import joblib
from scipy.sparse import hstack, csr_matrix
import json

# carregando o modelo
mdl_rf = joblib.load('mdl_rf.pkl')
title_vec = joblib.load('title_vec_rf.pkl')

# esse dicionário é para passar os meses de portugês para ingês
mapa_meses = {'Fev':'Feb',
              'Abr':'Apr',
              'Mai':'May',
              'Ago':'Aug',
              'Set':'Sep',
              'Out':'Oct',
              'Dez':'Dec'}

def clean_date(data):
  # transforma as datas de publicação dos vídeos no formato datetime do pandas
  regex = re.compile(r'(\d{,2}) de ([a-z]{3})\. de (\d{4})')
  if re.search(regex, data['date']).groups() is None:
    return None

  match = regex.findall(data['date'])
  # primeiro processo - encontrar os padrões de datas
  dates_tuple = match[0] if len(match) > 0 else None 
  # segundo processo - colocar a inicial do mês em letra maiuscula
  title_mounth = (dates_tuple[0], dates_tuple[1].title(), dates_tuple[2]) if dates_tuple != None else None
  # terceito proceso - unir as datas
  whole_dates = ' '.join(title_mounth) if title_mounth != None else None
  # quarto processo - colocar as abreviações dos meses em inglês
  regex_month = re.compile(r'[A-Za-z]{3}')
  month_format = regex_month.findall(whole_dates)[0]
  date_fomated = whole_dates.replace(month_format, mapa_meses[month_format]) if whole_dates != None else None
  # quinto processo - colocar o zero na frente dos dias menores que dez
  dates_series = '0'+date_fomated if (date_fomated != None) and (len(date_fomated) == 10) else date_fomated
   
  return pd.to_datetime(dates_series, format='%d %b %Y')


def clean_views(data):
  # processa a quantidade de visualização em cada vídeo para inteiro
  raw_views_str = re.match(r'(\d+\.?\d*)', data['views'])
  if raw_views_str is None: 
    return 0
  
  raw_views_str = raw_views_str.group(1).replace('.','')
  return int(raw_views_str)


def compute_features(data):
  # constroi os atributos numéricos e textuais
  if 'views' not in data:
    return None

  published_date = clean_date(data)
  if published_date is None: 
    return None

  views = clean_views(data)
  title = data['title']

  features = dict()

  features['tempo_desde_pub'] = (pd.Timestamp.today() - published_date) / np.timedelta64(1, 'D')
  features['views'] = views
  features['views_por_dia'] = features['views'] / features['tempo_desde_pub']
  del features['tempo_desde_pub']

  vectorized_title = title_vec.transform([title])
  num_features = csr_matrix(np.array([features['views'], features['views_por_dia']]))
  feature_array = hstack([num_features, vectorized_title])

  return feature_array


def compute_prediction(data):
  # faz o cálculo para ser usado no ranqueamento
  feature_array = compute_features(data)

  if feature_array is None:
    return 0

  prf = mdl_rf.predict_proba(feature_array)[0][1]
  p = prf

  return p