from URL import URL
from DB import DB
from bs4 import BeautifulSoup
import re

db = DB('play.db')
db.add_seeds('seed.txt')

count = 0
while db.count_unpr():
    # url = URL('http://citeseerx.ist.psu.edu/viewdoc/summary?cid=4320')
    count = count + 1
    url = db.get_unpr()

    url = URL(url)
    
    html = url.fetch()
    app_id = url.get_qs('id')
    
    if url.get_code() == 200:
        
        soup = BeautifulSoup(html, 'html.parser')
        
        id_app_title = soup.find("div", { "class" : "id-app-title" })
        id_app_title = id_app_title.text
        print id_app_title
        
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
        
        # meta_info = soup.findAll('div', { "class" : "content" })
        meta_info = soup.find('div', attrs = {'itemprop' : "numDownloads"})
        installs = meta_info.text.strip()
        print installs
        
        if not db.exists('metadata', app_id):
            db.insert('metadata', {
                                'id': app_id,
                                'name': id_app_title,
                                'org': name,
                                'genre': genre,
                                'installs': installs
                            })
        
        bar_numbers = soup.findAll("span", { "class" : "bar-number" })
        bar_numbers = bar_numbers[::-1]     # reversing bar numbers list
        rating = {"id": app_id}
        for i in range(1, 6):
            rating[i] = bar_numbers[i - 1].text.replace(',', '')
        print rating
        db.insert('rating', rating)
        
        rec_cluster = soup.findAll("div", { "class" : "rec-cluster" })
        see_more = rec_cluster[0].find('a')
        # print html
        
        url = URL('https://play.google.com/' + see_more['href'])
        html = url.fetch()
        
        soup = BeautifulSoup(html, 'html.parser')
        suggestions = soup.findAll("div", { "class" : "no-rationale" })
        # print len(suggestions)
        for suggestion in suggestions:
            anc = suggestion.find('a')
            
            url = URL(anc['href'])
            
            db.insert("edges", {
                "id_f": app_id,
                "id_t": url.get_qs('id')
            })
            
            if not db.exists('link', url.get_qs('id')):
                db.insert("link", {
                                "id": url.get_qs('id'),
                                "url": "https://play.google.com" + anc['href'],
                                "processed": 0
                })
            # print anc['href']
        
    db.update_link(app_id, 1)