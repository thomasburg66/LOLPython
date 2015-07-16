__author__ = 'Thomas'

'''
1.3x: read json output (mode 2) and write it in Excel format
1.2x: create local copy of match data in json format
1.1x: pull misc game data by guessing game ids
1.0x: get data for specific summoner
'''

NAME = "LOLPyth"
VERSION = "1.31 - 12Jul2015"

import urllib2 as urllib
import json
import time
import string
import sys

from colorama import init, Fore, Back, Style

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

# champion ids
champion_names={
      "35": "Shaco",
      "36": "DrMundo",
      "33": "Rammus",
      "34": "Anivia",
      "39": "Irelia",
      "157": "Yasuo",
      "37": "Sona",
      "38": "Kassadin",
      "154": "Zac",
      "150": "Gnar",
      "43": "Karma",
      "42": "Corki",
      "41": "Gangplank",
      "40": "Janna",
      "201": "Braum",
      "22": "Ashe",
      "23": "Tryndamere",
      "24": "Jax",
      "25": "Morgana",
      "26": "Zilean",
      "27": "Singed",
      "28": "Evelynn",
      "29": "Twitch",
      "3": "Galio",
      "161": "Velkoz",
      "2": "Olaf",
      "1": "Annie",
      "7": "Leblanc",
      "30": "Karthus",
      "6": "Urgot",
      "32": "Amumu",
      "5": "XinZhao",
      "31": "Chogath",
      "4": "TwistedFate",
      "9": "FiddleSticks",
      "8": "Vladimir",
      "19": "Warwick",
      "17": "Teemo",
      "18": "Tristana",
      "15": "Sivir",
      "16": "Soraka",
      "13": "Ryze",
      "14": "Sion",
      "11": "MasterYi",
      "12": "Alistar",
      "21": "MissFortune",
      "20": "Nunu",
      "107": "Rengar",
      "106": "Volibear",
      "105": "Fizz",
      "104": "Graves",
      "103": "Ahri",
      "99": "Lux",
      "102": "Shyvana",
      "101": "Xerath",
      "412": "Thresh",
      "98": "Shen",
      "222": "Jinx",
      "96": "KogMaw",
      "223": "TahmKench",
      "92": "Riven",
      "91": "Talon",
      "90": "Malzahar",
      "429": "Kalista",
      "10": "Kayle",
      "421": "RekSai",
      "89": "Leona",
      "79": "Gragas",
      "117": "Lulu",
      "114": "Fiora",
      "78": "Poppy",
      "115": "Ziggs",
      "77": "Udyr",
      "112": "Viktor",
      "113": "Sejuani",
      "110": "Varus",
      "111": "Nautilus",
      "119": "Draven",
      "432": "Bard",
      "245": "Ekko",
      "82": "Mordekaiser",
      "83": "Yorick",
      "80": "Pantheon",
      "81": "Ezreal",
      "86": "Garen",
      "84": "Akali",
      "85": "Kennen",
      "67": "Vayne",
      "126": "Jayce",
      "69": "Cassiopeia",
      "127": "Lissandra",
      "68": "Rumble",
      "121": "Khazix",
      "122": "Darius",
      "120": "Hecarim",
      "72": "Skarner",
      "236": "Lucian",
      "74": "Heimerdinger",
      "75": "Nasus",
      "238": "Zed",
      "76": "Nidalee",
      "134": "Syndra",
      "133": "Quinn",
      "59": "JarvanIV",
      "58": "Renekton",
      "57": "Maokai",
      "56": "Nocturne",
      "55": "Katarina",
      "64": "LeeSin",
      "62": "MonkeyKing",
      "63": "Brand",
      "268": "Azir",
      "267": "Nami",
      "60": "Elise",
      "131": "Diana",
      "61": "Orianna",
      "266": "Aatrox",
      "143": "Zyra",
      "48": "Trundle",
      "45": "Veigar",
      "44": "Taric",
      "51": "Caitlyn",
      "53": "Blitzcrank",
      "54": "Malphite",
      "254": "Vi",
      "50": "Swain"
   }

# LOL API credentials
api_keys = {
  "na": "268306a5-a526-4535-800c-623be8313f74",
  "euw": "71be2bcb-e5de-4784-bede-3573498311f2"
}

http_method = "GET"
http_handler = urllib.HTTPHandler()

G_loglevel=0


# Fore, Back and Style are convenience classes for the constant ANSI strings that set
#     the foreground, background and style. The don't have any magic of their own.
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

NAMES = {
    Fore.BLACK: 'black', Fore.RED: 'red', Fore.GREEN: 'green', Fore.YELLOW: 'yellow', Fore.BLUE: 'blue', Fore.MAGENTA: 'magenta', Fore.CYAN: 'cyan', Fore.WHITE: 'white'
    , Fore.RESET: 'reset',
    Back.BLACK: 'black', Back.RED: 'red', Back.GREEN: 'green', Back.YELLOW: 'yellow', Back.BLUE: 'blue', Back.MAGENTA: 'magenta', Back.CYAN: 'cyan', Back.WHITE: 'white',
    Back.RESET: 'reset'
}

