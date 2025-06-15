import urllib.request
import re
import requests

'''
This function when ran gives the most recent patch notes for League of Legends
Param: None
Returns: Str - The URL for the current patch for League of Legends
'''


def findpatcheslol():
    patches = requests.get('https://lolstatic-a.akamaihd.net/frontpage/apps/prod/harbinger-l10-website/'
                           'en-us/production/en-us/page-data/news/game-updates/page-data.json').json()
    for patch in patches['result']['pageContext']['data']['sections'][0]['props']['articles']:
        link = patch['link']['url']
        pattern = re.compile(r'/[a-z]+/[a-z-]+/patch[a-z0-9-]+?/')
        match = pattern.search(link)
        try:
            return 'https://na.leagueoflegends.com/en-us/' + match.string
        except AttributeError:
            pass


'''
This function will give the most recent patch notes for Teamfight Tactics
Param: None
Returns: Str - The URL for the current patch for Teamfight Tactics
'''


def findpatchestft():
    patches = requests.get(
        'https://lolstatic-a.akamaihd.net/frontpage/apps/prod/harbinger-l10-website/en-us/production/'
        'en-us/page-data/news/game-updates/page-data.json').json()
    for patch in patches['result']['pageContext']['data']['sections'][0]['props']['articles']:
        link = patch['link']['url']
        pattern = re.compile(r'/[a-z]+/[a-z-]+/teamfight-tactics-patch[a-z0-9-]+?/')
        match = pattern.search(link)
        try:
            return 'https://na.leagueoflegends.com/en-us/' + match.string
        except AttributeError:
            pass


''' 
This function when ran gives a list of the 6 most recent patch notes for League of Legends
Param: None
Returns: Str - The URL for the current patch for Teamfight Tactics
'''


def findpatchesval():
    patches = requests.get('https://playvalorant.com/page-data/en-us/news/page-data.json').json()
    for patch in patches['result']['data']['allContentstackArticles']['nodes']:
        link = patch['url']['url']
        pattern = re.compile(r'/[a-z]+/[a-z-]+/valorant-patch[a-z0-9-]+?/')
        match = pattern.search(link)
        try:
            return 'https://playvalorant.com/en-us/' + match.string
        except AttributeError:
            pass


'''
This scrapes for the link to get the patch overview image for league on a specific patch on the riot website
Param: Str - The patch url as a string
Returns: Str - The image url as a string
'''


def lolimage(patchurl):
    current = patchurl
    file = urllib.request.urlopen(current)
    stream = file.read().decode('utf-8')
    patterntitle = re.compile(r'Patch Highlights</h2>')
    titles = patterntitle.finditer(stream)
    startindex = 1000000000000
    for title in titles:
        currentindex = title.end()
        if currentindex < startindex:
            startindex = currentindex
    newstream = stream[startindex:]
    patternlink = re.compile(r'<img src=".+"')
    link = patternlink.search(newstream).group(0)
    return link[10:-1]


'''
This scrapes for the link to get the patch overview image for tft on a specific patch on the riot website.
Param: Str - The tft patch url as a string
Returns: Str - The image url as a string
'''


def tftimage(patchurl):
    current = patchurl
    file = urllib.request.urlopen(current)
    stream = file.read().decode('utf-8')
    patterntitle = re.compile(r'Highlights</h2>')
    titles = patterntitle.finditer(stream)
    startindex = 1000000000000
    for title in titles:
        currentindex = title.end()
        if currentindex < startindex:
            startindex = currentindex
    newstream = stream[startindex:]
    patternlink = re.compile(r'<img src=".+"')
    link = patternlink.search(newstream).group(0)
    return link[10:-1]


'''
This scrapes for the link to get the banner image for Valorant on a specific patch on the riot website.
Param: Str - The val patch url as a string
Returns: Str - The image url as a string
'''


def valimage(patchurl):
    current = patchurl
    file = urllib.request.urlopen(current)
    stream = file.read().decode('utf-8')
    patterntitle = re.compile(r'twitter:image')
    titles = patterntitle.finditer(stream)
    startindex = 1000000000000
    for title in titles:
        currentindex = title.end()
        if currentindex < startindex:
            startindex = currentindex
    newstream = stream[startindex:]
    patternlink = re.compile(r'content=".+?"')
    link = patternlink.search(newstream).group(0)
    return link[9:-1]


'''
This scrapes for the link to get the banner image for Valorant on a specific patch on the riot website.
Param: Str - The val patch url as a string
Returns: Str - The image url as a string
'''


