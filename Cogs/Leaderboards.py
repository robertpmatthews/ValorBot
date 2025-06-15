from discord.ext import commands
import MongoDB
import Main_Functions
import requests
import discord
import LiveGame
from asyncio import sleep


class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="makegroup",
                      description='Makes a group where you and your friends can track ranks and '
                                  'compete against each other!'
                                  'Use ?makegroup[groupname] (brackets not included).',
                      brief="Makes a group with the given name!",
                      case_insensitive=True)
    async def make_group(self, ctx, *args):
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
        if MongoDB.insert_group(ctx.guild.id, ctx.author, group, region) == "True":
            text = "Hey {} your group: " + group + " has been created! Use ?addplayer [summoner name] " \
                                                   "to add up to 15 players to your group!"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        elif MongoDB.insert_group(ctx.guild.id, ctx.author, group, region) == "False":
            text = "Sorry {} looks like you already made a group on this server. If you want, you can use " \
                   "?renamegroup [group name] to rename your group.".format(ctx.message.author.mention)
            await ctx.send(text)
        elif MongoDB.insert_group(ctx.guild.id, ctx.author, group, region) == "Group name already exists":
            text = "Sorry {} that group name is already taken on this server!".format(ctx.message.author.mention)
            await ctx.send(text)

    @commands.command(name="deletegroup",
                      description='Deletes a group that you made.'
                                  'Use ?deletegroup .',
                      brief="Deletes a group that you own.",
                      case_insensitive=True)
    async def delete_group(self, ctx):
        if MongoDB.delete_group(ctx.guild.id, ctx.author):
            text = "Your group has been deleted {}".format(ctx.message.author.mention)
            await ctx.send(text)
        else:
            text = "{} Could not delete your group.  Do you own a group?"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(name="addplayer",
                      description='Adds a player to a group that you made!'
                                  'Use ?addplayer[summonername] (brackets not included).',
                      brief="Adds a player to a group.",
                      case_insensitive=True)
    async def add_player(self, ctx, *args):
        summoner = ''
        for i in range(len(args)):
            summoner = summoner + ' ' + args[i]
        summoner = summoner[1:]
        if MongoDB.collection5.find_one({"_id": str(ctx.author.id)+str(ctx.guild.id), "server": ctx.guild.id}):
            collection = MongoDB.collection5.find_one(str(ctx.author.id) + str(ctx.guild.id))
            region = collection["region"]
            try:
                collection = MongoDB.collection5.find_one(str(ctx.author.id)+str(ctx.guild.id))
                region = collection["region"]
                Main_Functions.lol_watcher.summoner.by_name(region, summoner)
                if MongoDB.add_player(ctx.guild.id, ctx.author, summoner) == "Added":
                    text = summoner + " has been added to your group! {}"
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
                elif MongoDB.add_player(ctx.guild.id, ctx.author, summoner) == "Already here":
                    text = "Hm {}, looks like you already added " + summoner + "."
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
                elif MongoDB.add_player(ctx.guild.id, ctx.author, summoner) == "Too many members":
                    text = "Sorry {}, you have reached " \
                           "the max number of players in a group. " + summoner + " could not be added :frowning:"
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
            except requests.exceptions.HTTPError:
                text = "Sorry {}, Summoner: " + summoner + " is not a registered summoner name in " + \
                       Main_Functions.region_converter(region) + "!"
                text2 = text.format(ctx.message.author.mention)
                await ctx.send(text2)
        else:
            text = "Sorry {}, it doesn't appear that you have a group. You can make one with ?makegroup [groupname]."
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(name="removeplayer",
                      description='Removes a player from a group that you made!'
                                  'Use ?removeplayer[summonername] (brackets not included).',
                      brief="Removes player from group.",
                      case_insensitive=True)
    async def remove_player(self, ctx, *args):
        summoner = ''
        for i in range(len(args)):
            summoner = summoner + ' ' + args[i]
        summoner = summoner[1:]
        if MongoDB.collection5.find_one({"_id": str(ctx.author.id)+str(ctx.guild.id), "server": ctx.guild.id}):
            collection = MongoDB.collection5.find_one(str(ctx.author.id) + str(ctx.guild.id))
            region = collection["region"]
            try:
                Main_Functions.lol_watcher.summoner.by_name(region, summoner)
                if MongoDB.delete_player(ctx.guild.id, ctx.author, summoner) == "Deleted":
                    text = summoner + " has been removed from your group. {}"
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
                elif MongoDB.delete_player(ctx.guild.id, ctx.author, summoner) == "Summoner not found":
                    text = summoner + " was not found in your group. {}"
                    text2 = text.format(ctx.message.author.mention)
                    await ctx.send(text2)
            except requests.exceptions.HTTPError:
                text = "Sorry {}, Summoner: " + summoner + " is not a registered summoner name in " + \
                       Main_Functions.region_converter(region) + "!"
                text2 = text.format(ctx.message.author.mention)
                await ctx.send(text2)
        else:
            text = "Sorry {}, it doesn't appear that you have a group. You can make one with ?makegroup [groupname]."
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(name="renamegroup",
                      description='Renames a group that you made!'
                                  'Use ?renamegroup [new group name] brackets not included.',
                      brief="Renames your group.",
                      case_insensitive=True)
    async def rename_group(self, ctx, *args):
        group = ''
        for i in range(len(args)):
            group = group + ' ' + args[i]
        group = group[1:]
        if MongoDB.rename_group(ctx.guild.id, ctx.author, group) == "Group renamed":
            text = "Hey {} your group has been renamed to " + group + "! Use ?addplayer [summoner name] to add up to" \
                                                                      " 15 players to your group!"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        elif MongoDB.rename_group(ctx.guild.id, ctx.author, group) == "No group found":
            text = "Hey {} we couldn't find a group for you to rename. Use ?makegroup [group name] " \
                   "to make your own group!"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        elif MongoDB.rename_group(ctx.guild.id, ctx.author, group) == "Name already in use":
            text = "Sorry {}, that name is already used on this server. Try a different name."
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(aliases=["leaderboard", "lb"],
                      description='Displays leaderboard of the group you choose, where you can compare yourself '
                                  'to your friends and see ranked stats. '
                                  'Use ?leaderboard [group name] (brackets not included)',
                      brief="Displays leaderboard.",
                      case_insensitive=True)
    async def display_leaderboard(self, ctx, *args):
        group = ''
        for i in range(len(args)):
            group = group + ' ' + args[i]
        group = group[1:]
        mongo_data = MongoDB.collection5.find_one({"server": ctx.guild.id, "group": group})
        if not mongo_data:
            text = "Sorry {} I couldn't find a group with that name!".format(ctx.message.author.mention)
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
            my_group = MongoDB.collection5.find_one({"server": ctx.guild.id, "group": group})
            num = len(my_group["members"])
            embed = discord.Embed(title=group + " Leaderboard", color=0x00ff00)
            MongoDB.update_rank(ctx.guild.id, group)
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

            MongoDB.collection5.update({"server": ctx.guild.id, "group": group},
                                       {"$set": {"message": message.id}})
            MongoDB.collection5.update({"server": ctx.guild.id, "group": group},
                                       {"$set": {"channel": message.channel.id}})
            await sleep(60)
            MongoDB.collection5.update({"server": ctx.guild.id, "group": group},
                                       {"$set": {"message": 0}})
            MongoDB.collection5.update({"server": ctx.guild.id, "group": group},
                                       {"$set": {"channel": 0}})

    @commands.command(name="mygroup",
                      description='Gives your group name if you have one. '
                                  'Use ?mygroup ',
                      brief="Displays your group name.")
    async def group_name(self, ctx):
        if MongoDB.collection5.find_one({"_id": str(ctx.author.id)+str(ctx.guild.id)}):
            my_group = MongoDB.collection5.find_one({"_id": str(ctx.author.id)+str(ctx.guild.id)})
            groups = my_group["group"]
            text = "Hey {}, your group name is: " + groups + " " \
                                                             "and your groups region is " + \
                   Main_Functions.region_converter(my_group["region"]) + ". " \
                "Use ?leaderboard [group] to display updated leaderboard information! "
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        else:
            text = "Sorry {}, it doesn't appear that you have a group. You can make one with ?makegroup [groupname]."
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @commands.command(name="makegroupregion",
                      description='Makes a group where you and your friends can '
                                  'track ranks and compete against each other!'
                                  'Use ?makegroup [region][groupname] (brackets not included).',
                      brief="Makes a group with the given name!",
                      case_insensitive=True)
    async def makegroupregion(self, ctx, region, *args):
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
        if MongoDB.insert_group(ctx.guild.id, ctx.author, group, region) == "True":
            text = "Hey {} your group: " + group + " has been created! Use ?addplayer " \
                                                   "[summoner name] to add up to 15 players to your group!"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)
        elif MongoDB.insert_group(ctx.guild.id, ctx.author, group, region) == "False":
            text = "Sorry {} looks like you already made a group on this server. " \
                   "If you want, you can use ?renamegroup [group name] to rename your group.".format(
                    ctx.message.author.mention)
            await ctx.send(text)
        elif MongoDB.insert_group(ctx.guild.id, ctx.author, group, region) == "Group name already exists":
            text = "Sorry {} that group name is already taken on this server!".format(ctx.message.author.mention)
            await ctx.send(text)


def setup(bot):
    bot.add_cog(Leaderboards(bot))
