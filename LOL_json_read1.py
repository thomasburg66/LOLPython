__author__ = 'Thomas'

'''
1.2x: create local copy of match data in json format
1.1x: pull misc game data by guessing game ids
1.0x: get data for specific summoner
'''

NAME = "LOLPyth"
VERSION = "1.21 - 12Jul2015"

import urllib2 as urllib
import json
import time
import string
import sys

'''

https://developer.riotgames.com/api/methods

u'gameId': 1343001336, u'championId': 37, u'level': 30,
u'createDate': 1393263989033L, u'gameMode': u'ARAM', u'mapId': 12,
u'gameType': u'MATCHED_GAME', u'subType': u'ARAM_UNRANKED_5x5',
u'teamId': 200, u'invalid': False, u'ipEarned': 220,

u'fellowPlayers': [{u'team
Id': 200, u'championId': 143, u'summonerId': 22791283}, {u'teamId': 100, u'championId': 24, u'summonerId': 20130360}, {u'teamId': 100, u'cha
mpionId': 40, u'summonerId': 44188584}, {u'teamId': 200, u'championId': 92, u'summonerId': 31652931}, {u'teamId': 200, u'championId': 101, u
'summonerId': 21043585}, {u'teamId': 100, u'championId': 60, u'summonerId': 19635022}, {u'teamId': 200, u'championId': 114, u'summonerId': 2
0812831}, {u'teamId': 100, u'championId': 98, u'summonerId': 27704461}, {u'teamId': 100, u'championId': 18, u'summonerId': 20906123}]

, u'spell1': 21, u'spell2': 4,

u'stats':
{
  u'timePlayed': 1452, u'win': True, u'totalDamageDealt': 34410,
  u'magicDamageDealtToChampions': 11475, u'largestMultiKill': 1,
  u'largestKillingSpree': 2, u'magicDamageTaken': 8755, u'totalTimeCrowdControlDealt': 299,
  u'item2': 3116, u'item3': 302  0, u'item0': 3108, u'item1': 3089, u'item4': 3003,
  u'item5': 1004, u'minionsKilled': 24, u'championsKilled': 5, u'assists': 39,
  u'physicalDamageDealtToChampions': 2089,
  u'goldSpent': 12205,
  u'level': 18, u'physicalDamageDealtPlayer': 11448, u'totalHeal': 18475,
  u'goldEarned': 137
  68, u'turretsKilled': 1, u'totalDamageDealtToChampions': 13564, u'totalUnitsHealed': 5,
  u'team': 200, u'numDeaths': 4, u'totalDamageTaken':
  19566, u'killingSprees': 2, u'magicDamageDealtPlayer': 22962, u'physicalDamageTaken': 10811
}

}


'''

# LOL API credentials
api_keys = {
  "na": "268306a5-a526-4535-800c-623be8313f74",
  "euw": "71be2bcb-e5de-4784-bede-3573498311f2"
}

http_method = "GET"
http_handler = urllib.HTTPHandler()

G_loglevel=0

def Linefeed():
  print
  "----------------------------------------------------------------"


def get_api_key(region):
  for key, value in api_keys.items():
    if key == region:
      if G_loglevel > 50:
        print
        "API key for region", region, "is ", value
      return "api_key=" + value
  return "???"




def getJSONResponse(region,context, url_end):
# return success, then return val or error string

  if region == "na":
    full_url = "https://na.api.pvp.net/" + url_end
  elif region == "euw":
    full_url = "https://euw.api.pvp.net/" + url_end
  elif region=="global":
    full_url= "https://global.api.pvp.net/api/lol/static-data" + url_end
  else:
    print"unknown region"
    sys.exit()

  if G_loglevel > 40:
    print "getJSONResponse1 url is " + full_url

  try:
    httpresponse = urllib.urlopen(full_url)
  except Exception, e:
    if G_loglevel>10:
      print "http error ",e,"continuing..."
    return False,"HTTP error"+str(e)

  if G_loglevel > 80:
    print "getJSONResponse2 context",context + ": httpresponse is " + httpresponse

  jsonresponse = httpresponse.read()
  if G_loglevel > 70:
    print "getJSONResponse3 context",context + ": jsonresponse is " + jsonresponse

  try:
    j1 = json.loads(jsonresponse)
  except Exception, e:
    return False,"JSonError"+str(e)

  if G_loglevel > 60:
    print "getJSONResponse4 context",context + ": json resp is " + j1

  return True,j1


