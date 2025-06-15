import pymongo
from pymongo import MongoClient, errors
import Credentials
import Main_Functions
import time


clust = MongoClient('mongodb+srv://SlobbyCo:' + Credentials.MongoDBPass +
                    '@cluster0-h5xc5.mongodb.net/test?retryWrites=true&w=majority')
db = clust['DiscBot']
collection = db['Active Servers']
collection1 = db['Twitter Url\'s']
collection2 = db['Current Patch']
collection5 = db['Leaderboards']
collection6 = db['LiveMatch']
collection7 = db['TFT Leaderboards']
collection8 = db['TFT Stats']
test = db['Test']
post = {"_id": 0, "tweetdict": {"Valorant": 0, "League of Legends": 0, "Teamfight Tactics": 0,
        "Legends of Runeterra": 0, "Riot Games": 0}, "patchdict": {"Valorant": 0,
        "League of Legends": 0, "Teamfight Tactics": 0, "Legends of Runeterra": 0},
        "region": "na1", "name": "", "members": 0}
twit_url = {"_id": "", "screen_name": ""}
group_post = {"_id": "", "group": "", "server": "", "region": "", "members": {}}
tft_stats = {"_id": 0, "lb_count": 0}
'''
Inserts a server into the database with the server id if it has not been found in the database
Param: str - A string of the discord server id
Returns: None
'''


def insert_post(id, name, members):
    if not collection.find_one(id):
        post["_id"] = id
        post["name"] = name
        post["members"] = members
        post["tz"] = "edt"
        collection.insert_one(post)


'''
Inserts a url into the Twitter URL directory in MongoDB
Param: 2 str, url - a string of the url that was tweeted, screen_name - the screen name of the account that tweeted out
this tweet
Returns: None
'''


def insert_url(url, screen_name):
    twit_url["_id"] = url
    twit_url["screen_name"] = screen_name
    collection1.insert_one(twit_url)


'''
Inserts a new patch into the dictionary and also returns a string based on what game was updated, this compares to the
current link in the db and if it has changed then it will update and inform the code that it has been updated via the
return string output.
Param: 2 str, url - a string of the url for the obtained patch notes, game - The game that the patch note url is for
Return str - A string that informs us of whether or not there was a new patch for a respective game, returns 'Game has
not been updated' if there was no updated url.
'''


def insert_new_patch(url, game):
    patch_dict = collection2.find_one({'_id': 0})['patchdict']
    if patch_dict['League of Legends'] != url and game == 'League of Legends':
        patch_dict['League of Legends'] = url
        collection2.update_one({'_id': 0}, {"$set": {'patchdict': patch_dict}})
        return True
    elif patch_dict['Teamfight Tactics'] != url and game == 'Teamfight Tactics':
        patch_dict['Teamfight Tactics'] = url
        collection2.update_one({'_id': 0}, {"$set": {'patchdict': patch_dict}})
        return True
    elif patch_dict['Valorant'] != url and game == 'Valorant':
        patch_dict['Valorant'] = url
        collection2.update_one({'_id': 0}, {"$set": {'patchdict': patch_dict}})
        return True
    else:
        return False


'''
Inserts the new group that was created into the collection5 that is hosted on MongoDB. This allows us to store all of
the group data for a specified guild
@param server - the server object it belongs to, the creator the id and name of the discord user, and the group name so 
that the player can reference this group at a later date.
@return either "True" if the id is not in the database already then it will return true, if it is then it returns false,
if the group name already exists then it returns "Group name already exists"
'''


def insert_group(server, creator, group, region):
    if not collection5.find_one({"_id": str(creator.id)+str(server), "server": server}):
        try:
            if not collection5.find_one({"group": group, "server": server}):
                group_post["_id"] = str(creator.id)+str(server)
                group_post["group"] = group
                group_post["server"] = server
                group_post["message"] = 0
                group_post["channel"] = 0
                group_post["region"] = region
                collection5.insert_one(group_post)
                return "True"
        except pymongo.errors.DuplicateKeyError:
            return "Group name already exists"
    return "False"


'''
Insert Group for TFT
Inserts the new group that was created into the collection5 that is hosted on MongoDB. This allows us to store all of
the group data for a specified guild
@param server - the server object it belongs to, the creator the id and name of the discord user, and the group name so 
that the player can reference this group at a later date.
@return either "True" if the id is not in the database already then it will return true, if it is then it returns false,
if the group name already exists then it returns "Group name already exists"
'''


def insert_group_tft(server, creator, group, region):
    if not collection7.find_one({"_id": str(creator.id)+str(server), "server": server}):
        try:
            if not collection7.find_one({"group": group, "server": server}):
                group_post["_id"] = str(creator.id)+str(server)
                group_post["group"] = group
                group_post["server"] = server
                group_post["message"] = 0
                group_post["channel"] = 0
                group_post["region"] = region
                collection7.insert_one(group_post)
                return "True"
        except pymongo.errors.DuplicateKeyError:
            return "Group name already exists"
    return "False"


