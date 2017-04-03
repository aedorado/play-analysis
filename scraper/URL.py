import urllib2
import time
import urlparse

class URL:

    def __init__(self, url):
        self.url = url

    def fetch(self):
        OK = False
        tries = 0
        while not OK:
            try:
                response = urllib2.urlopen(self.url)
                print 'Success : ' + self.url
                OK = True
            except urllib2.HTTPError as e:
                tries = tries + 1
                if tries >= 256:
                    return -1
                print 'Failure.\nAn HTTP error occured : ' + str(e.code)
                print 'Refetching : ' + self.url
            time.sleep(2)
        html = response.read()
        return html
        
    def get_qs(self, key):
        parsed = urlparse.urlparse(self.url)
        return urlparse.parse_qs(parsed.query)[key][0].strip()