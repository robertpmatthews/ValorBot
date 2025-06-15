from riotwatcher import LolWatcher, TftWatcher
import Credentials
import LiveGame
from requests import HTTPError
import requests
import math
# List of games currently added to game list (games on game list receive patch notes and live tweets)
# Initializing the global variables tweetdict and patchdict
tweetdict = {}
patchdict = {}
# Accessing the Riot API for League of Legends and TFT respectively
lol_watcher = LolWatcher(Credentials.LOLAPIKey)
tft_watcher = TftWatcher(Credentials.TFTAPIKey)


'''
This function takes in an input of the player name and the returns the rank in solo queue if the name is found
Param: 2 str: name - The summoner name, my_region - the region of that summoner
Returns: List - Solo queue rank as the first element and WR as the second third is mini series, and flex queue rank as 
the fourth element and WR as the fifth and minseries as the sixth
'''


def getranklol(name, my_region):
    try:
        summoner = lol_watcher.summoner.by_name(my_region, name)
        summonerstat = lol_watcher.league.by_summoner(my_region, summoner['id'])
        display_info = ['', '', '', '', '', '', '', '']
        display_info[6] = short_live_match(my_region, summoner['id'], name)
        display_info[7] = get_mastery(summoner['id'],my_region)
        for values in summonerstat:
            if values['queueType'] == 'RANKED_SOLO_5x5':
                winrate = str(round(values['wins']/(values['wins'] + values['losses'])*100))
                display_info[0] = (Live_Game.find_emojis(values['tier'].lower().capitalize().split()[0]) + ' | '
                                   + values['tier'] + " " + values['rank'] + " " + str(values['leaguePoints']) + " LP")
                display_info[1] = ('Winrate: ' + winrate + '%')
                try:
                    if values['miniSeries']['progress']:
                        promos = ''
                        for letter in values['miniSeries']['progress']:
                            if letter == 'N':
                                promos = promos + ':grey_question:'
                            elif letter == 'W':
                                promos = promos + ':white_check_mark:'
                            else:
                                promos = promos + ':x:'
                        display_info[2] = 'Promos:' + promos
                except KeyError:
                    pass
            if values['queueType'] == 'RANKED_FLEX_SR':
                winrate = str(round(values['wins'] / (values['wins'] + values['losses']) * 100))
                display_info[3] = (Live_Game.find_emojis(values['tier'].lower().capitalize().split()[0]) + ' | '
                                   + values['tier'] + " " + values['rank'] + " " + str(values['leaguePoints']) + " LP")
                display_info[4] = ('Winrate: ' + winrate + '%')
                try:
                    if values['miniSeries']['progress']:
                        promos = ''
                        for letter in values['miniSeries']['progress']:
                            if letter == 'N':
                                promos = promos + ':grey_question:'
                            elif letter == 'W':
                                promos = promos + ':white_check_mark:'
                            else:
                                promos = promos + ':x:'
                        display_info[5] = 'Promos:' + promos
                except KeyError:
                    pass
        if display_info[0] == '':
            display_info[0] = 'Solo queue rank not found'
        if display_info[3] == '':
            display_info[3] = 'Flex queue rank not found'
        return display_info
    except HTTPError:
        return "Summoner name {} not found".format(name)


'''
This function takes in an input of the player name and the returns the rank in TFT if the name is found
Param: 2 str: name - The summoner name, my_region - the region of that summoner
Returns: List - TFT Rank as the first element, The rank of the player as the second, and the TFT rank as the third
'''


def get_rank_tft(name, my_region):
    try:
        summonertft = tft_watcher.summoner.by_name(my_region, name)
        summonerstattft = tft_watcher.league.by_summoner(my_region, summonertft['id'])
        display_info = ['', '', '']
        for values in summonerstattft:
            if values['queueType'] == 'RANKED_TFT':
                display_info[0] = (Live_Game.find_emojis(values['tier'].lower().capitalize().split()[0]) + ' | '
                                   + values['tier'] + " " + values['rank'] + " " + str(values['leaguePoints']) + " LP")
                display_info[1] = ('Wins: ' + str(values['wins']))
        if display_info[0] == '':
            display_info[0] = 'TFT rank not found'
        return display_info
    except HTTPError:
        return "Summoner name {} not found".format(name)


'''
This is a helper function to give a shorter version of live match
Param: 3 str - The region, summoner id, and name
Returns: a string representing the live game status of a user
'''


def short_live_match(my_region, summonerid, name):
    try:
        queuetypes = requests.get('http://static.developer.riotgames.com/docs/lol/queues.json')
        queuetypes = queuetypes.json()
        match = lol_watcher.spectator.by_summoner(my_region, summonerid)
        description = ''
        for queuetype in queuetypes:
            try:
                if match['gameQueueConfigId'] == queuetype['queueId']:
                    description = queuetype['description'][:-6]  # description of game-mode
            except KeyError:
                description = 'Custom'
            if description != '':
                break
        minutes = math.floor(match['gameLength'] / 60) + 3
        seconds = str(match['gameLength'] % 60)
        if len(seconds) == 1:
            seconds = '0' + seconds
        gamelength = str(minutes) + ':' + seconds
        emoji = ''
        champion = ''
        for player in match['participants']:
            if player['summonerId'] == summonerid:
                emoji = Live_Game.find_emojis(Live_Game.find_champion(str(player['championId'])))
                champion = Live_Game.find_champion(str(player['championId']))
        matchinfo = '{} is in a {} match playing {}|{} and is {} in game'.format(name, description, emoji, champion,
                                                                                 gamelength)
        return matchinfo
    except HTTPError:
        return "{} not in a live match".format(name)


'''
Enables tweets on a certain channel in a discord guild
Input: game (str) - The game that the player is requesting tweets for. channel (channel object) - The channel that the
user wishes to send those tweets to, and tweetdict - The tweet dictionary so that it will enabled tweets on for that
specified game. 
'''


def send_tweets(game, channel, tweetdict):
    if game.lower() == 'lol' or game.lower() == 'league' or game.lower() == 'league of legends':
        tweetdict["League of Legends"] = channel.id
        return "Sending League of Legends tweets to " + channel.name + "!"
    elif game.lower() == 'tft' or game.lower() == 'teamfight tactics' or game.lower() == 'team fight tactics':
        tweetdict['Teamfight Tactics'] = channel.id
        return "Sending Teamfight Tactics tweets to " + channel.name + "!"
    elif game == 'Valorant' or game.lower() == 'val' or game.lower() == 'valorant' or game == 'Val':
        tweetdict["Valorant"] = channel.id
        return "Sending Valorant tweets to " + channel.name + "!"
    elif game == 'LoR' or game == 'Legends Of Runeterra' or game.lower() == 'lor' or game.lower() == \
            'legends of runeterra':
        tweetdict["Legends of Runeterra"] = channel.id
        return "Sending Legends of Runeterra tweets to " + channel.name + "!"
    elif game == 'Riot' or game == 'Rito' or game.lower() == 'riot' or game.lower() == 'riot games':
        tweetdict["Riot Games"] = channel.id
        return "Sending Riot Games tweets to " + channel.name + "!"
    else:
        return "Sorry, that isn't a valid game. See ?helpsetup for valid games."


'''
Disables tweets on a certain channel in a discord guild
Input: game (str) - The game that the player is requesting tweets patches to be removed from. channel (channel object) -
The channel that the user wishes to stop those tweets from sending, and tweetdict - The tweet dictionary so that it 
will disable tweets for that specified game. 
Output: str - A string that will inform the user that tweets are disabled
'''


def stop_tweets(game, channel, tweetdict):
    if game == 'LoL' or game.lower() == 'league' or game.lower() == 'league of legends' or game.lower() == 'lol':
        tweetdict["League of Legends"] = 0
        return "No longer sending League of Legends tweets to " + channel.name + "!"
    elif game == 'TFT' or game == 'Teamfight Tactics' or game == 'Team fight Tactics' or game.lower() == 'tft' or \
            game.lower() == 'team fight tactics' or game.lower() == 'teamfight tactics':
        tweetdict['Teamfight Tactics'] = 0
        return "No longer sending Teamfight Tactics tweets to " + channel.name + "!"
    elif game == 'Valorant' or game.lower() == 'val' or game.lower() == 'valorant' or game == 'Val':
        tweetdict["Valorant"] = 0
        return "No longer sending Valorant tweets to " + channel.name + "!"
    elif game == 'LoR' or game == 'Legends Of Runeterra' or game.lower() == 'lor' \
            or game.lower() == 'legends of runeterra':
        tweetdict["Legends of Runeterra"] = 0
        return "No longer sending Legends of Runeterra tweets to " + channel.name + "!"
    elif game == 'Riot' or game == 'Rito' or game.lower() == 'riot' or game.lower() == 'riot games':
        tweetdict["Riot Games"] = 0
        return "No longer sending Riot Games tweets to " + channel.name + "!"
    else:
        return "Sorry, that isn't a valid game. See ?helpsetup for valid games."


