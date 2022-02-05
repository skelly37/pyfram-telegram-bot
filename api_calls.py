from requests import get
from urllib.request import urlretrieve
from urllib.parse import quote_plus

appID = # your appID

def short_anwser(query):
	query = "https://api.wolframalpha.com/v1/result?appid=" + appID + "&i=" + query
	return get(query).text

def get_image(query,filename):
        filename = "{}.png".format(filename)
        api_url = "https://api.wolframalpha.com/v1/simple?appid={}&i={}&background=F5F5F5&fontsize=20"
        query = api_url.format(appID,quote_plus(query))
        urlretrieve(query, filename)
        return filename

def query_wolfram(query, is_image=False):
	if not is_image:
		out = short_anwser(query)
		if out.strip() != "No short answer available":
			return out
                    
	return "Query result saved in: " + get_image(query)
