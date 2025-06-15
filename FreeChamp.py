from riotwatcher import LolWatcher
import Credentials
import LiveGame


'''
This creates the format for the embed for the free champ rotation for every champion:
@param: Str - The string of the region in the Riot API format for LoL
@return: champ_str (str) - the format for the embed that displays the free champion rotation for league of legends
'''


def champ_rotation(region):
    champs = []
    champ_str = ""
    lol_watcher = LolWatcher(Credentials.LOLAPIKey)
    free_champs = lol_watcher.champion.rotations(region)
    for champ_id in free_champs['freeChampionIds']:
        champs.append(Live_Game.find_champion(str(champ_id)))
    for champ in champs:
        champ_str = champ_str + Live_Game.find_emojis(champ) + "|" + champ + "\n"
    return champ_str
