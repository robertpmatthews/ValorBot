from riotwatcher import LolWatcher
import Credentials
import requests
import time
import calendar
import operator
lol_watcher = LolWatcher(Credentials.LOLAPIKey)


'''
This function returns a dictionary of upcoming clash tournament dates for the given region.
@param string: region
@return dictionary: clash info with keys as the upcoming tournament names

'''


def getclashdate(region, tz):
    url = "https://" + region + ".api.riotgames.com/lol/clash/v1/tournaments?api_key=" + Credentials.LOLAPIKey
    response = requests.get(url)
    clash_info = response.json()
    info = {}
    for key in clash_info:
        if not key['schedule'][0]["cancelled"]:
            tournament = key['nameKey'] + " " + key['nameKeySecondary']
            my_reg = int(str(key['schedule'][0]['registrationTime'])[:-3])
            date_reg = time.gmtime(my_reg)
            my_start = int(str(key['schedule'][0]['startTime'])[:-3])
            date_start = time.gmtime(my_start)
            reg = calendar.month_name[date_reg[1]] + " " +\
                hour_convertor(date_reg[2], date_reg[3]+time_zone_offset(tz), date_reg[4])
            start = calendar.month_name[date_start[1]] + " " + \
                hour_convertor(date_reg[2], date_start[3] + time_zone_offset(tz), date_start[4])

            tourney = tournament.capitalize().replace("_", " ")
            info[tourney] = [reg, start, my_reg]
        else:
            tournament = key['nameKey'] + " " + key['nameKeySecondary']
            tourney = tournament.capitalize().replace("_", " ")
            info[tourney] = ["Cancelled", "Cancelled", 0]
    return info


'''
This function returns the UTC offset for a given timezone.
@param string: timezone
@return int: UTC offset
'''


def time_zone_offset(tz):
    if tz == "gmt":
        return 0
    if tz == "bst":
        return 1
    if tz == "cest":
        return 2
    if tz == "eest":
        return 3
    if tz == "edt":
        return -4
    if tz == "cdt":
        return -5
    if tz == "mdt":
        return -6
    if tz == "pdt":
        return -7
    if tz == "msk":
        return 3


'''
Takes in integers of day hours and minutes and converts them to digestible string format.
@param integers: day, hour, minutes
@return str of day, hour:minutes

'''


def hour_convertor(day, hour, minutes):
    if minutes < 10:
        if 0 < hour < 12:
            return str(day) + ", " + str(hour) + ":0" + str(minutes) + " a.m."
        elif hour == 0:
            return str(day) + ", " + "12" + ":0" + str(minutes) + " a.m."
        elif hour < 0:
            return hour_convertor(day, 24+hour, minutes)
        else:
            return str(day) + ", " + str(hour-12) + ":0" + str(minutes) + " p.m."

    else:
        if 0 < hour < 12:
            return str(day) + ", " + str(hour) + ":" + str(minutes) + " a.m."
        elif hour == 0:
            return str(day) + ", " + "12" + ":" + str(minutes) + " a.m."
        elif hour < 0:
            return hour_convertor(day, 24+hour, minutes)
        else:
            return str(day) + ", " + str(hour-12) + ":" + str(minutes) + " p.m."


'''
This function sorts keys of clash info dictionary so that I can iterate over them in the right order.
@param dictionary of clash info
@return ordered keys which are the names of upcoming clash tournaments (List)
'''


def sort(dic):
    order = {}
    keys = []
    for key, values in dic.items():
        order[key] = values[2]
    sorted_dict = sorted(order.items(), key=operator.itemgetter(1), reverse=False)
    for i in sorted_dict:
        keys.append(i[0])
    return keys


if __name__ == '__main__':
    sort(getclashdate('na1', "edt"))
