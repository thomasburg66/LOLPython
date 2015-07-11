__author__ = 'Thomas'

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
api_keys={
  "na": "268306a5-a526-4535-800c-623be8313f74",
  "euw":"71be2bcb-e5de-4784-bede-3573498311f2"
}

loglevel=99 # global var !

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=loglevel)

def Linefeed():
  print "----------------------------------------------------------------"

def get_api_key(region):
  for key,value in api_keys.items():
    if key==region:
      if loglevel>50:
        print "API key for region",region,"is ",value
      return "api_key="+value
  return "???"

def getJSONResponse(context,url):
  if region=="na":
    url="https://na.api.pvp.net/"+url
  elif region=="euw":
    url="https://euw.api.pvp.net/"+url

  if loglevel>40:
    print context+": URL is "+url
  httpresponse=urllib.urlopen(url)
  jsonresponse=httpresponse.read()
  j1=json.loads(jsonresponse)
  if loglevel>80:
    print context+": json resp is "+str(j1)
  return j1

def get_champion_name(id,region):
  url="api/lol/static-data/"+region+"/v1.2/champion/"
  url=url+str(id)
  url=url+"?"+get_api_key(region)
  resp=getJSONResponse("get_champion_name`",url)
  return resp["name"]

def getSummonerId(name,region):
  url="api/lol/"+region+\
      "/v1.4/summoner/by-name/"+name+\
      "?"+get_api_key(region)
  resp=getJSONResponse("getSummonerId",url)
  j2=resp[name]
  id=j2["id"]
  return id

def safeGetStats(stats,value):
  try:
    theResult=stats[value]
  except Exception, e:
    theResult=0
  return theResult

def printSummonerGameList(id,region, do_csv):
  url1="api/lol/"+region+"/v1.3/game/by-summoner/"
  url2="/recent?"+get_api_key(region)
  url=url1+str(id)+url2

  resp=getJSONResponse("printSummonerGameList",url)
  gamelist=resp["games"]
  if loglevel>30:
    Linefeed()
    print "+++ gamelist is: <" + str(gamelist)+">"

  if do_csv:
    print "#\tWhen\tMins\tGameType\tSubType\tMode\tLvl"\
      "\tWon?\tChampion\tDamTC\tGEarn\tGSold\tKMni\tKTur\tKill\tDeth\tAsst"
  else:
    print " # When                   Mins GameType     "+\
      "   SubType              Mode      Lvl" \
      " Won?   Champion        DamTC GEarn GSold KMni KTur Kill Deth Asst"

  if not do_csv:
    print " - ------------------------ -- --------     "+\
      "   -------------------- --------  ---" \
      " ---- ----------------  ----- ----- ----- ---- ---- ---- ---- ----"

  gamenum=10

  for game in gamelist:
    if loglevel>0:
      Linefeed()
      print "*** game is <" + str(game)+">"

    # gather some data
    championId=game["championId"]
    championName=get_champion_name(championId,region)

    # stats
    stats=game["stats"]
    if loglevel==88:
      print stats;
    minutes=int(stats["timePlayed"])/60

    numtime=game["createDate"]/1000
    gametime=time.ctime(numtime)

    # physical damage if present
    try:
      pd=stats["physicalDamageDealtToChampions"]
    except Exception, e:
      pd="???"

    # and print it
    if do_csv:
      TXT="\""
      SEP="\t"
    else:
      TXT=""
      SEP=" "
    print \
      string.rjust(str(gamenum),2)+SEP+\
      TXT+gametime+TXT+SEP+\
      str(minutes)+SEP+\
      string.ljust(str(game["gameType"]),15)+SEP+\
      string.ljust(str(game["subType"]),20)+SEP+\
      string.ljust(game["gameMode"],10)+SEP+\
      string.rjust(str(game["level"]),2)+SEP+\
      string.ljust(str(stats["win"]),6)+SEP+\
      string.ljust(championName,15)+SEP+\
      string.rjust(str(pd),5)+SEP+\
      string.rjust(str(stats["goldEarned"]),5)+SEP+\
      string.rjust(str(stats["goldSpent"]),5)+SEP+\
      string.rjust(str(stats["minionsKilled"]),4)+SEP+\
      string.rjust(str(safeGetStats(stats,"turretsKilled")),4)+SEP+\
      string.rjust(str(safeGetStats(stats,"championsKilled")),4)+SEP+\
      string.rjust(str(safeGetStats(stats,"numDeaths")),4)+SEP+\
      string.rjust(str(safeGetStats(stats,"assists")),4)

    # increase counter
    gamenum=gamenum-1

def usage():
  print "usage: " + sys.argv[0] + " <name of summoner> <region> <csv> <debug>"
  print "   <csv>   - Y or y for Excel readable format"
  print "           - any other value for human readable format"
  print "   <debug> - 0 for quiet mode"
  print "         - any other value for human readable format"

def dummy_main():
  return

if __name__ == '__main__':
  # default summoner_name
  summoner_name="lgw2015" # "sayna" mtyranus

  # get runtime parameters
  try:
    summoner_name=sys.argv[1]
    region=sys.argv[2]
    do_csv=sys.argv[3]
    loglevel=int(sys.argv[4])
  except Exception,e:
    usage()
    sys.exit()

  if do_csv=="y" or do_csv=="Y":
    do_csv=True
  else:
    do_csv=False

  if not do_csv:
    print "human readable output, region '"+region+"', summoner '"\
      +summoner_name+"', debug "+str(loglevel)

  # convert to id
  id=getSummonerId(summoner_name,region)

  # headline
  if not do_csv:
    print "--- Statistics for "+region+" Summoner , "+summoner_name #+time.ctime(time.now())

  # get stats
  printSummonerGameList(id,region,do_csv)

