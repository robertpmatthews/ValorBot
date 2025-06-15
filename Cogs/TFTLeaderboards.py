from discord.ext import commands
import MongoDB
import Main_Functions
import requests
import discord
import LiveGame
from asyncio import sleep


class TFTLeaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="makegrouptft",
                      description='Makes a group where you and your '
                                  'friends can track ranks and compete against each other!'
                                  'Use ?makegrouptft[groupname] (brackets not included).',
                      brief="Makes a TFT group with the given name!",
                      case_insensitive=True)
    async def make_group_tft(self, ctx, *args):
        group = ''
        for i in range(len(args)):
            group = group + ' ' + args[i]
        group = group[1:]
        if len(group) > 20:
            text = "Sorry {} that group name is too long!".format(ctx.message.author.mention)
            await ctx.send(text)
            return
        my_collection = MongoDB.collection.find_one(ctx.guild.id)
        region = my_collection["region"]
        if MongoDB.insert_group_tft(ctx.guild.id, ctx.author, group, region) == "True":
            text = "Hey {} your TFT group: " + group + " has been created! " \
                                                       "Use ?addplayertft [summoner name] " \
                                                       "to add up to 15 players to your group!"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        elif MongoDB.insert_group_tft(ctx.guild.id, ctx.author, group, region) == "False":
            text = "Sorry {} looks like you already made a TFT group on this server. " \
                   "If you want, you can use ?renamegrouptft [group name] " \
                   "to rename your group.".format(ctx.message.author.mention)
            await ctx.send(text)
        elif MongoDB.insert_group_tft(ctx.guild.id, ctx.author, group, region) == "Group name already exists":
            text = "Sorry {} that TFT group name is already taken on this server!".format(ctx.message.author.mention)
            await ctx.send(text)

    @commands.command(name="deletegrouptft",
                      description='Deletes a TFT group that you made.'
                                  'Use ?deletegrouptft .',
                      brief="Deletes a TFT group that you own.",
                      case_insensitive=True)
    async def delete_group_tft(self, ctx):
        if MongoDB.delete_group_tft(ctx.guild.id, ctx.author):
            text = "Your TFT group has been deleted {}".format(ctx.message.author.mention)
            await ctx.send(text)
        else:
            text = "{} Could not delete your TFT group.  Do you own a TFT group?"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(name="addplayertft",
                      description='Adds a player to a group that you made!'
                                  'Use ?addplayertft[summonername] (brackets not included).',
                      brief="Adds a player to a TFT group.",
                      case_insensitive=True)
    async def add_player_tft(self, ctx, *args):
        summoner = ''
        for i in range(len(args)):
            summoner = summoner + ' ' + args[i]
        summoner = summoner[1:]
        if MongoDB.collection7.find_one({"_id": str(ctx.author.id)+str(ctx.guild.id), "server": ctx.guild.id}):
            collection = MongoDB.collection7.find_one(str(ctx.author.id) + str(ctx.guild.id))
            region = collection["region"]
            try:
                collection = MongoDB.collection.find_one(ctx.guild.id)
                region = collection["region"]
                Main_Functions.tft_watcher.summoner.by_name(region, summoner)
                MongoDB.update_tft(1)
                if MongoDB.add_player_tft(ctx.guild.id, ctx.author, summoner) == "Added":
                    text = summoner + " has been added to your TFT group! {}"
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
                elif MongoDB.add_player_tft(ctx.guild.id, ctx.author, summoner) == "Already here":
                    text = "Hm {}, looks like you already added " + summoner + "."
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
                elif MongoDB.add_player_tft(ctx.guild.id, ctx.author, summoner) == "Too many members":
                    text = "Sorry {}, you have reached the max number " \
                           "of players in a TFT group. " + summoner + " could not be added :frowning:"
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
                elif MongoDB.add_player_tft(ctx.guild.id, ctx.author, summoner) == "Group not found":
                    text = "Sorry {}, it doesn't appear that you have a group. " \
                           "You can make one with ?makegrouptft [groupname]."
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
            except requests.exceptions.HTTPError:
                text = "Sorry {}, Summoner: " + summoner + " is not a registered summoner name in " + \
                       Main_Functions.region_converter(region) + "!"
                text2 = text.format(ctx.message.author.mention)
                await ctx.send(text2)
        else:
            text = "Sorry {}, it doesn't appear that you have a group. You can make one with ?makegrouptft [groupname]."
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(name="removeplayertft",
                      description='Removes a player from a TFT group that you made!'
                                  'Use ?removeplayertft[summonername] (brackets not included).',
                      brief="Removes player from TFT group.",
                      case_insensitive=True)
    async def remove_player_tft(self, ctx, *args):
        summoner = ''
        for i in range(len(args)):
            summoner = summoner + ' ' + args[i]
        summoner = summoner[1:]
        if MongoDB.collection7.find_one({"_id": str(ctx.author.id)+str(ctx.guild.id), "server": ctx.guild.id}):
            collection = MongoDB.collection7.find_one(str(ctx.author.id) + str(ctx.guild.id))
            region = collection["region"]
            try:
                collection = MongoDB.collection.find_one(ctx.guild.id)
                region = collection["region"]
                Main_Functions.tft_watcher.summoner.by_name(region, summoner)
                MongoDB.update_tft(1)
                if MongoDB.delete_player_tft(ctx.guild.id, ctx.author, summoner) == "Deleted":
                    text = summoner + " has been removed from your TFT group. {}"
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
                elif MongoDB.delete_player_tft(ctx.guild.id, ctx.author, summoner) == "Summoner not found":
                    text = summoner + " was not found in your TFT group. {}"
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
                elif MongoDB.delete_player_tft(ctx.guild.id, ctx.author, summoner) == "Group not found":
                    text = "Sorry {}, it doesn't appear that " \
                           "you have a TFT group. You can make one with ?makegrouptft [groupname]."
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
            except requests.exceptions.HTTPError:
                text = "Sorry {}, Summoner: " + summoner + " is not a registered summoner name in " + \
                       Main_Functions.region_converter(region) + "!"
                text2 = text.format(ctx.message.author.mention)
                await ctx.send(text2)
        else:
            text = "Sorry {}, it doesn't appear that you have a group. You can make one with ?makegrouptft [groupname]."
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(name="renamegrouptft",
                      description='Renames a group that you made!'
                                  'Use ?renamegrouptft [new group name] brackets not included.',
                      brief="Renames your TFT group.",
                      case_insensitive=True)
    async def rename_group_tft(self, ctx, *args):
        group = ''
        for i in range(len(args)):
            group = group + ' ' + args[i]
        group = group[1:]
        if MongoDB.rename_group_tft(ctx.guild.id, ctx.author, group) == "Group renamed":
            text = "Hey {} your TFT group has been renamed to " + group + "! " \
                                                                          "Use ?addplayertft [summoner name] " \
                                                                          "to add up to 15 players to your group!"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        elif MongoDB.rename_group_tft(ctx.guild.id, ctx.author, group) == "No group found":
            text = "Hey {} we couldn't find a TFT group for you to rename. " \
                   "Use ?makegrouptft [group name] to make your own group!"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        elif MongoDB.rename_group_tft(ctx.guild.id, ctx.author, group) == "Name already in use":
            text = "Sorry {}, that name is already used on this server. Try a different name."
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(aliases=["leaderboardtft", "lbtft"],
                      description='Displays TFT leaderboard of the group you choose, where you can compare yourself '
                                  'to your friends and see ranked stats. '
                                  'Use ?leaderboardtft [group name] or ?lbtft (brackets not included)',
                      brief="Displays TFT leaderboard.",
                      case_insensitive=True)
    async def display_leaderboard_tft(self, ctx, *args):
        group = ''
        for i in range(len(args)):
            group = group + ' ' + args[i]
        group = group[1:]
        mongo_data = MongoDB.collection7.find_one({"server": ctx.guild.id, "group": group})
        if not mongo_data:
            text = "Sorry {} I couldn't find a TFT group with that name!".format(ctx.message.author.mention)
            await ctx.send(text)
        elif mongo_data['message']:
            guild = ctx.guild
            textchannels = guild.text_channels
            for textchannel in textchannels:
                if textchannel.id == mongo_data['channel']:
                    channel = textchannel
            message = await channel.fetch_message(mongo_data['message'])
            await ctx.send(embed=message.embeds[0])
        else:
            my_group = MongoDB.collection7.find_one({"server": ctx.guild.id, "group": group})
            num = len(my_group["members"])
            embed = discord.Embed(title=group + " TFT Leaderboard", color=0x00ff00)
            MongoDB.update_rank_tft(ctx.guild.id, group)
            my_sorted = Main_Functions.ordered_list(Main_Functions.numerical_ranks(my_group["members"]))
            my_str = ''
            rank = ''
            for i in range(1, num+1):
                my_str = my_str + str(i) + ". " + my_sorted[i-1] + "\n"
                if Live_Game.find_emojis(my_group["members"][my_sorted[i-1]][0][:-2]) == "Unranked":
                    rank = rank + Live_Game.find_emojis(my_group["members"][my_sorted[i - 1]][0][:-2]) + str(
                        my_group["members"][my_sorted[i - 1]][0]) + " " + str(
                        my_group["members"][my_sorted[i - 1]][1]) + "\n"
                else:
                    rank = rank + Live_Game.find_emojis(my_group["members"][my_sorted[i-1]][0][:-2]) + "| " + \
                           str(my_group["members"][my_sorted[i-1]][0]) + " " + \
                           str(my_group["members"][my_sorted[i-1]][1])+" LP""\n"
            embed.add_field(name='Summoner name',
                            value=my_str,
                            inline=True)
            embed.add_field(name='**Rank**',
                            value=rank,
                            inline=True)
            embed.set_footer(text="*Leaderboards can only be updated every minute*")
            message = await ctx.send(embed=embed)
            MongoDB.update_tft(num)
            MongoDB.collection7.update({"server": ctx.guild.id, "group": group},
                                       {"$set": {"message": message.id}})
            MongoDB.collection7.update({"server": ctx.guild.id, "group": group},
                                       {"$set": {"channel": message.channel.id}})
            await sleep(60)
            MongoDB.collection7.update({"server": ctx.guild.id, "group": group},
                                       {"$set": {"message": 0}})
            MongoDB.collection7.update({"server": ctx.guild.id, "group": group},
                                       {"$set": {"channel": 0}})

    @commands.command(name="mygrouptft",
                      description='Gives your group name if you have one. '
                                  'Use ?mygrouptft ',
                      brief="Displays your group name.")
    async def group_name_tft(self, ctx):
        if MongoDB.collection7.find_one({"_id": str(ctx.author.id)+str(ctx.guild.id)}):
            my_group = MongoDB.collection7.find_one({"_id": str(ctx.author.id)+str(ctx.guild.id)})
            groups = my_group["group"]
            text = "Hey {}, your TFT group name is: " + groups + ". Use ?leaderboardtft [group] " \
                                                                 "to display updated leaderboard information! "
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        else:
            text = "Sorry {}, it doesn't appear that you have a group. You can make one with ?makegrouptft [groupname]."
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(name="makegroupregiontft",
                      description='Makes a group where you and your friends '
                                  'can track ranks and compete against each other!'
                                  'Use ?makegroup [region][groupname] (brackets not included).',
                      brief="Makes a group with the given name!",
                      case_insensitive=True)
    async def makegroupregiontft(self, ctx, region, *args):
        group = ''
        if Main_Functions.region_converter_backwards(
                region) == "Invalid region. Use ?helpsetup for a list of valid regions!":
            await ctx.send(Main_Functions.region_converter_backwards(region))
            return
        for i in range(len(args)):
            group = group + ' ' + args[i]
        group = group[1:]
        if len(group) > 20:
            text = "Sorry {} that group name is too long!".format(ctx.message.author.mention)
            await ctx.send(text)
            return
        region = Main_Functions.region_converter_backwards(
                region)
        if MongoDB.insert_group_tft(ctx.guild.id, ctx.author, group, region) == "True":
            text = "Hey {} your TFT group: " + group + " has been created! " \
                                                       "Use ?addplayer [summoner name] " \
                                                       "to add up to 15 players to your group!"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        elif MongoDB.insert_group_tft(ctx.guild.id, ctx.author, group, region) == "False":
            text = "Sorry {} looks like you " \
                   "already made a TFT group on this server. If you want, " \
                   "you can use ?renamegroup [group name] to rename your group.".format(
                    ctx.message.author.mention)
            await ctx.send(text)
        elif MongoDB.insert_group_tft(ctx.guild.id, ctx.author, group, region) == "Group name already exists":
            text = "Sorry {} that TFT group name is already taken on this server!".format(ctx.message.author.mention)
            await ctx.send(text)


def setup(bot):
    bot.add_cog(TFTLeaderboards(bot))
