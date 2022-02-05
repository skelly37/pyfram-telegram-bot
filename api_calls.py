from requests import get
from urllib.request import urlretrieve
from urllib.parse import quote_plus


class Bot:
    def __init__(self, appID):
        self.appID = appID

    def __short_anwser(self, sequery):
        url = "https://api.wolframalpha.com/v1/result?appid={}&i={}"
        query = url.format(self.appID, quote_plus(sequery))
        return get(query).text

    def __get_image(self, query):
        filename = "{}.png".format(query)
        api_url = "https://api.wolframalpha.com/v1/simple?appid={}&i={}&background=F5F5F5&fontsize=20"
        query = api_url.format(self.appID, quote_plus(query))
        urlretrieve(query, filename)
        return filename

    def query_wolfram(self, query, is_image=False):
        if not is_image:
            out = self.__short_anwser(query)
            if out.strip() != "No short answer available":
                return out

        return "Query result saved in: " + self.__get_image(query)

def temp_test(self):
    b = Bot("APP_ID")
    print(f"2+2= {b.query_wolfram('2+2')}")
    print(f"Poland (should return text): {b.query_wolfram('Poland')}")
    print(f"Poland (should fetch image): {b.query_wolfram('Poland', True)}")

temp_test()
