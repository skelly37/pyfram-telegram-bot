from urllib.parse import quote_plus
from requests import get
from random import randint

#TODO randomize API calls from list of few APIS

class WolframBot:
    def __init__(self, app_ids) -> None:
        self.app_ids = app_ids
        self.num_of_appids = len(app_ids)

    def __get_random_id(self) -> str:
        return self.app_ids[randint(0, self.num_of_appids - 1)]

    def __short_anwser(self, query: str) -> str:
        url = "https://api.wolframalpha.com/v1/result?appid={}&i={}"
        id = self.__get_random_id()
        query = url.format(id, quote_plus(query))
        return get(query).text

    def __get_image(self, query: str) -> str:
        filename = "{}.png".format(query)
        api_url = "https://api.wolframalpha.com/v1/simple?appid={}&i={}&background=F5F5F5&fontsize=20"
        id = self.__get_random_id()
        query = api_url.format(id, quote_plus(query))
        r = get(query, stream = True)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        return filename

    def query_wolfram(self, query: str, is_image=False) -> str:
        if not is_image:
            out = self.__short_anwser(query)
            if out.strip() != "No short answer available":
                return out

        return "Query result saved in: " + self.__get_image(query)