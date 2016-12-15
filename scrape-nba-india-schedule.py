import requests
from bs4 import BeautifulSoup
import json

# Initially used it like shown below, but the get params NEED to be ORDERED.
# get_params = {
# 	'LeagueID': '00',
# 	'Season': '2016',
# 	'RegionID': '16'
# }

headers = {
	
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language': 'en-US,en;q=0.8',
	'Cache-Control': 'max-age=0',
	'Connection' : 'keep-alive',
	'Cookie': 'AMCVS_248F210755B762187F000101%40AdobeOrg=1; AMCV_248F210755B762187F000101%40AdobeOrg=817868104%7CMCIDTS%7C17106%7CMCMID%7C78092087918634394234567867213126827336%7CMCAAMLH-1478502128%7C3%7CMCAAMB-1478502128%7CNRX38WO0n5BH8Th-nqAG_A%7CMCOPTOUT-1477904528s%7CNONE%7CMCAID%7CNONE; s_ppvl=http%253A%2F%2Fglobal.nba.com%2Fvideo%2Findia-fans-hear-the-truth-from-paul-pierce%2F%2C100%2C100%2C703%2C1280%2C703%2C1280%2C800%2C2%2CL; s_cc=true; s_sq=%5B%5BB%5D%5D; s_vi=[CS]v1|2C0B763885190B3C-40000609E0002489[CE]; s_fid=388766E1CD718A67-087634DEC2E69663; s_ppv=http%253A%2F%2Fglobal.nba.com%2Fbroadcaster-schedule%2F%2C100%2C100%2C1095%2C1280%2C150%2C1280%2C800%2C2%2CL',
	'Host' : 'stats.nba.com',
	'Upgrade-Insecure-Requests' : '1',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}

get_params = (('LeagueID', '00'), ('Season', '2016'), ('RegionID', '16'))
url = "http://stats.nba.com/stats/internationalbroadcasterschedule"
r = requests.get(url, params=get_params, headers=headers)
print(r)
data = json.loads(r.text)

upcomingMatches =  data['resultSets'][0]['NextGameList']
allMatches = data['resultSets'][1]['CompleteGameList']
allMatchesJson = json.dumps(data['resultSets'][1]['CompleteGameList'], indent=4, sort_keys=True)

obj = open('nba_schedule_india.json', 'w')
obj.write(allMatchesJson)
obj.close

# for match in allMatches:



