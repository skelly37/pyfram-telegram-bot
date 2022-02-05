from requests import get

appID = #put API key here

def get_short_anwser(query):
	query = "https://api.wolframalpha.com/v1/result?appid=" + appID + "&i=" + query
	return get(query).text
