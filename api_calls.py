from urllib.parse import quote_plus
from requests import get
from random import randint
from time import sleep


class WolframBot:
    def __init__(self, app_ids) -> None:
        self.__app_ids = app_ids
        self.num_of_appids = len(self.__app_ids)

    def __get_random_id(self) -> str:
        return self.__app_ids[randint(0, self.num_of_appids - 1)]

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

    def __get_url_of_steps_image(self, img_xml):
        img_list = img_xml.split("\n")
        url_index = -1
        for i in range(len(img_list)):
            if "Possible intermediate steps" in img_list[i]:
                url_index = i+1
                break

        if url_index == -1:
            return "No step by step solution available."

        url_raw = str(img_list[url_index]).strip()
        url = url_raw.replace(' ', '').replace('<imgsrc=', '').replace('<img src=', '').replace("'", "").replace('"', '')

        return url


    def get_step_by_step(self, query: str) -> str:
        filename = "{}.png".format(query)
        api_url = "https://api.wolframalpha.com/v2/query?appid={}&input={}&podstate=Step-by-step+solution&format=image&totaltimeout=2&background=F5F5F5&fontsize=20"
        id = self.__get_random_id()

        query = api_url.format(id, quote_plus(query))
        response = get(query)
        img_src = self.__get_url_of_steps_image(response.text)
        sleep(4)

        if img_src != "No step by step solution available.":
            for count in range(35):
                r = get(img_src, stream=True)
                if r.status_code == 200:
                    with open(filename, "wb") as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)

                    return "Query result saved in: " + filename
                else:
                    sleep(2)
        else:
            return img_src
        return "Error processing your request."

    def query_wolfram(self, query: str, is_image=False) -> str:
        if not is_image:
            out = self.__short_anwser(query)
            if out.strip() != "No short answer available":
                return out

        image_response = self.__get_image(query)
        if image_response != "Error processing your request.":
            return "Query result saved in: " + image_response

        return image_response
