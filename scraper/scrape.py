from URL import URL
from DB import DB
from bs4 import BeautifulSoup
import re

url = URL('https://play.google.com/store/apps/details?id=com.bsb.hike')
html = url.fetch()
# print html

soup = BeautifulSoup(html, 'html.parser')

id_app_title = soup.find("div", { "class" : "id-app-title" })
id_app_title = id_app_title.text
print id_app_title

document_subtitles = soup.findAll("div", { "class" : "document-subtitles" })
# print document_subtitles

re_name = re.compile('<span itemprop="name">.*?<\/span>')
name = re_name.findall(html)
name = name[0]
name = re.sub(r"<.*?>", "", name)
print name

re_genre = re.compile('<span itemprop="genre">.*?<\/span>')
genre = re_genre.findall(html)
genre = genre[0]
genre = re.sub(r"<.*?>", "", genre)
print genre

bar_numbers = soup.findAll("span", { "class" : "bar-number" })
print bar_numbers


rec_cluster = soup.findAll("div", { "class" : "rec-cluster" })
see_more = rec_cluster[0].find('a')
print see_more['href']
# print html