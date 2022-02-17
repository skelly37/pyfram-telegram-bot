from urllib.parse import quote_plus
from requests import get
from random import randint
from time import sleep

from typing import List, Sequence


class WolframBot:
    ERROR_MSG: str = "Error processing your request"
    NO_STEPS_MSG: str = "No step by step solution available"
    NO_SHORT_MSG: str = "No short answer available"
    RESULT_SAVED_MSG: str = "Query result saved in: "

    def __init__(self, app_ids: Sequence[str], background: str = "F5F5F5", fontsize: str = "21", units: str ="metric") -> None:
        self.__app_ids: Sequence[str] = app_ids
        self.__background = background
        self.__fontsize = fontsize
        self.__units = units
        self.__num_of_appids: int = len(self.__app_ids)

    def __get_random_id(self) -> str:
        return self.__app_ids[randint(0, self.__num_of_appids - 1)]

    def __short_answer(self, query: str) -> str:
        url: str = "https://api.wolframalpha.com/v1/result?appid={}&i={}&units={}"
        id: str = self.__get_random_id()
        query = url.format(id, quote_plus(query), self.__units)
        return get(query).text

    def __get_image(self, query: str) -> str:
        filename: str = "{}.png".format(query)
        api_url: str = "https://api.wolframalpha.com/v1/simple?appid={}&i={}&background={}&fontsize={}&units={}"
        id : str= self.__get_random_id()
        query = api_url.format(id, quote_plus(query), self.__background, self.__fontsize, self.__units)
        r = get(query, stream=True)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            return filename
        return self.ERROR_MSG

    def __get_url_of_steps_image(self, img_xml: str) -> str:
        img_list: List[str] = img_xml.split("\n")
        url_index: int = -1
        for i in range(len(img_list)):
            if "Possible intermediate steps" in img_list[i]:
                url_index = i + 1
                break

        if url_index == -1:
            return self.NO_STEPS_MSG

        url_raw: str = str(img_list[url_index]).strip()
        url: str = url_raw.replace(' ', '').replace('<imgsrc=', '').replace('<img src=', '').replace("'", "").replace('"', '')

        return url

    def get_step_by_step(self, query: str) -> str:
        filename: str = "{}.png".format(query)
        api_url: str = "https://api.wolframalpha.com/v2/query?appid={}&input={}&podstate=Step-by-step+solution&format=image&totaltimeout=8&background={}&fontsize={}&units={}"
        id: str = self.__get_random_id()

        query = api_url.format(id, quote_plus(query), self.__background, self.__fontsize, self.__units)
        response = get(query)
        img_src: str = self.__get_url_of_steps_image(response.text)
        sleep(5)

        if img_src != self.NO_STEPS_MSG:
            for count in range(30):
                r = get(img_src, stream=True)
                if r.status_code == 200:
                    with open(filename, "wb") as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)

                    return self.RESULT_SAVED_MSG + filename
                else:
                    print(img_src)
                    sleep(3)
        else:
            return img_src
        return self.ERROR_MSG

    def query_wolfram(self, query: str, is_image: bool = False, inline_mode: bool = False) -> str:
        if not is_image:
            out: str = self.__short_answer(query)
            if out.strip() != self.NO_SHORT_MSG or inline_mode:
                return out

        image_response: str = self.__get_image(query)
        if image_response != self.ERROR_MSG:
            return self.RESULT_SAVED_MSG + image_response

        return image_response
