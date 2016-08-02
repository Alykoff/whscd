from __future__ import print_function
import requests
import logging
import re
import http.client as httplib
import csv
from time import sleep

base_url = 'https://www.whoscored.com'
start_url = base_url + '/Regions/252/Tournaments/2/Seasons/5826/Stages/12496/PlayerStatistics/England-Premier-League-2015-2016'
player_statistic_url = base_url + '/StatisticsFeed/1/GetPlayerStatistics'
incap_cookie_name = 'incap_ses_324_774904'
visid_cookie_name = 'visid_incap_774904'
last_mode_header_name = 'Model-Last-Mode'

ses_pattern = re.compile('.*' + incap_cookie_name + '=([^;]*).*$')
visit_pattern = re.compile('.*' + visid_cookie_name + '=([^;]*).*$')
model_id_pattern = re.compile("'" + last_mode_header_name + "': '(.*)' }")

httplib.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

numberOfPlayersToPick = 10
timeout_sec = 2
x_cookie = ""
with open('cookie.txt', encoding='utf-8') as cookie_file:
	x_cookie = str(cookie_file.read()).replace('\n', '') 

params = {
	"category": "summary",
	"subcategory": "all",
	"statsAccumulationType": "0",
	"isCurrent": "true",
	"playerId": "",
	"teamIds": "",
	"matchId": "",
	"stageId": "12496",
	"tournamentOptions": "2",
	"sortBy": "Rating",
	"sortAscending": "",
	"age": "",
	"ageComparisonType": "",
	"appearances": "",
	"appearancesComparisonType": "",
	"field": "Overall",
	"nationality": "",
	"positionOptions": "",
	"timeOfTheGameEnd": "",
	"timeOfTheGameStart": "",
	"isMinApp": "true",
	"page": "",
	"includeZeroValues": "",
	"numberOfPlayersToPick": numberOfPlayersToPick
}
auth_headers = {
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"pragma": "no-cache",
	"dnt": "1",
	"x-requested-with": "XMLHttpRequest",
	"accept-language": "en-US,en;q=0.8,ru;q=0.6",
	"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
	"cache-control": "no-cache",
	"upgrade-insecure-requests": "1",
	"authority": "www.whoscored.com",
	"cookie": x_cookie
}
headers = {
	"pragma": "no-cache",
	"dnt": "1",
	"x-requested-with": "XMLHttpRequest",
	"accept-language": "en-US,en;q=0.8,ru;q=0.6",
	"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
	"accept": "application/json, text/javascript, */*; q=0.01",
	"cache-control": "no-cache",
	"upgrade-insecure-requests": "1",
	"authority": "www.whoscored.com",
	"referer": "https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/5826/Stages/12496/PlayerStatistics/England-Premier-League-2015-2016",
	"cookie": x_cookie
}
auth_request = requests.get(
	start_url,
	headers=auth_headers,
	timeout=timeout_sec
)

sleep(1)

model_id = model_id_pattern.search(auth_request.text).group(1)
r_headers = headers.copy()
r_headers['model-last-mode'] = model_id

r = requests.get(
	player_statistic_url, 
	params=params, 
	headers=r_headers,
	timeout=timeout_sec
)
rjson = r.json()
print('\n=====')
print(rjson)
with open('out/england_premier.csv', 'w+') as england_premier_file:
	england_premier_csv = csv.writer(england_premier_file)
	england_premier_csv.writerow([
		'teamId',
		'playedPositionsShort',
		'apps',
		'positionText',
		'isActive',
		'passSuccess',
		'rating',
		'isOpta',
		'yellowCard',
		'seasonName',
		'subOn',
		'ranking',
		'seasonId',
		'playedPositions',
		'isManOfTheMatch',
		'tournamentName',
		'tournamentRegionId',
		'age',
		'tournamentRegionCode',
		'firstName',
		'goal',
		'minsPlayed',
		'redCard',
		'height',
		'lastName',
		'name',
		'regionCode',
		'weight',
		'manOfTheMatch',
		'tournamentId',
		'shotsPerGame',
		'aerialWonPerGame',
		'tournamentShortName',
		'assistTotal',
		'teamName',
		'playerId'
	])
	for x in rjson['playerTableStats']:
		england_premier_csv.writerow([
			x['teamId'],
			x['playedPositionsShort'],
			x['apps'],
			x['positionText'],
			x['isActive'],
			x['passSuccess'],
			x['rating'],
			x['isOpta'],
			x['yellowCard'],
			x['seasonName'],
			x['subOn'],
			x['ranking'],
			x['seasonId'],
			x['playedPositions'],
			x['isManOfTheMatch'],
			x['tournamentName'],
			x['tournamentRegionId'],
			x['age'],
			x['tournamentRegionCode'],
			x['firstName'],
			x['goal'],
			x['minsPlayed'],
			x['redCard'],
			x['height'],
			x['lastName'],
			x['name'],
			x['regionCode'],
			x['weight'],
			x['manOfTheMatch'],
			x['tournamentId'],
			x['shotsPerGame'],
			x['aerialWonPerGame'],
			x['tournamentShortName'],
			x['assistTotal'],
			x['teamName'],
			x['playerId']
		])




