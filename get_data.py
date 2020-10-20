from requests_html import HTMLSession, HTML 
from bs4 import BeautifulSoup

def download_search_page(query, page):
  api = 'https://www.youtube.com/results?search_query={query}&sp=CAI%253D&p={page}'
  url = api.format(query=query, page=page)
  session = HTMLSession()
  response = session.get(url)
  # executando java-script
  response.html.render(sleep=1, timeout=30)
  return response.html.html

def parse_search_page(page_html):
  html_file = HTML(html=page_html)

  video_list = []
  tags = html_file.find('a#video-title')

  for tag in tags:
    link = tag.attrs['href']
    title = tag.attrs['title']
    data = {'link':link,
            'title':title}
    video_list.append(data)
    
  return video_list

def download_video_page(link):
  url = 'https://www.youtube.com{link}'.format(link=link)
  session = HTMLSession()
  response = session.get(url)
  response.html.render(sleep=1, timeout=100)

  return response.html.html

def parse_video_page(page_html):
  parsed = BeautifulSoup(page_html, 'html.parser')
  # coletar título, data de publicação e quantidade de visualizações
  elements = parsed.find_all('yt-formatted-string', {'class':'style-scope ytd-video-primary-info-renderer'})
  elements.append(parsed.find('span', {'class':'view-count style-scope yt-view-count-renderer'}))

  title, date, views = [element.text if element is not None else 'NaN' for element in elements]

  data = {'title':title,
          'date':date,
          'views': views}

  return data