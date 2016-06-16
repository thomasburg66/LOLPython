__author__ = 'Thomas'

'''
1.6x: gather all games for specific summoners
1.5x: optionally list co-players in mode 1
1.4x: added color coding, added IP earned
1.3x: read json output (mode 2) and write it in Excel format
1.2x: create local copy of match data in json format
1.1x: pull misc game data by guessing game ids
1.0x: get data for specific summoner
'''

NAME = "LOLPyth"
VERSION = "1.70 - 16Jun2016"

import urllib2 as urllib
import json
import time
import string
import sys

from colorama import init, Fore, Back, Style

dummy_game_list_tb_NA = "1"
'''
W GameID     When                   Mins GameType        SubType              Mode     LvlL Champion    LvlC DamTC GEarn GSold KMni KTur Kill Deth Asst   IP
- ---------- ------------------------ -- ------------------------------------ -------- ---- ---------   ---- ----- ----- ----- ---- ---- ---- ---- ---- ----
N 1889648116 Sat Jul 18 00:02:03 2015 20 MATCHED_GAME    NORMAL               CLASSIC     5 Ziggs          8   214  3653  3840   33    0    0    2    0   63
    levels:    5,3,7,9,5,4,7,7,?69111817?,
    summoners: 68953593,69331960,66061889,56822520,59821370,69321812,69180533,68820435,69111817,
'''

dummy_game_list_tb_EUW = "1"
'''

TB EUW games

W GameID     When                   Mins GameType        SubType              Mode     LvlL Champion    LvlC DamTC GEarn GSold KMni KTur Kill Deth Asst   IP
- ---------- ------------------------ -- ------------------------------------ -------- ---- ---------   ---- ----- ----- ----- ---- ---- ---- ---- ---- ----
N 2204924082 Fri Jul 17 11:32:29 2015 52 CUSTOM_GAME     NONE                 CLASSIC    14 Ziggs         17  5065 11791 17250  125    0    5   13    1    0
Y 2205198825 Fri Jul 17 03:37:38 2015 58 MATCHED_GAME    NORMAL               CLASSIC    14 Ziggs         18  3446 13994 17050   93    0    4   16   13  295
Y 2205190699 Fri Jul 17 02:30:40 2015 35 MATCHED_GAME    NORMAL               CLASSIC    13 Ziggs         14   385  8642  7075   75    1    1    4    3   99
N 2205143769 Fri Jul 17 01:39:52 2015 43 MATCHED_GAME    NORMAL               CLASSIC    13 Ziggs         17  3830 12834 11075  125    0    6    7   12   77
N 2205083368 Fri Jul 17 00:33:09 2015 43 MATCHED_GAME    NORMAL               CLASSIC    13 Ziggs         16  1981 11200 13475  120    0    2   10    8   77
N 2205015157 Thu Jul 16 23:36:48 2015 31 MATCHED_GAME    NORMAL               CLASSIC    13 Ziggs         13  1299  6926  7625   80    0    1    7    3   60
N 2204940713 Thu Jul 16 22:23:09 2015 18 MATCHED_GAME    ODIN_UNRANKED        ODIN       13 Ziggs         15  2259 10579 10900   20    0    6    7    1   45
N 2204883052 Thu Jul 16 21:58:32 2015 13 MATCHED_GAME    ODIN_UNRANKED        ODIN       13 Gnar          12  4498  7129  7825    3    0    4    8    2   34
Y 2204325865 Thu Jul 16 18:17:12 2015  8 MATCHED_GAME    ODIN_UNRANKED        ODIN       13 Ziggs         10  1141  5070  3300   10    0    6    0    4   39
N 2203867696 Thu Jul 16 06:28:44 2015 16 MATCHED_GAME    ODIN_UNRANKED        ODIN       13 Ziggs         15  2256  8827  8600   12    0    4    5   11   41


W GameID     When                   Mins GameType        SubType              Mode     LvlL Champion    LvlC DamTC GEarn GSold KMni KTur Kill Deth Asst   IP
- ---------- ------------------------ -- ------------------------------------ -------- ---- ---------   ---- ----- ----- ----- ---- ---- ---- ---- ---- ----
Y 2206349197 Fri Jul 17 22:35:10 2015 10 MATCHED_GAME    ODIN_UNRANKED        ODIN       14 Ziggs         11   784  5607  3500   10    0    3    1    0   44
    levels:    18,21,21,20,18,21,18,21,?75667631?,
    summoners: 75967202,75440808,75432691,75857718,76017591,75302890,75512727,75987243,75667631,

'''

dummy_match_json_data = "1"

'''

https://developer.riotgames.com/api/methods

u'gameId': 1343001336, u'championId': 37, u'level': 30,
u'createDate': 1393263989033L, u'gameMode': u'ARAM', u'mapId': 12,
u'gameType': u'MATCHED_GAME', u'subType': u'ARAM_UNRANKED_5x5',
u'teamId': 200, u'invalid': False, u'ipEarned': 220,

u'fellowPlayers':

[

  {u'teamId': 200, u'championId': 143, u'summonerId': 22791283},
  {u'teamId': 100, u'championId': 24, u'summonerId': 20130360},
  {u'teamId': 100, u'championId': 40, u'summonerId': 44188584},
  {u'teamId': 200, u'championId': 92, u'summonerId': 31652931},
  {u'teamId': 200, u'championId': 101, u'summonerId': 21043585},
  {u'teamId': 100, u'championId': 60, u'summonerId': 19635022},
  {u'teamId': 200, u'championId': 114, u'summonerId': 20812831},
  {u'teamId': 100, u'championId': 98, u'summonerId': 27704461},
  {u'teamId': 100, u'championId': 18, u'summonerId': 20906123}

]

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
champion_names = {
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

G_loglevel = 0

# Fore, Back and Style are convenience classes for the constant ANSI strings that set
#     the foreground, background and style. The don't have any magic of their own.
FORES = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
BACKS = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
STYLES = [Style.DIM, Style.NORMAL, Style.BRIGHT]

NAMES = {
    Fore.BLACK: 'black', Fore.RED: 'red', Fore.GREEN: 'green', Fore.YELLOW: 'yellow', Fore.BLUE: 'blue',
    Fore.MAGENTA: 'magenta', Fore.CYAN: 'cyan', Fore.WHITE: 'white'
    , Fore.RESET: 'reset',
    Back.BLACK: 'black', Back.RED: 'red', Back.GREEN: 'green', Back.YELLOW: 'yellow', Back.BLUE: 'blue',
    Back.MAGENTA: 'magenta', Back.CYAN: 'cyan', Back.WHITE: 'white',
    Back.RESET: 'reset'
}

RUN_MODES = {
    1: {"LIST", "List games"},
    2: {"COLLECT", "Collect all games"},
    3: {"READJSON", "Read JSON file"},
    4: {"SUMSEARCH", "Search for specific Summoner's games"},
    5: {"CHAMPIONINFO", "Get Info for a specific Champion"}
}

RUN_MODE_LIST = 1
RUN_MODE_COLLECT = 2
RUN_MODE_READJSON = 3
RUN_MODE_SUMSEARCH = 4
RUN_MODE_CHAMPIONINFO = 5

init()

G_loglevel=99



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


def getJSONResponse(region, context, url_end):
    # return success, then return val or error string

    if region == "na":
        full_url = "https://na.api.pvp.net/" + url_end
    elif region == "euw":
        full_url = "https://euw.api.pvp.net/" + url_end
    elif region == "global":
        full_url = "https://global.api.pvp.net/api/lol/static-data" + url_end
    else:
        print"unknown region"
        sys.exit()

    if G_loglevel > 40:
        print "getJSONResponse1 url is " + full_url

    try:
        httpresponse = urllib.urlopen(full_url)
    except Exception, e:
        if G_loglevel > 10:
            print "http error ", e, "continuing..."
        return False, "HTTP error" + str(e)

    if G_loglevel > 80:
        print "getJSONResponse2 context", context + ": httpresponse is " + str(httpresponse)

    jsonresponse = httpresponse.read()
    if G_loglevel > 70:
        print "getJSONResponse3 context", context + ": json raw response is \n\n===== BEGIN JSON====\n\n" + str(jsonresponse) + "\n===== END JSON====\n\n"

    try:
        j1 = json.loads(jsonresponse)
    except Exception, e:
        return False, "JSonError" + str(e)

    if G_loglevel > 80:
        print "getJSONResponse4 context", context + ": json pythonized resp is " + str(j1)

    return True, j1


def get_champion_name_static(id):
    for key, value in champion_names.items():
        if key == id:
            return value
    return "???"

def get_champion_id_static(name):
    for key, value in champion_names.items():
        if value == name:
            return key
    return "???"



'''
{"68953593": {
   "id": 68953593,
   "name": "akoceeryan",
   "profileIconId": 28,
   "revisionDate": 1437170523000,
   "summonerLevel": 5
}}'''


def get_summoner_info_dynamic(id, region):
    url_end = "api/lol/" + region + "/v1.4/summoner/"
    url_end = url_end + str(id)
    url_end = url_end + "?" + get_api_key(region)
    success, resp = getJSONResponse(region, "get_summoner_name", url_end)
    if not success:
        return "?", "?"
    sumdata = resp[str(id)]
    return sumdata["summonerLevel"], sumdata["name"]


def get_champion_name_dynamic(id, region):
    url_end = "api/lol/" + region + "/v1.2/champion/"
    url_end = url_end + str(id)
    url_end = url_end + "?" + get_api_key(region)
    success, resp = getJSONResponse("global", "get_champion_name", url_end)
    if not success:
        print "oops - champion not found"
        sys.exit()
    return resp["name"]


def getSummonerId(name, region):
    url_end = "api/lol/" + region + \
              "/v1.4/summoner/by-name/" + name + \
              "?" + get_api_key(region)
    success, resp = getJSONResponse(region, "getSummonerId", url_end)
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


def printSummonerGameList(id, region, do_csv, do_show_summoner_data):
    url1 = "api/lol/" + region + "/v1.3/game/by-summoner/"
    url2 = "/recent?" + get_api_key(region)
    url = url1 + str(id) + url2

    success, resp = getJSONResponse(region, "printSummonerGameList", url)
    if not success:
        print "oops - gamelist not found"
        sys.exit()

    gamelist = resp["games"]
    if G_loglevel > 30:
        Linefeed()
        print "+++ gamelist is: <" + str(gamelist) + ">"

    if do_csv:
        print "Won?\tGameID\tWhen\tMins\tGameType\tSubType\tMode\tLvlL" \
              "\tChampion\tLvlC\tDamTC\tGEarn\tGSold\tKMni\tKTur\tKill\tDeth\tAsst\tIP"
    else:
        sys.stdout.write('%s' % (Back.BLUE))
        print \
            "W GameID     When                   Mins GameType        " + \
            "SubType              Mode     LvlL " \
            "Champion    LvlC DamTC GEarn GSold KMni KTur Kill Deth Asst   IP"

    if not do_csv:
        print \
            "- ---------- ------------------------ -- ----------------" + \
            "-------------------- -------- ---- " \
            "---------   ---- ----- ----- ----- ---- ---- ---- ---- ---- ----"
        sys.stdout.write('%s' % (Back.RESET))

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
        minutes = string.rjust(str(int(stats["timePlayed"]) / 60), 2)

        numtime = game["createDate"] / 1000
        gametime = time.ctime(numtime)

        # and print it
        if do_csv:
            TXT = "\""
            SEP = "\t"
        else:
            TXT = ""
            SEP = " "

        # win/loss in color
        winloss = string.ljust(str(stats["win"]), 6);
        if winloss == "True  ":
            # green
            sys.stdout.write('%s' % (Back.GREEN))
            winloss = "Y"
        else:
            # red
            sys.stdout.write('%s' % (Back.RED))
            winloss = "N"

        print \
            winloss + SEP + \
            string.rjust(str(game["gameId"]), 2) + SEP + \
            TXT + gametime + TXT + SEP + \
            str(minutes) + SEP + \
            string.ljust(str(game["gameType"]), 15) + SEP + \
            string.ljust(str(game["subType"]), 20) + SEP + \
            string.ljust(game["gameMode"], 10) + SEP + \
            string.rjust(str(game["level"]), 2) + SEP + \
            string.ljust(championName, 10) + SEP + \
            string.rjust(str(safeGetStats(stats, "level")), 5) + SEP + \
            string.rjust(str(safeGetStats(stats, "physicalDamageDealtToChampions")), 5) + SEP + \
            string.rjust(str(safeGetStats(stats, "goldEarned")), 5) + SEP + \
            string.rjust(str(safeGetStats(stats, "goldSpent")), 5) + SEP + \
            string.rjust(str(safeGetStats(stats, "minionsKilled")), 4) + SEP + \
            string.rjust(str(safeGetStats(stats, "turretsKilled")), 4) + SEP + \
            string.rjust(str(safeGetStats(stats, "championsKilled")), 4) + SEP + \
            string.rjust(str(safeGetStats(stats, "numDeaths")), 4) + SEP + \
            string.rjust(str(safeGetStats(stats, "assists")), 4) + SEP + \
            string.rjust(str(game["ipEarned"]), 4)

        if do_show_summoner_data:
            # optionally: print list of summoners: id/name/level
            try:
                player_list = game["fellowPlayers"]
                sumidlist = "    sum ids:   "
                sumnamelist = "    sum names: "
                levlist = "    levels:    "
                for p in player_list:
                    thisid = p["summonerId"]
                    sumidlist = sumidlist + str(thisid) + ","
                    level, name = get_summoner_info_dynamic(thisid, region)
                    levlist = levlist + str(level) + ","
                    sumnamelist = sumnamelist + name + ","

                #        if G_loglevel>40:
                print sumidlist
                print sumnamelist
                print levlist
            except Exception, e:
                # ignore mistake
                print "--- fellow players not found"

        # increase counter
        gamenum = gamenum - 1

        # be a good LOL API citizen
        time.sleep(1 / 8)

import sys
def printf(format, *args):
    sys.stdout.write(format % args)

# /api/lol/static-data/{region}/v1.2/champion/{id}
def process_champion_data(json_data,output_format):
    # gather info
    champ_name=json_data["name"]
    champ_title=json_data["title"]
    ally_tips=json_data["allytips"][0]
    enemy_tips=json_data["enemytips"][0]
    # some massaging on tags
    tags_raw=json_data["tags"]
    tags=""
    for t in tags_raw:
        tags=tags + " " + t

    # print it
    if output_format=="HUMAN":
        if G_loglevel > 5:
            print "\n\n============================================================================="

        printf("%-10s,\"%-25s,\"%-20s\"\n", champ_name , champ_title, tags)

        if G_loglevel > 5:
            print "\n===Ally Tips ==="
            print ally_tips

            print "\n===Enemy Tips==="
            print enemy_tips

# /api/lol/{region}/v2.2/match/
def process_match(mode, match_id, region, output_format, sumlist):
    url_end = "api/lol/" + region + \
              "/v2.2/match/" + str(match_id) + \
              "?" + get_api_key(region)

    success, resp = getJSONResponse(region, "process_match", url_end)
    if not success:
        # match not found: keep going
        return success

    if G_loglevel > 100:
        print resp

    sep1 = ' '
    txt1 = "\""

    if output_format == "JSON":
        print resp
    else:
        if mode == RUN_MODE_COLLECT:
            print match_id, \
                "\"" + str(time.ctime(resp["matchCreation"] / 1000)) + "\"", \
                resp["matchCreation"], \
                resp["matchDuration"], \
                resp["mapId"], \
                resp["matchVersion"], \
                resp["queueType"], resp["matchMode"], resp["matchType"]
        elif mode == RUN_MODE_SUMSEARCH:
            # go through all sum ids in match, look for match, process only if match
            try:
                player_list = resp["fellowPlayers"]
                if G_loglevel > 40:
                    print "player list is: ", player_list
                for p in player_list:
                    thisid = p["summonerId"]
                    level, name = get_summoner_info_dynamic(thisid, region)
                try:
                    if sumlist.index(thisid):
                        print "### found game!!! ", match_id
                except Exception, e:
                    # summoner not found, ignore
                    print "sum not found"
            except Exception, e:
                # ignore mistake
                print "--- fellow players not found"

    return True


def pull_loop(mode, starting_match_id, ending_match_id, pull_interval_ms, region, output_format, sumlist):
    match_id = starting_match_id
    is_done = False

    while not is_done:
        # get next match
        success = process_match(mode, match_id, region, output_format, sumlist)

        # wait a bit
        time.sleep(pull_interval_ms / 1000)

        # next match
        match_id = match_id + 1


def get_output_format(input):
    input = input.upper();
    if input == "JSON" or input == "TXT" or input == "HUMAN":
        return input
    else:
        print "illegal value '" + input + "' for <output format>"
        sys.exit()


def list_last_games_mode_1():
    # mode 1
    # get runtime parameters
    try:
        summoner_name = sys.argv[2]
        region = sys.argv[3]
        do_csv = sys.argv[4]
        do_show_summoner_data = sys.argv[5]
        set_loglevel(int(sys.argv[6]))
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
        print " "

    if do_show_summoner_data == "y" or do_show_summoner_data == "Y":
        do_show_summoner_data = True
    else:
        do_show_summoner_data = False

    # convert to id
    id = getSummonerId(summoner_name, region)

    # get stats
    printSummonerGameList(id, region, do_csv, do_show_summoner_data)


def collect_data_mode_2():
    # mode 2

    try:
        starting_match_id = int(sys.argv[2])
        region = sys.argv[3]
        pull_interval_ms = int(sys.argv[4])
        output_format = get_output_format(sys.argv[5])
        set_loglevel(int(sys.argv[6]))
    except Exception, e:
        usage(2)
        sys.exit()

    print "mode 2 - data collecting mode: starting match id ", starting_match_id, \
        ", pull interval ", pull_interval_ms, "ms" \
                                              ", region ", region, ", loglevel ", G_loglevel

    pull_loop(starting_match_id, pull_interval_ms, region, output_format)

    sys.exit()


def read_json_data_mode_3():

    try:
        output_format = get_output_format(sys.argv[2])
        set_loglevel(int(sys.argv[3]))
    except Exception, e:
        usage(3)
        sys.exit()

    print "mode 3 - read json data from file ", \
        ", output format ", output_format, ", loglevel ", G_loglevel

    print "matchId matchCreationNum matchCreationDate Champion"
    # read through stdin
    for line in sys.stdin:
        # raw python json format now in line
        if G_loglevel > 80:
            print "read_json_data_mode_3 - 1: Raw  line: <" + line + ">"

        # convert back to dict
        mydict = eval(line)

        # time of game
        numtime = mydict["matchCreation"]
        gametime = "\"" + time.ctime(numtime / 1000) + "\""

        # disect participants
        participants = mydict["participants"]
        for p in participants:
            print mydict["matchId"], numtime, gametime, get_champion_name_static(str(p["championId"]))


def collect_my_games_mode_4():

    # list of summoners to go through
    sumname_list = []

    # get runtime args
    try:
        starting_match_id = int(sys.argv[2])
        ending_match_id = int(sys.argv[3])
        region = sys.argv[4]
        pull_interval_ms = int(sys.argv[5])
        output_format = get_output_format(sys.argv[6])
        set_loglevel(int(sys.argv[7]))
        for i in range(8, len(sys.argv)):
            sumname_list.append(sys.argv[i])

    except Exception, e:
        print "argv is ", sys.argv
        print "argv.count() is ", len(sys.argv)
        usage(4)
        sys.exit()

    print "--- mode 4 - collecting games for the following summoners: "
    for s in sumname_list:
        print "   ", s

    pull_loop(RUN_MODE_SUMSEARCH, starting_match_id, ending_match_id,
              pull_interval_ms, region, output_format, sumname_list)

def get_champion_info_5():

    # list of summoners to go through
    sumname_list = []

    # get runtime args
    try:
        output_format = get_output_format(sys.argv[2])
        set_loglevel(int(sys.argv[3]))
        for i in range(4, len(sys.argv)):
            sumname_list.append(sys.argv[i])

    except Exception, e:
        print "argv is ", sys.argv
        print "argv.count() is ", len(sys.argv)
        usage(5)
        sys.exit()

    print "--- mode 5 - collecting games for the following summoners: "
    for s in sumname_list:
        print "   ", s

    # now do the work
    for s in sumname_list:
        # capitalize first character, find id
        sumname=s[0].upper()+s[1:]
        champion_id=get_champion_id_static(sumname)
        if G_loglevel>40:
            print sumname, "has id ", champion_id

        # call JSNON to get info
        region="euw"
        url_end = "/"+region+"/v1.2/champion/"
        url_end = url_end + str(champion_id) + "?champData=all"
        url_end = url_end + "&" + get_api_key(region)
        success, resp = getJSONResponse("global", "get_champion_name", url_end)
        if not success:
            print "oops - champion not found"
            sys.exit()

        # and process the info
        process_champion_data(resp,output_format)


def print_allowed_output_formats(mode):
    if mode == 1 or mode == 3 or mode == 5:
        print "    <output format> can be CSV or HUMAN"
    elif mode == 2 or mode == 4:
        print "    <output format> can be CSV or HUMAN or JSON"

def set_loglevel(level):
    global G_loglevel
    G_loglevel=level

def usage(mode):

    print "\n\n==================================================================================================="
    print "="
    print "="

    if mode == 0 or mode == 1:
        print "\n\n--- Mode 1: get last 10 games for a summoner ---"
        print   "usage: " + sys.argv[0] + " 1 <name of summoner> <region> <output format> <show summoners> <loglevel>"
        print_allowed_output_formats(1)
        print  "           - any other value for human readable format"
        print  "   <show summoners> - Y or y to display other summoners and levels"

    if mode == 0 or mode == 2:
        print "\n\n--- Mode 2: slowly gather game data ---"
        print "usage: " + sys.argv[0] + \
              " 2 <starting game id> <region> <pull interval[ms]> <output format> <loglevel>"
        print_allowed_output_formats(2)

    if mode == 0 or mode == 3:
        print "\n\n--- Mode 3: read json data and write csv ---"
        print "usage: " + sys.argv[0] + \
              " 3 <output format> <loglevel>"
        print_allowed_output_formats(3)

    if mode == 0 or mode == 4:
        print "\n\n--- Mode 4: gather game data for specific summoners ---"
        print "usage: " + sys.argv[0] + \
              " 4 <starting game id> <ending game id> <region> <pull interval[ms]> <output format> <loglevel>" \
              "<sumname1> [<sumname2> ... <sumnameN>]"
        print_allowed_output_formats(4)

    if mode == 0 or mode == 5:
        print "\n\n--- Mode 5: gather info for a champion ---"
        print "usage: " + sys.argv[0] + \
              " 5 <output format> <loglevel>"
        "<sumname1> [<sumname2> ... <sumnameN>]"
        print_allowed_output_formats(5)

    print "\n="
    print "="
    print "===================================================================================================\n\n"


def hello():
    print NAME, " version ", VERSION


def dummy_main():
    return


if __name__ == '__main__':

    hello()

    try:
        mode = int(sys.argv[1])
    except Exception, e:
        usage(0)
        sys.exit()

    if mode == 1:
        # show last games
        list_last_games_mode_1()

    if mode == 2:
        # data collecting mode: every game
        collect_data_mode_2()

    elif mode == 3:
        # read json data
        read_json_data_mode_3()

    elif mode == 4:
        # data collection: only for specific summoners
        collect_my_games_mode_4()

    elif mode == 5:
        get_champion_info_5()
