from google.appengine.ext import ndb
import urlparse

class Photo(ndb.Model):
    mime = ndb.StringProperty()
    data = ndb.BlobProperty()
    
    @classmethod
    def from_data_uri(cls, uri):
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
        return '/photo?id=' + self.key.id()

def upload_photo(photo_url):
    p = Photo.from_data_uri(photo_url)
    p.put()
    return p.get_url()
