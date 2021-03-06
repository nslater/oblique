import BeautifulSoup
import urllib

from google.appengine import api

import base

class Main(base.RequestHandler):

    def get(self, *args):
        uri = args[1] or ""
        if not uri:
            return self.ok("Please specify a URI.")
        uri = urllib.unquote(uri)
        if not uri.startswith("http://"):
            uri = "http://" + uri
        try:
            tree = BeautifulSoup.BeautifulSoup(
                api.urlfetch.fetch(uri).content,
                convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
        except:
            return self.ok("Error fetching fact.")
        try:
            message = base.collapse(tree.find("p", {"class" : "fact"}).string)
        except:
            return self.ok("Could not find fact.")
        return self.ok(message)
