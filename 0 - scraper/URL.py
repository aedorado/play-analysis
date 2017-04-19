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
                self.code = 200
                return response.read()
            except urllib2.HTTPError as e:
                tries = tries + 1
                if tries >= 3:
                    self.code = e.code
                    return -1
                print 'An HTTP error occured : ' + str(e.code)
                print 'Refetching : ' + self.url
            time.sleep(2)
        
    def get_code(self):
        return self.code
        
        
    def get_qs(self, key):
        parsed = urlparse.urlparse(self.url)
        return urlparse.parse_qs(parsed.query)[key][0].strip()