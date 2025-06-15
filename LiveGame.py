from riotwatcher import LolWatcher, TftWatcher
import Credentials
import requests
import math
import json
from Emojis import Emojis

lol_watcher = LolWatcher(Credentials.LOLAPIKey)
tft_watcher = TftWatcher(Credentials.TFTAPIKey)


'''
This function returns the live game that the summoner is in
Param: 2 str - Summoner name and region, assumed to be NA if none is put in.
Returns: List - The match that the summoner is in
'''


def live_match(name, region):
    try:
        summoner = lol_watcher.summoner.by_name(region, name)
    except requests.exceptions.HTTPError:
        return "The summoner {} does not exist".format(name)
    try:
        queuetypes = requests.get('http://static.developer.riotgames.com/docs/lol/queues.json')
        queuetypes = queuetypes.json()
        match = lol_watcher.spectator.by_summoner(region, summoner['id'])
        # finding the game mode
        description = ''
        for queuetype in queuetypes:
            try:
                if match['gameQueueConfigId'] == queuetype['queueId']:
                    description = queuetype['description'][:-6]  # description of game-mode
            except KeyError:
                description = 'Custom'
            if description != '':
                break
        # finding the summoner spell name
        # Calculating game length in minutes and seconds instead of just minutes
        minutes = math.floor(match['gameLength']/60) + 3
        seconds = str(match['gameLength'] % 60)
        if len(seconds) == 1:
            seconds = '0' + seconds
        gamelength = str(minutes) + ':' + seconds
        # Now calculating who is on which team
        team1 = {}
        team2 = {}
        team1count = 1
        team2count = 1
        for player in match['participants']:
            # newplayerdata is in the form Team, Champion, Summoner1, Summoner 2, Primary Rune, Secondary Rune
            newplayerdata = list()
            newplayerdata.append(player['summonerName'])
            newplayerdata.append((find_champion(str(player['championId']))))
            newplayerdata.append(find_summoner_spell(str(player['spell1Id'])))
            newplayerdata.append(find_summoner_spell(str(player['spell2Id'])))
            runes = find_runes(str(player['perks']['perkIds'][0]), str(player['perks']['perkSubStyle']))
            newplayerdata.append(runes[0])
            newplayerdata.append(runes[1])
            newplayerdata.append(player['summonerId'])
            if player['teamId'] == 100:
                team1['player' + str(team1count)] = newplayerdata
                team1count += 1
            else:
                team2['player' + str(team2count)] = newplayerdata
                team2count += 1
        return {'Team 1': team1, 'Team 2': team2, 'gamemode': description, 'gametime': gamelength,
                'gameId': match['gameId'], 'Team 1 count': team1count-1, 'Team 2 count': team2count-1}
    except requests.exceptions.HTTPError:
        return "{} not in a live match".format(name)


'''
Converts a summoner spell id into the summoner spell name
Param: str - Summoner spell id
Return: str - Summoner spell name 
'''


def find_summoner_spell(summspellid):
    with open(r'summoner.json') as summonerspell:
        summonerspelldata = json.load(summonerspell)
    for summspells, values in summonerspelldata['data'].items():
        if values['key'] == summspellid:
            return values['name']
    return


'''
Converts a champion id into the summoner name
Param: str - champion id
Return: str - champion name
'''


def find_champion(champid):
    with open(r'champion.json',
              encoding="utf8") as champions:
        champdata = json.load(champions)
    for champ, values in champdata['data'].items():
        if values['key'] == champid:
            return values['name']
    return


'''
Get's primary and secondary runes
Param: 2 str - summoner  perkstyle and perk substyle id's
Return: Tuple - of both primary and secondary summoner spells 
'''


def find_runes(perkid1, perksubstyleid):
    with open(r'runesReforged.json',
              encoding="utf8") as runes:
        runesdata = json.load(runes)
    mainrune = ''
    secondaryrune = ''
    for rune in runesdata:
        if str(rune['id']) == perksubstyleid:
            secondaryrune = rune['key']
        for runesmaller in rune['slots'][0]['runes']:
            if str(runesmaller['id']) == perkid1:
                mainrune = runesmaller['key']
        if mainrune != '' and secondaryrune != '':
            break
    return mainrune, secondaryrune


'''
For a specified champion, summoners spell, or rune it finds the correct emoji 
Input: str - the name of the champion, summ spell, rune, or rank
Output: str - The correctly formatted emoji for discord
'''


def find_emojis(name):
    if name == "":
        return "Unranked"
    if name == "Rek'Sai":
        name = "RekSai"
    if name == "Cho'gath":
        name = "ChoGath"
    if name == "Kai'Sa":
        name = "KaiSa"
    if name == "Kha'Zix":
        name = "KhaZix"
    if name == "Kog'Maw":
        name = 'KogMaw'
    if name == "Vel'Koz":
        name = "VelKoz"
    if name == "Dr. Mundo":
        name = "DrMundo"
    if name == 'Nunu & Willump':
        name = 'Nunu'
    if name == 'Mastery3' or name == 'Mastery1' or name == 'Mastery2':
        name = 'Mastery1'
    for emoji in Emojis:
        if name.replace(' ', '') in emoji:
            return emoji
    return ''


if __name__ == '__main__':
    print(live_match('LucieNova', 'na1'))