'''
Enables patches on a certain channel in a discord guild
Input: game (str) - The game that the player is requesting patches for. channel (channel object) - The channel that the
user wishes to send those patches to, and patchdict - The tweet dictionary so that it will enabled patches on for that
specified game. 
Output: str - A string that will inform the user that patches are enabled
'''


def send_patch(game, channel, patchdict):
    if game == 'LoL' or game.lower() == 'league' or game.lower() == 'league of legends' or game.lower() == 'lol':
        patchdict["League of Legends"] = channel.id
        return "Sending League of Legends live patch notes to " + channel.name + "!"
    elif game == 'TFT' or game == 'Teamfight Tactics' or game == 'Team fight Tactics' or game.lower() == 'tft' \
            or game.lower() == 'team fight tactics' or game.lower() == 'teamfight tactics':
        patchdict["Teamfight Tactics"] = channel.id
        return "Sending Teamfight Tactics live patch notes to " + channel.name + "!"
    elif game == 'Valorant' or game.lower() == 'val' or game.lower() == 'valorant' or game == 'Val':
        patchdict["Valorant"] = channel.id
        return "Sending Valorant live patch notes to " + channel.name + "!"
    else:
        return "Sorry, that isn't a valid game. See ?helpsetup for valid games."


'''
Disables patches on a certain channel in a discord guild
Input: game (str) - The game that the player is requesting patches for to be removed from. channel (channel object) - 
The channel that the user wishes to stop those patches from sending, and patchdict - The patch dictionary so that it 
will enabled patches on for that specified game. 
Output: str - A string that will inform the user that patches are disabled
'''


def stop_patch(game, channel, patchdict):
    if game == 'LoL' or game.lower() == 'league' or game.lower() == 'league of legends' or game.lower() == 'lol':
        patchdict["League of Legends"] = 0
        return "No longer sending League of Legends patch notes to " + channel.name + "!"
    elif game == 'TFT' or game == 'Teamfight Tactics' or game == 'Team fight Tactics' or game.lower() == 'tft' \
            or game.lower() == 'team fight tactics' or game.lower() == 'teamfight tactics':
        patchdict['Teamfight Tactics'] = 0
        return "No longer sending Teamfight Tactics patch notes to " + channel.name + "!"
    elif game == 'Valorant' or game.lower() == 'val' or game.lower() == 'valorant' or game == 'Val':
        patchdict["Valorant"] = 0
        return "No longer sending Valorant patch notes to " + channel.name + "!"
    else:
        return "Sorry, that isn't a valid game. See ?helpsetup for valid games."


'''
This displays the games for which the live patch notes are enabled in a string for the user to see
Param: Dict - A dictionary of the servers patchdict, a dictionary of which games are enabled for live patch notes
Returns: str - A string that tells them what games have active live tweets in an easy to read sentence.  
'''


def patchnotes(thepatchdict):
    games = ''
    for game, enabled in thepatchdict.items():
        if enabled:
            games = games + game + ", "

    if games == '':
        return "You are currently not following any live patch notes."
    games = games[:-2]
    games = "You are currently getting live patch notes from the following games: " + games
    return games


'''
This displays the games for which the tweets are enabled in a string for the user to see
Param: Dict - A dictionary of the servers patchdict, a dictionary of which games are enabled for tweets notes
Returns: str - A string that tells them what games have active live patch notes in an easy to read sentence.   
'''


def tweets(thetweetdict):
    games = ''
    for game, enabled in thetweetdict.items():
        if enabled:
            games = games + game + ", "

    if games == '':
        return "You are currently not following any tweets."
    games = games[:-2]
    games = "You are currently getting tweets from the following games: " + games
    return games


'''
This function will take in a dictionary, this dictionary should contain a string key of the player name, and then
the values be a list of the players rank and lp. It will then convert this to a numerical value, every rank = 105 points
which starts at iron 4 with a value of 5 to account for being -3 lp when you dodge at 0 lp iron 4. This also allows
for an unranked player to be given a numerical rank value of 0.
@input - players - Dictionary of player names as keys and values being a list of rank and lp
@return - PlayersNumerical - Dictionary of player names as keys and values an integer that corresponds to their 
combined Rank and LP
'''