init()

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
    print "getJSONResponse2 context",context + ": httpresponse is " + str(httpresponse)

  jsonresponse = httpresponse.read()
  if G_loglevel > 70:
    print "getJSONResponse3 context",context + ": json raw response is " + str(jsonresponse)

  try:
    j1 = json.loads(jsonresponse)
  except Exception, e:
    return False,"JSonError"+str(e)

  if G_loglevel > 60:
    print "getJSONResponse4 context",context + ": json pythonized resp is " + str(j1)

  return True,j1

def get_champion_name_static(id):
  for key,value in champion_names.items():
    if key==id:
      return value
  return "???"

def get_champion_name_dynamic(id, region):
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
    print "Won?\tGameID\tWhen\tMins\tGameType\tSubType\tMode\tLvl" \
      "\tChampion\tDamTC\tGEarn\tGSold\tKMni\tKTur\tKill\tDeth\tAsst"
  else:
    print "Won?   GameID     When                   Mins GameType     " + \
      "   SubType              Mode      Lvl" \
      " Champion        DamTC GEarn GSold KMni KTur Kill Deth Asst"

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
    championName = get_champion_name_static(str(championId))

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

    # win/loss in color
    winloss=string.ljust(str(stats["win"]), 6);
    if winloss=="True  ":
      # green
      sys.stdout.write('%s%-6s%s' % (Back.GREEN,winloss, Back.RESET))
    else:
      # red
      sys.stdout.write('%s%-6s%s' % (Back.RED,winloss,Back.RESET))

    print \
        string.rjust(str(gamenum), 2) + SEP + \
        TXT + gametime + TXT + SEP + \
        str(minutes) + SEP + \
        string.ljust(str(game["gameType"]), 15) + SEP + \
        string.ljust(str(game["subType"]), 20) + SEP + \
        string.ljust(game["gameMode"], 10) + SEP + \
        string.rjust(str(game["level"]), 2) + SEP + \
        string.ljust(championName, 15) + SEP + \
        string.rjust(str(pd), 5) + SEP + \
        string.rjust(str(safeGetStats(stats,"goldEarned")), 5) + SEP + \
        string.rjust(str(safeGetStats(stats,"goldSpent")), 5) + SEP + \
        string.rjust(str(safeGetStats(stats,"minionsKilled")), 4) + SEP + \
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
  input=input.upper();
  if input=="JSON" or input=="TXT" or input=="HUMAN":
    return input
  else:
    print "illegal value '"+input+"' for <output format>"
    sys.exit()

def collect_data_mode_2():
  # mode 2
  global G_loglevel

  try:
    starting_match_id = int(sys.argv[2])
    region = sys.argv[3]
    pull_interval_ms = int(sys.argv[4])
    output_format=get_output_format(sys.argv[5])
    G_loglevel = int(sys.argv[6])
  except Exception, e:
    usage(2)
    sys.exit()

  print "mode 2 - data collecting mode: starting match id ",starting_match_id,\
        ", pull interval ",pull_interval_ms,"ms" \
        ", region ",region,", loglevel ",G_loglevel

  pull_loop(starting_match_id, pull_interval_ms, region, output_format)

  sys.exit()

def read_json_data_mode_3():
  # mode 3
  global G_loglevel

  try:
    output_format=get_output_format(sys.argv[2])
    G_loglevel = int(sys.argv[3])
  except Exception, e:
    usage(3)
    sys.exit()

  print "mode 3 - read json data from file ",\
        ", output format ",output_format,", loglevel ",G_loglevel

  print "matchId matchCreationNum matchCreationDate Champion"
  # read through stdin
  for line in sys.stdin:
    # raw python json format now in line
    if G_loglevel>80:
      print "read_json_data_mode_3 - 1: Raw  line: <"+line+">"

    # convert back to dict
    mydict=eval(line)

    # time of game
    numtime = mydict["matchCreation"]
    gametime = "\""+time.ctime(numtime/1000)+"\""

    # disect participants
    participants=mydict["participants"]
    for p in participants:
      print mydict["matchId"],numtime,gametime,get_champion_name_static(str(p["championId"]))

def usage(mode):

  if mode==0 or mode==1:

    print "\n\n--- Mode 1: get last 10 games for a summoner ---"
    print   "usage: " + sys.argv[0] + " 1 <name of summoner> <region> <csv> <loglevel>"
    print  "   <csv>   - Y or y for Excel readable format"
    print  "           - any other value for human readable format"

  if mode==0 or mode==2:
    print "\n\n--- Mode 2: slowly gather game data ---"
    print "usage: " + sys.argv[0] + \
          " 2 <starting game id> <region> <pull interval[ms]> <output format> <loglevel>"
    print "    <output format> can be JSON or CSV"

  if mode==0 or mode==3:
    print "\n\n--- Mode 3: read json data and write csv ---"
    print "usage: " + sys.argv[0] + \
          " 3 <output format> <loglevel>"
    print "    <output format> can be CSV or HUMAN"


def hello():
  print NAME, " version ", VERSION

def dummy_main():
  return

if __name__ == '__main__':

  hello()

  try:
    mode=int(sys.argv[1])
  except Exception, e:
    usage(0)
    sys.exit()

  if mode==2:
    # data collecting mode
    collect_data_mode_2()
    sys.exit()
  elif mode==3:
    # read json data
    read_json_data_mode_3()
    sys.exit()

  # mode 1
  # get runtime parameters
  try:
    summoner_name = sys.argv[2]
    region = sys.argv[3]
    do_csv = sys.argv[4]
    G_loglevel = int(sys.argv[5])
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
