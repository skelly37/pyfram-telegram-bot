from urllib.request import urlretrieve, urlopen, Request
from urllib.parse import quote_plus
from typing import Callable
import telebot

class WolframBot:
    def __init__(self, appID: str) -> None:
        self.appID = appID

    def __short_anwser(self, query: str) -> str:
        url = "https://api.wolframalpha.com/v1/result?appid={}&i={}"
        query = url.format(self.appID, quote_plus(query))
        response = urlopen(Request(query))
        return response.read().decode()

    def __get_image(self, query: str) -> str:
        filename = "{}.png".format(query)
        api_url = "https://api.wolframalpha.com/v1/simple?appid={}&i={}&background=F5F5F5&fontsize=20"
        query = api_url.format(self.appID, quote_plus(query))
        urlretrieve(query, filename)
        return filename

    def query_wolfram(self, query: str, is_image=False:) -> str:
        if not is_image:
            out = self.__short_anwser(query)
            if out.strip() != "No short answer available":
                return out

        return "Query result saved in: " + self.__get_image(query)

def temp_test() -> None:
    appid = open("api_key.txt").readline().strip()
    b = WolframBot(appid)
    print(f"2+2= {b.query_wolfram('2+2')}")
    print(f"Poland (should return text): {b.query_wolfram('binomial coefficient')}")
    print(f"Poland (should fetch image): {b.query_wolfram('binomial coefficient', True)}")

temp_test()
