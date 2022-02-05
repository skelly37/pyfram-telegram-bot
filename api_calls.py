from requests import get
from urllib.request import urlretrieve

appID = #your appID

def short_anwser(query):
	query = "https://api.wolframalpha.com/v1/result?appid=" + appID + "&i=" + query
	return get(query).text

def get_image(query):
	filename = query + ".png"
	
	query = "https://api.wolframalpha.com/v1/simple?appid=" + appID + "&i=" + query
	query += "&background=F5F5F5"
	query += "&fontsize=20"
	
	urlretrieve(query, filename)
	return filename

def query_wolfram(query, is_image=False):
	if not is_image:
		out = short_anwser(query)
		if out.strip() != "No short answer available":
			return out

	return "Query result saved in: " + get_image(query)
