from discord.ext import commands
import LiveGame
import discord
from Main_Functions import get_tier_faster
import MongoDB
from asyncio import sleep
from pymongo.errors import DuplicateKeyError
import Main_Functions
import SummonerThreading


class LiveGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="livegame",
                      description='Displays a live match for league of legends '
                                  'write ?livegame [summoner name]. (Brackets not needed)',
                      brief="Gets live game for lol of a specified summoner",
                      case_insensitive=True)
    async def livegamelol(self, ctx, *args):
        name = ''
        for i in range(len(args)):
            name = name + ' ' + args[i]
        name = name[1:]
        collection = MongoDB.collection.find_one(ctx.guild.id)
        region = collection["region"]
        gamedata = Live_Game.live_match(name, region)
        if gamedata == name + ' not in a live match' or gamedata == 'The summoner ' + name + ' does not exist':
            await ctx.send(gamedata)
            return
        mongo_data = MongoDB.collection6.find_one({'_id': gamedata['gameId']})
        try:
            if mongo_data:
                message = await self.bot.get_guild(mongo_data['guild']).get_channel(mongo_data['channel'])\
                    .fetch_message(mongo_data['message'])
                embed = message.embeds[0]
                embed.description = 'Game Time: ' + gamedata['gametime']
                await ctx.send(embed=embed)
                return
        except AttributeError:
            pass
        embed = discord.Embed(title=gamedata['gamemode'], description='Game Time: ' + gamedata['gametime'])
        rankdict = {}
        for i in range(gamedata['Team 1 count']):
            rankdict['t1p' + str(i+1)] = gamedata['Team 1']['player' + str(i+1)][6]
        for i in range(gamedata['Team 2 count']):
            rankdict['t2p' + str(i+1)] = gamedata['Team 2']['player' + str(i+1)][6]
        new_rank_dict = AbsolutelyPog.multiple_summoners_threading(rankdict, region)
        try:
            t1player1 = Live_Game.find_emojis(gamedata['Team 1']['player1'][1]) + '|' + gamedata['Team 1']['player1'][0]
            t1player1s = Live_Game.find_emojis(gamedata['Team 1']['player1'][2]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player1'][3])
            t1player1r = Live_Game.find_emojis(gamedata['Team 1']['player1'][4]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player1'][5])
            t1p1rank = new_rank_dict['t1p1']
            t1player1rank = Live_Game.find_emojis(t1p1rank[0][:-2]) + '|' + t1p1rank[0] + ' ' + str(t1p1rank[1]) + 'LP'
            if t1player1rank == 'Unranked| LP':
                t1player1rank = 'Unranked'
        except KeyError:
            t1player1 = ''
            t1player1s = ''
            t1player1r = ''
            t1player1rank = ''
        try:
            t1player2 = Live_Game.find_emojis(gamedata['Team 1']['player2'][1]) + '|' + gamedata['Team 1']['player2'][0]
            t1player2s = Live_Game.find_emojis(gamedata['Team 1']['player2'][2]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player2'][3])
            t1player2r = Live_Game.find_emojis(gamedata['Team 1']['player2'][4]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player2'][5])
            t1p2rank = new_rank_dict['t1p2']
            t1player2rank = Live_Game.find_emojis(t1p2rank[0][:-2]) + '|' + t1p2rank[0] + ' ' + str(t1p2rank[1]) + 'LP'
            if t1player2rank == 'Unranked| LP':
                t1player2rank = 'Unranked'
        except KeyError:
            t1player2 = ''
            t1player2s = ''
            t1player2r = ''
            t1player2rank = ''
        try:
            t1player3 = Live_Game.find_emojis(gamedata['Team 1']['player3'][1]) + '|' + gamedata['Team 1']['player3'][0]
            t1player3s = Live_Game.find_emojis(gamedata['Team 1']['player3'][2]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player3'][3])
            t1player3r = Live_Game.find_emojis(gamedata['Team 1']['player3'][4]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player3'][5])
            t1p3rank = new_rank_dict['t1p3']
            t1player3rank = Live_Game.find_emojis(t1p3rank[0][:-2]) + '|' + t1p3rank[0] + ' ' + str(t1p3rank[1]) + 'LP'
            if t1player3rank == 'Unranked| LP':
                t1player3rank = 'Unranked'
        except KeyError:
            t1player3 = ''
            t1player3s = ''
            t1player3r = ''
            t1player3rank = ''
        try:
            t1player4 = Live_Game.find_emojis(gamedata['Team 1']['player4'][1]) + '|' + gamedata['Team 1']['player4'][0]
            t1player4s = Live_Game.find_emojis(gamedata['Team 1']['player4'][2]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player4'][3])
            t1player4r = Live_Game.find_emojis(gamedata['Team 1']['player4'][4]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player4'][5])
            t1p4rank = new_rank_dict['t1p4']
            t1player4rank = Live_Game.find_emojis(t1p4rank[0][:-2]) + '|' + t1p4rank[0] + ' ' + str(t1p4rank[1]) + 'LP'
            if t1player4rank == 'Unranked| LP':
                t1player4rank = 'Unranked'
        except KeyError:
            t1player4 = ''
            t1player4s = ''
            t1player4r = ''
            t1player4rank = ''
        try:
            t1player5 = Live_Game.find_emojis(gamedata['Team 1']['player5'][1]) + '|' + gamedata['Team 1']['player5'][0]
            t1player5s = Live_Game.find_emojis(gamedata['Team 1']['player5'][2]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player5'][3])
            t1player5r = Live_Game.find_emojis(gamedata['Team 1']['player5'][4]) + \
                Live_Game.find_emojis(gamedata['Team 1']['player5'][5])
            t1p5rank = new_rank_dict['t1p5']
            t1player5rank = Live_Game.find_emojis(t1p5rank[0][:-2]) + '|' + t1p5rank[0] + ' ' + str(t1p5rank[1]) + 'LP'
            if t1player5rank == 'Unranked| LP':
                t1player5rank = 'Unranked'
        except KeyError:
            t1player5 = ''
            t1player5s = ''
            t1player5r = ''
            t1player5rank = ''
        try:
            t2player1 = Live_Game.find_emojis(gamedata['Team 2']['player1'][1]) + '|' + gamedata['Team 2']['player1'][0]
            t2player1s = Live_Game.find_emojis(gamedata['Team 2']['player1'][2]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player1'][3])
            t2player1r = Live_Game.find_emojis(gamedata['Team 2']['player1'][4]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player1'][5])
            t2p1rank = new_rank_dict['t2p1']
            t2player1rank = Live_Game.find_emojis(t2p1rank[0][:-2]) + '|' + t2p1rank[0] + ' ' + str(t2p1rank[1]) + 'LP'
            if t2player1rank == 'Unranked| LP':
                t2player1rank = 'Unranked'
        except KeyError:
            t2player1 = ''
            t2player1s = ''
            t2player1r = ''
            t2player1rank = ''
        try:
            t2player2 = Live_Game.find_emojis(gamedata['Team 2']['player2'][1]) + '|' + gamedata['Team 2']['player2'][0]
            t2player2s = Live_Game.find_emojis(gamedata['Team 2']['player2'][2]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player2'][3])
            t2player2r = Live_Game.find_emojis(gamedata['Team 2']['player2'][4]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player2'][5])
            t2p2rank = new_rank_dict['t2p2']
            t2player2rank = Live_Game.find_emojis(t2p2rank[0][:-2]) + '|' + t2p2rank[0] + ' ' + str(t2p2rank[1]) + 'LP'
            if t2player2rank == 'Unranked| LP':
                t2player2rank = 'Unranked'
        except KeyError:
            t2player2 = ''
            t2player2s = ''
            t2player2r = ''
            t2player2rank = ''
        try:
            t2player3 = Live_Game.find_emojis(gamedata['Team 2']['player3'][1]) + '|' + gamedata['Team 2']['player3'][0]
            t2player3s = Live_Game.find_emojis(gamedata['Team 2']['player3'][2]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player3'][3])
            t2player3r = Live_Game.find_emojis(gamedata['Team 2']['player3'][4]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player3'][5])
            t2p3rank = new_rank_dict['t2p3']
            t2player3rank = Live_Game.find_emojis(t2p3rank[0][:-2]) + '|' + t2p3rank[0] + ' ' + str(t2p3rank[1]) + 'LP'
            if t2player3rank == 'Unranked| LP':
                t2player3rank = 'Unranked'
        except KeyError:
            t2player3 = ''
            t2player3s = ''
            t2player3r = ''
            t2player3rank = ''
        try:
            t2player4 = Live_Game.find_emojis(gamedata['Team 2']['player4'][1]) + '|' + gamedata['Team 2']['player4'][0]
            t2player4s = Live_Game.find_emojis(gamedata['Team 2']['player4'][2]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player4'][3])
            t2player4r = Live_Game.find_emojis(gamedata['Team 2']['player4'][4]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player4'][5])
            t2p4rank = new_rank_dict['t2p4']
            t2player4rank = Live_Game.find_emojis(t2p4rank[0][:-2]) + '|' + t2p4rank[0] + ' ' + str(t2p4rank[1]) + 'LP'
            if t2player4rank == 'Unranked| LP':
                t2player4rank = 'Unranked'
        except KeyError:
            t2player4 = ''
            t2player4s = ''
            t2player4r = ''
            t2player4rank = ''
        try:
            t2player5 = Live_Game.find_emojis(gamedata['Team 2']['player5'][1]) + '|' + gamedata['Team 2']['player5'][0]
            t2player5s = Live_Game.find_emojis(gamedata['Team 2']['player5'][2]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player5'][3])
            t2player5r = Live_Game.find_emojis(gamedata['Team 2']['player5'][4]) + \
                Live_Game.find_emojis(gamedata['Team 2']['player5'][5])
            t2p5rank = new_rank_dict['t2p5']
            t2player5rank = Live_Game.find_emojis(t2p5rank[0][:-2]) + '|' + t2p5rank[0] + ' ' + str(t2p5rank[1]) + 'LP'
            if t2player5rank == 'Unranked| LP':
                t2player5rank = 'Unranked'
        except KeyError:
            t2player5 = ''
            t2player5s = ''
            t2player5r = ''
            t2player5rank = ''
        embed.insert_field_at(index=0, name='**Rank**',
                              value=t2player1rank + '\n' + t2player2rank + '\n' + t2player3rank + '\n' + t2player4rank +
                              '\n' + t2player5rank,
                              inline=True)
        embed.insert_field_at(index=0, name='**Blue Side**',
                              value=t1player1 + '\n' + t1player2 + '\n' + t1player3 + '\n' + t1player4 + '\n' +
                              t1player5,
                              inline=True)
        embed.insert_field_at(index=2, name='**Summs    Runes**',
                              value=t2player1s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player1r + '\n' +
                              t2player2s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player2r + '\n' +
                              t2player3s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player3r + '\n' +
                              t2player4s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player4r + '\n' +
                              t2player5s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player5r,
                              inline=True)
        embed.insert_field_at(index=1, name='**Summs    Runes**',
                              value=t1player1s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player1r + '\n' +
                              t1player2s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player2r + '\n' +
                              t1player3s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player3r + '\n' +
                              t1player4s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player4r + '\n' +
                              t1player5s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player5r,
                              inline=True)
        embed.insert_field_at(index=2, name='**Red Side**',
                              value=t2player1 + '\n' + t2player2 + '\n' + t2player3 + '\n' + t2player4 + '\n' +
                              t2player5,
                              inline=True)
        embed.insert_field_at(index=1, name='**Rank**',
                              value=t1player1rank + '\n' + t1player2rank + '\n' + t1player3rank + '\n' + t1player4rank +
                              '\n' + t1player5rank,
                              inline=True)
        if (t2player1 != '') and (t1player1 != ''):
            message = await ctx.send(embed=embed)
        else:
            message = '{} is in a game alone'.format(name)
            message = await ctx.send(message)
        try:
            MongoDB.collection6.insert_one({'_id': gamedata['gameId'], 'message': message.id,
                                            'channel': ctx.channel.id, 'guild': ctx.guild.id})
            await sleep(2700)
            MongoDB.collection6.delete_one({'_id': gamedata['gameId']})
        except DuplicateKeyError:
            pass

    @commands.command(aliases=["livegameregion", "livegreg", "livegamer", "lgreg", "lgr"],
                      description='Displays a live match for league of legends for given region write ?livegameregion '
                                  '[region] [summoner name] to get live game stats. (Brackets not needed)',
                      brief="Gets live game for lol of a specified summoner",
                      case_insensitive=True)
    async def live_game_lol_region(self, ctx, region, *args):
        name = ''
        for i in range(len(args)):
            name = name + ' ' + args[i]
        name = name[1:]
        if Main_Functions.region_converter_backwards(
                region) == "Invalid region. Use ?helpsetup for a list of valid regions!":
            await ctx.send(Main_Functions.region_converter_backwards(region))
            return
        region = Main_Functions.region_converter_backwards(
                region)
        gamedata = Live_Game.live_match(name, region)
        if gamedata == name + ' not in a live match' or gamedata == 'The summoner ' + name + ' does not exist':
            await ctx.send(gamedata)
            return
        mongo_data = MongoDB.collection6.find_one({'_id': gamedata['gameId']})
        try:
            if mongo_data:
                message = await self.bot.get_guild(mongo_data['guild']).get_channel(
                    mongo_data['channel']).fetch_message(mongo_data['message'])
                embed = message.embeds[0]
                embed.description = 'Game Time: ' + gamedata['gametime']
                await ctx.send(embed=embed)
                return
        except AttributeError:
            pass
        embed = discord.Embed(title=gamedata['gamemode'], description='Game Time: ' + gamedata['gametime'])
        rankdict = {}
        for i in range(gamedata['Team 1 count']):
            rankdict['t1p' + str(i + 1)] = gamedata['Team 1']['player' + str(i + 1)][6]
        for i in range(gamedata['Team 2 count']):
            rankdict['t2p' + str(i + 1)] = gamedata['Team 2']['player' + str(i + 1)][6]
        new_rank_dict = AbsolutelyPog.multiple_summoners_threading(rankdict, region)
        try:
            t1player1 = Live_Game.find_emojis(gamedata['Team 1']['player1'][1]) + '|' + \
                        gamedata['Team 1']['player1'][0]
            t1player1s = Live_Game.find_emojis(gamedata['Team 1']['player1'][2]) + Live_Game.find_emojis(
                gamedata['Team 1']['player1'][3])
            t1player1r = Live_Game.find_emojis(gamedata['Team 1']['player1'][4]) + Live_Game.find_emojis(
                gamedata['Team 1']['player1'][5])
            t1p1rank = new_rank_dict['t1p1']
            t1player1rank = Live_Game.find_emojis(t1p1rank[0][:-2]) + '|' + t1p1rank[0] + ' ' + str(
                t1p1rank[1]) + 'LP'
            if t1player1rank == 'Unranked| LP':
                t1player1rank = 'Unranked'
        except KeyError:
            t1player1 = ''
            t1player1s = ''
            t1player1r = ''
            t1player1rank = ''
        try:
            t1player2 = Live_Game.find_emojis(gamedata['Team 1']['player2'][1]) + '|' + \
                        gamedata['Team 1']['player2'][0]
            t1player2s = Live_Game.find_emojis(gamedata['Team 1']['player2'][2]) + Live_Game.find_emojis(
                gamedata['Team 1']['player2'][3])
            t1player2r = Live_Game.find_emojis(gamedata['Team 1']['player2'][4]) + Live_Game.find_emojis(
                gamedata['Team 1']['player2'][5])
            t1p2rank = new_rank_dict['t1p2']
            t1player2rank = Live_Game.find_emojis(t1p2rank[0][:-2]) + '|' + t1p2rank[0] + ' ' + str(
                t1p2rank[1]) + 'LP'
            if t1player2rank == 'Unranked| LP':
                t1player2rank = 'Unranked'
        except KeyError:
            t1player2 = ''
            t1player2s = ''
            t1player2r = ''
            t1player2rank = ''
        try:
            t1player3 = Live_Game.find_emojis(gamedata['Team 1']['player3'][1]) + '|' + \
                        gamedata['Team 1']['player3'][0]
            t1player3s = Live_Game.find_emojis(gamedata['Team 1']['player3'][2]) + Live_Game.find_emojis(
                gamedata['Team 1']['player3'][3])
            t1player3r = Live_Game.find_emojis(gamedata['Team 1']['player3'][4]) + Live_Game.find_emojis(
                gamedata['Team 1']['player3'][5])
            t1p3rank = new_rank_dict['t1p3']
            t1player3rank = Live_Game.find_emojis(t1p3rank[0][:-2]) + '|' + t1p3rank[0] + ' ' + str(
                t1p3rank[1]) + 'LP'
            if t1player3rank == 'Unranked| LP':
                t1player3rank = 'Unranked'
        except KeyError:
            t1player3 = ''
            t1player3s = ''
            t1player3r = ''
            t1player3rank = ''
        try:
            t1player4 = Live_Game.find_emojis(gamedata['Team 1']['player4'][1]) + '|' + \
                        gamedata['Team 1']['player4'][0]
            t1player4s = Live_Game.find_emojis(gamedata['Team 1']['player4'][2]) + Live_Game.find_emojis(
                gamedata['Team 1']['player4'][3])
            t1player4r = Live_Game.find_emojis(gamedata['Team 1']['player4'][4]) + Live_Game.find_emojis(
                gamedata['Team 1']['player4'][5])
            t1p4rank = new_rank_dict['t1p4']
            t1player4rank = Live_Game.find_emojis(t1p4rank[0][:-2]) + '|' + t1p4rank[0] + ' ' + str(
                t1p4rank[1]) + 'LP'
            if t1player4rank == 'Unranked| LP':
                t1player4rank = 'Unranked'
        except KeyError:
            t1player4 = ''
            t1player4s = ''
            t1player4r = ''
            t1player4rank = ''
        try:
            t1player5 = Live_Game.find_emojis(gamedata['Team 1']['player5'][1]) + '|' + \
                        gamedata['Team 1']['player5'][0]
            t1player5s = Live_Game.find_emojis(gamedata['Team 1']['player5'][2]) + Live_Game.find_emojis(
                gamedata['Team 1']['player5'][3])
            t1player5r = Live_Game.find_emojis(gamedata['Team 1']['player5'][4]) + Live_Game.find_emojis(
                gamedata['Team 1']['player5'][5])
            t1p5rank = new_rank_dict['t1p5']
            t1player5rank = Live_Game.find_emojis(t1p5rank[0][:-2]) + '|' + t1p5rank[0] + ' ' + str(
                t1p5rank[1]) + 'LP'
            if t1player5rank == 'Unranked| LP':
                t1player5rank = 'Unranked'
        except KeyError:
            t1player5 = ''
            t1player5s = ''
            t1player5r = ''
            t1player5rank = ''
        try:
            t2player1 = Live_Game.find_emojis(gamedata['Team 2']['player1'][1]) + '|' + \
                        gamedata['Team 2']['player1'][0]
            t2player1s = Live_Game.find_emojis(gamedata['Team 2']['player1'][2]) + Live_Game.find_emojis(
                gamedata['Team 2']['player1'][3])
            t2player1r = Live_Game.find_emojis(gamedata['Team 2']['player1'][4]) + Live_Game.find_emojis(
                gamedata['Team 2']['player1'][5])
            t2p1rank = new_rank_dict['t2p1']
            t2player1rank = Live_Game.find_emojis(t2p1rank[0][:-2]) + '|' + t2p1rank[0] + ' ' + str(
                t2p1rank[1]) + 'LP'
            if t2player1rank == 'Unranked| LP':
                t2player1rank = 'Unranked'
        except KeyError:
            t2player1 = ''
            t2player1s = ''
            t2player1r = ''
            t2player1rank = ''
        try:
            t2player2 = Live_Game.find_emojis(gamedata['Team 2']['player2'][1]) + '|' + \
                        gamedata['Team 2']['player2'][0]
            t2player2s = Live_Game.find_emojis(gamedata['Team 2']['player2'][2]) + Live_Game.find_emojis(
                gamedata['Team 2']['player2'][3])
            t2player2r = Live_Game.find_emojis(gamedata['Team 2']['player2'][4]) + Live_Game.find_emojis(
                gamedata['Team 2']['player2'][5])
            t2p2rank = new_rank_dict['t2p2']
            t2player2rank = Live_Game.find_emojis(t2p2rank[0][:-2]) + '|' + t2p2rank[0] + ' ' + str(
                t2p2rank[1]) + 'LP'
            if t2player2rank == 'Unranked| LP':
                t2player2rank = 'Unranked'
        except KeyError:
            t2player2 = ''
            t2player2s = ''
            t2player2r = ''
            t2player2rank = ''
        try:
            t2player3 = Live_Game.find_emojis(gamedata['Team 2']['player3'][1]) + '|' + \
                        gamedata['Team 2']['player3'][0]
            t2player3s = Live_Game.find_emojis(gamedata['Team 2']['player3'][2]) + Live_Game.find_emojis(
                gamedata['Team 2']['player3'][3])
            t2player3r = Live_Game.find_emojis(gamedata['Team 2']['player3'][4]) + Live_Game.find_emojis(
                gamedata['Team 2']['player3'][5])
            t2p3rank = new_rank_dict['t2p3']
            t2player3rank = Live_Game.find_emojis(t2p3rank[0][:-2]) + '|' + t2p3rank[0] + ' ' + str(
                t2p3rank[1]) + 'LP'
            if t2player3rank == 'Unranked| LP':
                t2player3rank = 'Unranked'
        except KeyError:
            t2player3 = ''
            t2player3s = ''
            t2player3r = ''
            t2player3rank = ''
        try:
            t2player4 = Live_Game.find_emojis(gamedata['Team 2']['player4'][1]) + '|' + \
                        gamedata['Team 2']['player4'][0]
            t2player4s = Live_Game.find_emojis(gamedata['Team 2']['player4'][2]) + Live_Game.find_emojis(
                gamedata['Team 2']['player4'][3])
            t2player4r = Live_Game.find_emojis(gamedata['Team 2']['player4'][4]) + Live_Game.find_emojis(
                gamedata['Team 2']['player4'][5])
            t2p4rank = new_rank_dict['t2p4']
            t2player4rank = Live_Game.find_emojis(t2p4rank[0][:-2]) + '|' + t2p4rank[0] + ' ' + str(
                t2p4rank[1]) + 'LP'
            if t2player4rank == 'Unranked| LP':
                t2player4rank = 'Unranked'
        except KeyError:
            t2player4 = ''
            t2player4s = ''
            t2player4r = ''
            t2player4rank = ''
        try:
            t2player5 = Live_Game.find_emojis(gamedata['Team 2']['player5'][1]) + '|' + \
                        gamedata['Team 2']['player5'][0]
            t2player5s = Live_Game.find_emojis(gamedata['Team 2']['player5'][2]) + Live_Game.find_emojis(
                gamedata['Team 2']['player5'][3])
            t2player5r = Live_Game.find_emojis(gamedata['Team 2']['player5'][4]) + Live_Game.find_emojis(
                gamedata['Team 2']['player5'][5])
            t2p5rank = new_rank_dict['t2p5']
            t2player5rank = Live_Game.find_emojis(t2p5rank[0][:-2]) + '|' + t2p5rank[0] + ' ' + str(
                t2p5rank[1]) + 'LP'
            if t2player5rank == 'Unranked| LP':
                t2player5rank = 'Unranked'
        except KeyError:
            t2player5 = ''
            t2player5s = ''
            t2player5r = ''
            t2player5rank = ''
        embed.insert_field_at(index=0, name='**Rank**',
                              value=t2player1rank + '\n' + t2player2rank + '\n' + t2player3rank + '\n' + t2player4rank +
                              '\n' + t2player5rank,
                              inline=True)
        embed.insert_field_at(index=0, name='**Blue Side**',
                              value=t1player1 + '\n' + t1player2 + '\n' + t1player3 + '\n' + t1player4 + '\n' +
                              t1player5,
                              inline=True)
        embed.insert_field_at(index=2, name='**Summs    Runes**',
                              value=t2player1s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player1r + '\n' +
                              t2player2s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player2r + '\n' +
                              t2player3s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player3r + '\n' +
                              t2player4s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player4r + '\n' +
                              t2player5s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t2player5r,
                              inline=True)
        embed.insert_field_at(index=1, name='**Summs    Runes**',
                              value=t1player1s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player1r + '\n' +
                              t1player2s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player2r + '\n' +
                              t1player3s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player3r + '\n' +
                              t1player4s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player4r + '\n' +
                              t1player5s + ' \u200b \u200b \u200b \u200b \u200b \u200b' + t1player5r,
                              inline=True)
        embed.insert_field_at(index=2, name='**Red Side**',
                              value=t2player1 + '\n' + t2player2 + '\n' + t2player3 + '\n' + t2player4 + '\n' +
                              t2player5,
                              inline=True)
        embed.insert_field_at(index=1, name='**Rank**',
                              value=t1player1rank + '\n' + t1player2rank + '\n' + t1player3rank + '\n' + t1player4rank +
                              '\n' + t1player5rank,
                              inline=True)

        if (t2player1 != '') and (t1player1 != ''):
            message = await ctx.send(embed=embed)
        else:
            message = '{} is in a game alone'.format(name)
            message = await ctx.send(message)
        try:
            MongoDB.collection6.insert_one({'_id': gamedata['gameId'], 'message': message.id,
                                            'channel': ctx.channel.id, 'guild': ctx.guild.id})
            await sleep(2700)
            MongoDB.collection6.delete_one({'_id': gamedata['gameId']})
        except DuplicateKeyError:
            pass


def setup(bot):
    bot.add_cog(LiveGame(bot))
