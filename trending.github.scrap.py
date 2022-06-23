import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()
languages = ['', 'c++', 'javascript', 'python']
ranges = ['daily', 'weekly', 'monthly']
url = 'https://github.com/trending/{}'

r = session.get(url.format(languages[0]), params={'since': ranges[0]})
html_soup = BeautifulSoup(r.text, 'html.parser')
repos_element = html_soup.find_all(class_='Box-row')
for repo in repos_element:
  author_element = repo.find(class_='text-normal')
  name = author_element.next_sibling.strip()
  author = author_element.get_text(strip=True)
  author = author[:len(author) - 2]
  star = repo.find(class_='octicon octicon-star').next_sibling.strip()
  language = repo.find('span', attrs={'itemprop':'programmingLanguage'})
  if (language is not None):
    language = language.get_text(strip=True)
  else:
    language = ''
  # muted-link d-inline-block mr-3
  print('Repo:', name)
  print('Author:', author)
  print('Star:', star)
  print('Language:', language)