def numerical_ranks(players):
    players_numerical = {}
    for name, ranks in players.items():
        tempnumericalrank = 0
        if ranks[0] == 'Challenger 1' or ranks[0] == 'Grandmaster 1' or ranks[0] == 'Master 1':
            tempnumericalrank = 2525 + ranks[1]
        if ranks[0] == 'Diamond 1':
            tempnumericalrank = 2420 + ranks[1]
        if ranks[0] == 'Diamond 2':
            tempnumericalrank = 2315 + ranks[1]
        if ranks[0] == 'Diamond 3':
            tempnumericalrank = 2210 + ranks[1]
        if ranks[0] == 'Diamond 4':
            tempnumericalrank = 2105 + ranks[1]
        if ranks[0] == 'Platinum 1':
            tempnumericalrank = 2000 + ranks[1]
        if ranks[0] == 'Platinum 2':
            tempnumericalrank = 1895 + ranks[1]
        if ranks[0] == 'Platinum 3':
            tempnumericalrank = 1790 + ranks[1]
        if ranks[0] == 'Platinum 4':
            tempnumericalrank = 1685 + ranks[1]
        if ranks[0] == 'Gold 1':
            tempnumericalrank = 1580 + ranks[1]
        if ranks[0] == 'Gold 2':
            tempnumericalrank = 1475 + ranks[1]
        if ranks[0] == 'Gold 3':
            tempnumericalrank = 1370 + ranks[1]
        if ranks[0] == 'Gold 4':
            tempnumericalrank = 1265 + ranks[1]
        if ranks[0] == 'Silver 1':
            tempnumericalrank = 1160 + ranks[1]
        if ranks[0] == 'Silver 2':
            tempnumericalrank = 1055 + ranks[1]
        if ranks[0] == 'Silver 3':
            tempnumericalrank = 950 + ranks[1]
        if ranks[0] == 'Silver 4':
            tempnumericalrank = 845 + ranks[1]
        if ranks[0] == 'Bronze 1':
            tempnumericalrank = 740 + ranks[1]
        if ranks[0] == 'Bronze 2':
            tempnumericalrank = 635 + ranks[1]
        if ranks[0] == 'Bronze 3':
            tempnumericalrank = 530 + ranks[1]
        if ranks[0] == 'Bronze 4':
            tempnumericalrank = 425 + ranks[1]
        if ranks[0] == 'Iron 1':
            tempnumericalrank = 320 + ranks[1]
        if ranks[0] == 'Iron 2':
            tempnumericalrank = 215 + ranks[1]
        if ranks[0] == 'Iron 3':
            tempnumericalrank = 110 + ranks[1]
        if ranks[0] == 'Iron 4':
            tempnumericalrank = 5 + ranks[1]
        players_numerical[name] = tempnumericalrank
    return players_numerical


''' This function will take the input of a dictionary that has the player names as keys and their numerical ranks as 
values, and then return a list that has the players names in order for the leaderboard.
@input - Dictionary with keys being the player names and values being the numerical rank
@return -  A list that has the player names in descending order for the leaderboard.
'''


def ordered_list(players_numerical_dict):
    highestplayerlist = []
    while len(players_numerical_dict) != 0:
        highestplayer = ''
        highestplayerrank = -1
        for name, rank in players_numerical_dict.items():
            if highestplayerrank < rank:
                highestplayer = name
                highestplayerrank = rank
        highestplayerlist.append(highestplayer)
        del players_numerical_dict[highestplayer]
    return highestplayerlist


'''
This the tier of the player in LOL based off the summoner name and the region calls get_tier_faster to do all of the 
functions
Param: 2 str - the summoner name and the region
returns: Tuple - of the tiers and LP for solo queue
'''


def get_tier(name, my_region='na1'):
    summoner = lol_watcher.summoner.by_name(my_region, name)
    return get_tier_faster(summoner['id'], my_region)


'''
This the tier of the player in LOL based off the summoner name and the region calls get_tier_faster to do all of the 
functions
Param: 2 str - the summoner name and the region
returns: Tuple - of the tiers and LP in ranked
'''


def get_tier_tft(name, my_region='na1'):
    summoner = tft_watcher.summoner.by_name(my_region, name)
    return get_tier_faster_tft(summoner['id'], my_region)


'''
This the tier of the player in LOL based off the summoner id and the region, helper function to get_tier, also helpful 
to use
in functions where you already have the summoner id to reduce the amount of calls to the Riot API
Param: 2 str - the summoner name and the region
returns: Tuple - of the tiers and LP for solo queue
'''