'''
Deletes the group from collection5 on MongoDB, this can be called hen the user wants to delete the group entirely, and 
it is also called when said player leaves the server
@param: server - the server object of the user that called this command, and creator - the owner of the group that this
group will be deleted from
@:return: true if there if that creator has created a group in the respective server, false otherwise
'''


def delete_group(server, creator):
    if collection5.find_one({"_id": str(creator.id)+str(server), "server": server}):
        collection5.delete_one({"_id": str(creator.id)+str(server), "server": server})
        return True
    else:
        return False


'''
delete group TFT
Deletes the group from collection7 on MongoDB, this can be called hen the user wants to delete the group entirely, and 
it is also called when said player leaves the server
@param: server - the server object of the user that called this command, and creator - the owner of the group that this
group will be deleted from
@:return: true if there if that creator has created a group in the respective server, false otherwise
'''


def delete_group_tft(server, creator):
    if collection7.find_one({"_id": str(creator.id)+str(server), "server": server}):
        collection7.delete_one({"_id": str(creator.id)+str(server), "server": server})
        return True
    else:
        return False


'''
Adds a player to the creators group based on the summoner name and the server that they are in
@param: server - the server object of the user that called this command, creator - the owner of the group that this
summoner will be added to, and summoner - the summoner name of the player that is being added to the group
@:return "Added" if the player meets all the criteria to be added, 'Already here' if the player is already in the group,
'Too many members' if the group has hit the fifteen player limit, and "Group not found" if the discord user calling the
command is not the creator of any groups on the respective server
'''


def add_player(server, creator, summoner):
    lower = []
    if collection5.find_one({"_id": str(creator.id)+str(server), "server": server}):
        my_group = collection5.find_one({"_id": str(creator.id)+str(server), "server": server})
        if len(my_group["members"]) < 15:
            for members in my_group["members"]:
                lower.append(members.lower())
            if summoner.lower() not in lower:
                region = my_group["region"]
                summonerid = Main_Functions.get_summoner_id(summoner, region)
                temp = Main_Functions.get_tier_faster(summonerid, region)
                my_group["members"][summoner] = [temp[0], temp[1], summonerid]
                collection5.update({"_id": str(creator.id)+str(server), "server": server},
                                   {"$set": {"members": my_group["members"]}})
                return "Added"
            return "Already here"
        return "Too many members"
    return "Group not found"


'''
Add player TFT
Adds a player to the creators group based on the summoner name and the server that they are in
@param: server - the server object of the user that called this command, creator - the owner of the group that this
summoner will be added to, and summoner - the summoner name of the player that is being added to the group
@:return "Added" if the player meets all the criteria to be added, 'Already here' if the player is already in the group,
'Too many members' if the group has hit the fifteen player limit, and "Group not found" if the discord user calling the
command is not the creator of any groups on the respective server
'''


def add_player_tft(server, creator, summoner):
    lower = []
    if collection7.find_one({"_id": str(creator.id) + str(server), "server": server}):
        my_group = collection7.find_one({"_id": str(creator.id) + str(server), "server": server})
        if len(my_group["members"]) < 15:
            for members in my_group["members"]:
                lower.append(members.lower())
            if summoner.lower() not in lower:
                region = my_group["region"]
                summonerid = Main_Functions.get_summoner_id_tft(summoner, region)
                temp = Main_Functions.get_tier_faster_tft(summonerid, region)
                my_group["members"][summoner] = [temp[0], temp[1], summonerid]
                collection7.update({"_id": str(creator.id) + str(server), "server": server},
                                   {"$set": {"members": my_group["members"]}})
                return "Added"
            return "Already here"
        return "Too many members"
    return "Group not found"


'''
deletes a player to the creators group based on the summoner name and the server that they are in
@param: server - the server object of the user that called this command, creator - the owner of the group that this
summoner will be added to, and summoner - the summoner name of the player that is being added to the group
@:return "Deleted" if the player meets all the criteria to be deleted, 'Summoner not found' if the name that was input 
was not in the group that the creator is in, and 'Group not found' if the discord user calling the
command is not the creator of any groups on the respective guild
'''


def delete_player(server, creator, summoner):
    if collection5.find_one({"_id": str(creator.id)+str(server), "server": server}):
        my_group = collection5.find_one({"_id": str(creator.id)+str(server), "server": server})
        if summoner in my_group["members"]:
            del my_group["members"][summoner]
            collection5.update({"_id": str(creator.id)+str(server), "server": server},
                               {"$set": {"members": my_group["members"]}})
            return "Deleted"
        return "Summoner not found"
    return "Group not found"


'''
Delete player tft
deletes a player to the creators group based on the summoner name and the server that they are in
@param: server - the server object of the user that called this command, creator - the owner of the group that this
summoner will be added to, and summoner - the summoner name of the player that is being added to the group
@:return "Deleted" if the player meets all the criteria to be deleted, 'Summoner not found' if the name that was input 
was not in the group that the creator is in, and 'Group not found' if the discord user calling the
command is not the creator of any groups on the respective guild
'''