def tftimagemetadata(patchurl):
    current = patchurl
    file = urllib.request.urlopen(current)
    stream = file.read().decode('utf-8')
    patterntitle = re.compile(r'twitter:image')
    titles = patterntitle.finditer(stream)
    startindex = 1000000000000
    for title in titles:
        currentindex = title.end()
        if currentindex < startindex:
            startindex = currentindex
    newstream = stream[startindex:]
    patternlink = re.compile(r'content=".+?"')
    link = patternlink.search(newstream).group(0)
    return link[9:-1]


'''
This scrapes for the link to get the banner image for Valorant on a specific patch on the riot website.
Param: Str - The val patch url as a string
Returns: Str - The image url as a string
'''


def lolimagemetadata(patchurl):
    current = patchurl
    file = urllib.request.urlopen(current)
    stream = file.read().decode('utf-8')
    patterntitle = re.compile(r'twitter:image')
    titles = patterntitle.finditer(stream)
    startindex = 1000000000000
    for title in titles:
        currentindex = title.end()
        if currentindex < startindex:
            startindex = currentindex
    newstream = stream[startindex:]
    patternlink = re.compile(r'content=".+?"')
    link = patternlink.search(newstream).group(0)
    return link[9:-1]


'''
This returns the current patch for the given game by the user
Param: Str - The game name that the player wants to receive the desired patch link for
Returns: Str - The current patch link for the inputted game
'''


def currentpatch(game):
    if game == 'TFT' or game == 'Teamfight Tactics' or game == 'Team fight Tactics' or game == 'tft' or \
            game == 'team fight tactics':
        return findpatchestft()
    elif game == 'Valorant' or game == 'val' or game == 'valorant':
        return findpatchesval()
    elif game == 'LoL' or game == 'League' or game == 'League of Legends' or game == 'lol':
        return findpatcheslol()
    else:
        return "This is not a valid game or you input the name in an unaccepted format"


'''
This returns the current image for the given patch
Param: Str - the game that the player wants to receive the desired patch link for
Returns: Str - The current patch image for the inputted game
'''


def currentpatchpic(game):
    if game == 'TFT' or game == 'Teamfight Tactics' or game == 'Team fight Tactics' or game == 'tft' or \
            game == 'team fight tactics':
        return tftimage(findpatchestft())
    elif game == 'Valorant' or game == 'val' or game == 'valorant':
        return valimage(findpatchesval())
    elif game == 'LoL' or game == 'League' or game == 'League of Legends' or game == 'lol':
        return lolimage(findpatcheslol())
    else:
        return "This is not a valid game or you input the name in an unaccepted format"


'''
This returns the current image for the given patch
Param: Str - the game that the player wants to receive the desired patch link for
Returns: Str - The current patch image for the inputted game
'''


def currentpatchpicmetadata(game):
    if game == 'TFT' or game == 'Teamfight Tactics' or game == 'Team fight Tactics' or game == 'tft' or \
            game == 'team fight tactics':
        return tftimagemetadata(findpatchestft())
    elif game == 'Valorant' or game == 'val' or game == 'valorant':
        return valimage(findpatchesval())
    elif game == 'LoL' or game == 'League' or game == 'League of Legends' or game == 'lol':
        return lolimagemetadata(findpatcheslol())
    else:
        return "This is not a valid game or you input the name in an unaccepted format"


'''
This function returns the metadata for league of legends to help format the discord message
Param: str - input the link of the game to find the metadata
Returns: dict - a dictionary of title, description, and author thumbnail
'''


def metadata(url):
    current = url
    file = urllib.request.urlopen(current)
    stream = file.read().decode('utf-8')
    patterntitle = re.compile(r'"og:title" content=".+?"')
    patterndescription = re.compile(r'og:description" content=".+?"')
    patternthumbnail = re.compile(r'og:image" content=".+?"')
    matchtitle = patterntitle.search(stream).group(0)[20:-1]
    matchdescription = patterndescription.search(stream).group(0)[25:-1]
    matchthumbnail = patternthumbnail.search(stream).group(0)[19:-1]
    return {'title': matchtitle, 'description': matchdescription, 'thumbnail': matchthumbnail}


if __name__ == '__main__':
    '''
    print(currentpatchpicmetadata('lol'))
    print(currentpatchpicmetadata('tft'))
    print(currentpatchpicmetadata('val'))
    '''
    print(findpatcheslol())
