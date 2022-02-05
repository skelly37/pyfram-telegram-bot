from requests import get
from urllib.request import urlretrieve
from urllib.parse import quote_plus

class Bot:

    def __init__(self,appid):
        self.appid = appid        

    def short_answer(self,sequery):
            url = "https://api.wolframalpha.com/v1/result?appid={}&i={}"
            query = url.format(self.appid,quote_plus(sequery))
            return get(query).text

    def get_image(self,query,filename):
            filename = "{}.png".format(filename)
            api_url = "https://api.wolframalpha.com/v1/simple?appid={}&i={}&background=F5F5F5&fontsize=20"
            query = api_url.format(self.appID,quote_plus(query))
            urlretrieve(query, filename)
            return filename

    def query_wolfram(self,query, is_image=False):
            if not is_image:
                    out = short_anwser(query)
                    if out.strip() != "No short answer available":
                            return out
                        
            return "Query result saved in: " + get_image(query)