def get_champion_name(id, region):
  url_end = "/"+region + "/v1.2/champion/"
  url_end = url_end + str(id)
  url_end = url_end + "?" + get_api_key(region)
  success,resp = getJSONResponse("global", "get_champion_name", url_end)
  if not success:
    print "oops - champion not found"
    sys.exit()
  return resp["name"]
def getSummonerId(name, region):
  url_end = "api/lol/" + region + \
        "/v1.4/summoner/by-name/" + name + \
        "?" + get_api_key(region)
  success,resp = getJSONResponse(region, "getSummonerId", url_end)
  if not success:
    print "oops - summoner not found"
    sys.exit()

  j2 = resp[name]
  id = j2["id"]
  return id

def safeGetStats(stats, value):
  try:
    theResult = stats[value]
  except Exception, e:
    theResult = 0
  return theResult


def printSummonerGameList(id, region, do_csv):
  url1 = "api/lol/" + region + "/v1.3/game/by-summoner/"
  url2 = "/recent?" + get_api_key(region)
  url = url1 + str(id) + url2

  success,resp = getJSONResponse(region,"printSummonerGameList", url)
  if not success:
    print "oops - gamelist not found"
    sys.exit()

  gamelist = resp["games"]
  if G_loglevel > 30:
    Linefeed()
    print "+++ gamelist is: <" + str(gamelist) + ">"

  if do_csv:
    print "GameID\tWhen\tMins\tGameType\tSubType\tMode\tLvl" \
      "\tWon?\tChampion\tDamTC\tGEarn\tGSold\tKMni\tKTur\tKill\tDeth\tAsst"
  else:
    print "GameID     When                   Mins GameType     " + \
      "   SubType              Mode      Lvl" \
      " Won?   Champion        DamTC GEarn GSold KMni KTur Kill Deth Asst"

  if not do_csv:
    print \
    "---------- ------------------------ -- --------     " + \
    "   -------------------- --------  ---" \
    " ---- ----------------  ----- ----- ----- ---- ---- ---- ---- ----"

  gamenum = 10

  for game in gamelist:
    if G_loglevel > 0:
      Linefeed()
      print "*** game is <" + str(game) + ">"

    # gather some data
    championId = game["championId"]
    championName = get_champion_name(championId, region)

    # stats
    stats = game["stats"]
    if G_loglevel == 88:
      print stats;
    minutes = int(stats["timePlayed"]) / 60

    numtime = game["createDate"] / 1000
    gametime = time.ctime(numtime)

    # physical damage if present
    try:
      pd = stats["physicalDamageDealtToChampions"]
    except Exception, e:
      pd = "???"

    # and print it
    if do_csv:
      TXT = "\""
      SEP = "\t"
    else:
      TXT = ""
      SEP = " "

    gamenum=game["gameId"]

    print \
        string.rjust(str(gamenum), 2) + SEP + \
        TXT + gametime + TXT + SEP + \
        str(minutes) + SEP + \
        string.ljust(str(game["gameType"]), 15) + SEP + \
        string.ljust(str(game["subType"]), 20) + SEP + \
        string.ljust(game["gameMode"], 10) + SEP + \
        string.rjust(str(game["level"]), 2) + SEP + \
        string.ljust(str(stats["win"]), 6) + SEP + \
        string.ljust(championName, 15) + SEP + \
        string.rjust(str(pd), 5) + SEP + \
        string.rjust(str(stats["goldEarned"]), 5) + SEP + \
        string.rjust(str(stats["goldSpent"]), 5) + SEP + \
        string.rjust(str(stats["minionsKilled"]), 4) + SEP + \
        string.rjust(str(safeGetStats(stats, "turretsKilled")), 4) + SEP + \
        string.rjust(str(safeGetStats(stats, "championsKilled")), 4) + SEP + \
        string.rjust(str(safeGetStats(stats, "numDeaths")), 4) + SEP + \
        string.rjust(str(safeGetStats(stats, "assists")), 4)

    # increase counter
    gamenum = gamenum - 1