def get_tier_faster(summonerid, my_region='na1'):
    summonerstat = lol_watcher.league.by_summoner(my_region, summonerid)
    for values in summonerstat:
        if values['queueType'] == 'RANKED_SOLO_5x5':
            if values['rank'] == "I":
                return values["tier"][0] + values["tier"][1:].lower() + " " + str(1), values['leaguePoints']
            elif values['rank'] == "II":
                return values["tier"][0] + values["tier"][1:].lower() + " " + str(2), values['leaguePoints']
            elif values['rank'] == "III":
                return values["tier"][0] + values["tier"][1:].lower() + " " + str(3), values['leaguePoints']
            elif values['rank'] == "IV":
                return values["tier"][0] + values["tier"][1:].lower() + " " + str(4), values['leaguePoints']
    return "", ""


'''
TFT
'''


def get_tier_faster_tft(summonerid, my_region='na1'):
    summonerstat = tft_watcher.league.by_summoner(my_region, summonerid)
    for values in summonerstat:
        if values['queueType'] == 'RANKED_TFT':
            if values['rank'] == "I":
                return values["tier"][0] + values["tier"][1:].lower() + " " + str(1), values['leaguePoints']
            elif values['rank'] == "II":
                return values["tier"][0] + values["tier"][1:].lower() + " " + str(2), values['leaguePoints']
            elif values['rank'] == "III":
                return values["tier"][0] + values["tier"][1:].lower() + " " + str(3), values['leaguePoints']
            elif values['rank'] == "IV":
                return values["tier"][0] + values["tier"][1:].lower() + " " + str(4), values['leaguePoints']
    return "", ""


''''
Converts the region from the Riot API format to a readable format
Input: str - A string of the region in a Riot API format
Output: str - A string of the region in the readable format
'''


def region_converter(region):
    if region == 'na1':
        return 'NA'
    if region == 'euw1':
        return 'EUW'
    if region == 'eun1':
        return 'EUNE'
    if region == 'oc1':
        return 'OCE'
    if region == 'kr':
        return 'KR'
    if region == 'jp1':
        return 'JP'
    if region == 'br1':
        return 'BR'
    if region == 'la1':
        return 'LAN'
    if region == 'la2':
        return 'LAS'
    if region == 'ru':
        return 'RU'
    if region == 'tr1':
        return 'TR'


'''
Converts the region from a readable format to the Riot API format
Input: str - A string of the region in a readable format
Output: str - A string of the region in the Riot API format
'''


def region_converter_backwards(region):
    if region.lower() == 'na':
        return 'na1'
    if region.lower() == 'euw':
        return 'euw1'
    if region.lower() == 'eune':
        return 'eun1'
    if region.lower() == 'oce':
        return 'oc1'
    if region.lower() == 'kr':
        return 'kr'
    if region.lower() == 'jp':
        return 'jp1'
    if region.lower() == 'br':
        return 'br1'
    if region.lower() == 'lan':
        return 'la1'
    if region == 'las':
        return 'la2'
    if region == 'ru':
        return 'ru'
    if region == 'tr':
        return 'tr1'
    else:
        return 'Invalid region. Use ?helpsetup for a list of valid regions!'


'''
Takes in a summonername and the region of that summoner and returns the summoner's id from the Riot API for LoL
Input: 2 str: summonername - The summoners name, and my_region - the region in the Riot API format
Output: str - The summoner_id of a player via the LoL Riot API 
'''


def get_summoner_id(summonername, my_region):
    return lol_watcher.summoner.by_name(my_region, summonername)['id']


'''
Takes in a summonername and the region of that summoner and returns the summoner's id from the Riot API for TFT
Input: 2 str: summonername - The summoners name, and my_region - the region in the Riot API format
Output: str - The summoner_id of a player via the TFT Riot API 
'''


def get_summoner_id_tft(summonername, my_region):
    return tft_watcher.summoner.by_name(my_region, summonername)['id']




def get_mastery(summoner_id,region):
    mastery = lol_watcher.champion_mastery.by_summoner(region, summoner_id)
    my_champs = ''
    for i in range(3):
        mast = ('{:,}'.format(int(mastery[i]["championPoints"])))
        my_champs += Live_Game.find_emojis(Live_Game.find_champion(str(mastery[i]["championId"]))) + "|" + \
                     Live_Game.find_champion(str(mastery[i]["championId"])) + " " + \
                     Live_Game.find_emojis("Mastery" + str(mastery[i]["championLevel"])) \
                     + " " + str(mast) + "\n"

    return my_champs


if __name__ == '__main__':
    print(get_summoner_id('BigBert', 'na1'))
    print(get_mastery("7xhUOoTwv32gTeCzJfijEm4J3iPWfM_L0pt45uSw-_YDHGQ","na1"))
    print(Live_Game.find_champion(str(121)))
