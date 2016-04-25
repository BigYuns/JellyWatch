from google.appengine.ext import ndb
import urlparse
import webapp2

class Photo(ndb.Model):
    mime = ndb.StringProperty()
    data = ndb.BlobProperty()
    
    @classmethod
    def from_data_uri(cls, url):
        up = urlparse.urlparse(url)
        head, data = up.path.split(',', 1)
        bits = head.split(';')
        mime_type = bits[0] if bits[0] else 'text/plain'
        charset, b64 = 'ASCII', False
        for bit in bits:
            if bit.startswith('charset='):
                charset = bit[8:]
            elif bit == 'base64':
                b64 = True
        plaindata = data.decode("base64")
        
        p = Photo()
        p.mime = mime_type
        p.data = plaindata
        return p
    
    def get_url(self):
        return '/photo?id=' + self.key.urlsafe()

def store_photo(photo_url):
    p = Photo.from_data_uri(photo_url)
    p.put()
    return p.get_url()

class ServePhotoHandler(webapp2.RequestHandler):
    def get(self):
        p = ndb.Key(urlsafe=self.request.get('id')).get()
        self.response.headers['Content-Type'] = p.mime.encode('utf-8')
        self.response.write(p.data)