def delete_player_tft(server, creator, summoner):
    if collection7.find_one({"_id": str(creator.id)+str(server), "server": server}):
        my_group = collection7.find_one({"_id": str(creator.id)+str(server), "server": server})
        if summoner in my_group["members"]:
            del my_group["members"][summoner]
            collection7.update({"_id": str(creator.id)+str(server), "server": server},
                               {"$set": {"members": my_group["members"]}})
            return "Deleted"
        return "Summoner not found"
    return "Group not found"


'''
This function renames the group
@param: server - the server object of the user that called this command, creator - the owner of the group that this
summoner will be added to, and summoner - the summoner name of the player that is being added to the group
@:return "Group renamed" if the group meets all the criteria to be renamed, 'No group found' if the discord user that is
calling the command is not the creator of a group, and 'Name already in use' if the the user tries to input a name that
is already the name of a different group on the same guild.
'''


def rename_group(server, creator, group):
    if not collection5.find_one({"server": server, "group": group}):
        if collection5.find_one({"_id": str(creator.id)+str(server), "server": server}):
            collection5.update({"_id": str(creator.id)+str(server), "server": server}, {"$set": {"group": group}})
            return "Group renamed"
        return "No group found"
    return "Name already in use"


'''
rename group TFT
This function renames the group
@param: server - the server object of the user that called this command, creator - the owner of the group that this
summoner will be added to, and summoner - the summoner name of the player that is being added to the group
@:return "Group renamed" if the group meets all the criteria to be renamed, 'No group found' if the discord user that is
calling the command is not the creator of a group, and 'Name already in use' if the the user tries to input a name that
is already the name of a different group on the same guild.
'''


def rename_group_tft(server, creator, group):
    if not collection7.find_one({"server": server, "group": group}):
        if collection7.find_one({"_id": str(creator.id)+str(server), "server": server}):
            collection7.update({"_id": str(creator.id)+str(server), "server": server}, {"$set": {"group": group}})
            return "Group renamed"
        return "No group found"
    return "Name already in use"


'''
This function updates all the ranks of the players in their group
@param: server - the server object of the user that called this command, and group - the group that the ranks are being
updated for
@return: None
'''


def update_rank(server, group):
    my_group = collection5.find_one({"server": server, "group": group})
    region = my_group["region"]
    for summoner, values in my_group["members"].items():
        temp = Main_Functions.get_tier_faster(values[2], region)
        my_group["members"][summoner] = [temp[0], temp[1], values[2]]
    collection5.update({"server": server, "group": group},
                       {"$set": {"members": my_group["members"]}})


'''
update rank TFT
This function updates all the ranks of the players in their group
@param: server - the server object of the user that called this command, and group - the group that the ranks are being
updated for
@return: None
'''


def update_rank_tft(server, group):
    my_group = collection7.find_one({"server": server, "group": group})
    region = my_group["region"]
    for summoner, values in my_group["members"].items():
        temp = Main_Functions.get_tier_faster_tft(values[2], region)
        my_group["members"][summoner] = [temp[0], temp[1], values[2]]
    collection7.update({"server": server, "group": group},
                       {"$set": {"members": my_group["members"]}})


'''
Insert leaderboard message
'''


def insert_leaderboard_message(embed_id, creator, server):
    collection5.update({"_id": str(creator.id)+str(server), "server": server}, {"$set": {"message": embed_id}})
    time.sleep(120)
    collection5.update({"_id": str(creator.id) + str(server), "server": server}, {"$set": {"message": 0}})


'''
Insert tft leaderboard msg
'''


def insert_leaderboard_message_tft(embed_id, creator, server):
    collection7.update({"_id": str(creator.id) + str(server), "server": server}, {"$set": {"message": embed_id}})
    time.sleep(120)
    collection7.update({"_id": str(creator.id) + str(server), "server": server}, {"$set": {"message": 0}})


'''
LB startup
'''


def leaderboard_startup():
    leaderboards = collection5.find({})
    for leaderboard in leaderboards:
        collection5.update({"_id": leaderboard['_id']}, {'$set': {'message': 0}})
        collection5.update({"_id": leaderboard['_id']}, {'$set': {'channel': 0}})


'''
Lb startup TFT
'''


def leaderboard_startup_tft():
    leaderboards = collection7.find({})
    for leaderboard in leaderboards:
        collection7.update({"_id": leaderboard['_id']}, {'$set': {'message': 0}})
        collection7.update({"_id": leaderboard['_id']}, {'$set': {'channel': 0}})


def update_tft(calls):
    collection8.update_one({"_id": 0}, {'$inc': {"lb_count": calls}})


if __name__ == '__main__':
    print('why are u running mongo as the main script chat')
    '''
    insert_new_patch(PatchNotes.currentpatchpic('League of Legends'), 'League of Legends')
    insert_new_patch(PatchNotes.currentpatchpic('Teamfight Tactics'), 'Teamfight Tactics')
    
    mine = collection.find({})
    for collect in mine:
        try:
            print(collect["tz"])
        except:
            collection.update_one({"_id":collect["_id"]}, {'$set': {'tz': "edt"}})
    '''