# /api/lol/{region}/v2.2/match/
def process_match(match_id,region,output_format):
  url_end = "api/lol/" + region + \
        "/v2.2/match/" + str(match_id) + \
        "?" + get_api_key(region)

  success,resp = getJSONResponse(region, "process_match", url_end)
  if not success:
    return success

#  if G_loglevel>100:
#    print resp

  sep1=' '
  txt1="\""

  if output_format=="JSON":
    print resp
  else:
    print match_id,\
      "\""+str(time.ctime(resp["matchCreation"]/1000))+"\"",\
      resp["matchCreation"],\
      resp["matchDuration"],\
      resp["mapId"],\
      resp["matchVersion"],\
      resp["queueType"],resp["matchMode"],resp["matchType"]

  return True

def pull_loop(starting_match_id, pull_interval_ms, region, output_format):
  match_id=starting_match_id
  is_done=False

  while not is_done:
    # get next match
    success=process_match(match_id,region,output_format)

    # wait a bit
    time.sleep(pull_interval_ms / 1000)

    # next match
    match_id=match_id+1

def get_output_format(input):
  input.upper();
  if input=="JSON" or input=="TXT":
    return input
  else:
    print "illegal value '"+input+"' for <output format>"
    sys.exit()

def collect_data():
  global G_loglevel

  try:
    starting_match_id = int(sys.argv[1])
    region = sys.argv[2]
    pull_interval_ms = int(sys.argv[3])
    output_format=get_output_format(sys.argv[4])
    G_loglevel = int(sys.argv[5])
  except Exception, e:
    usage(2)
    sys.exit()

  print "data collecting mode: starting match id ",starting_match_id,\
        ", pull interval ",pull_interval_ms,"ms" \
        ", region ",region,", loglevel ",G_loglevel

  pull_loop(starting_match_id, pull_interval_ms, region, output_format)

  sys.exit()

def usage(mode):

  if mode==0 or mode==1:
    print "\n\n--- Mode1: get last 10 games for a summoner ---"
    print   "usage: " + sys.argv[0] + " <name of summoner> <region> <csv> <loglevel>"
    print  "   <csv>   - Y or y for Excel readable format"
    print  "           - any other value for human readable format"

  if mode==0 or mode==2:
    print "\n\n--- Mode2: slowly gather game data ---"
    print "usage: " + sys.argv[0] + \
          " <starting game id> <region> <pull interval[ms]> <output format> <loglevel>"
    print "    <output format> can be JSON or CSV"


def hello():
  print NAME, " version ", VERSION

def dummy_main():
  return

if __name__ == '__main__':

  hello()

  try:
    mode=int(sys.argv[1])
    if mode>1000000000:
      # data collecting mode
      collect_data()
  except Exception, e:
    try:
      strval=sys.argv[1]
    except Exception, e:
      usage(0)
      sys.exit()

  # get runtime parameters
  try:
    summoner_name = sys.argv[1]
    region = sys.argv[2]
    do_csv = sys.argv[3]
    G_loglevel = int(sys.argv[4])
  except Exception, e:
    usage(1)
    sys.exit()

  if do_csv == "y" or do_csv == "Y":
    do_csv = True
  else:
    do_csv = False

  if not do_csv:
    print "human readable output, region '" + region + "', summoner '" \
      + summoner_name + "', debug " + str(G_loglevel)

  # convert to id
  id = getSummonerId(summoner_name, region)

 # get stats
  printSummonerGameList(id, region, do_csv)
