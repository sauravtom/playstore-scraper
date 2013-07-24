import webapp2
from google.appengine.ext import ndb
from scraper import generate_app_list,generate_app_details


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
     
        
        arr1,arr2 = generate_app_list()
        self.response.write(arr1)

        '''
        for i in arr1:
            d = generate_app_details(i,arr1.index(i)+1)
            #sys.exit(0)
            self.response.write(i)

        for i in arr2:
            #d=generate_app_details(i,arr1.index(i)+1)
            self.response.write(i)
         '''

class Product(ndb.Model):
    link = ndb.KeyProperty(required = True)
    @classmethod
    def addProduct(cls,link):
        product = Product(link = link)
        return product.put()

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)