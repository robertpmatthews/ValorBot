from discord.ext import commands
import Main_Functions
import discord
import MongoDB


class RankCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    '''
    Commands related to League of Legends
    '''

    @commands.command(name="ranklol",
                      description='Gets the rank of the inputted summoner in Solo and Flex League.',
                      brief="Gets LOL Rank",
                      case_insensitive=True)
    async def rank(self, ctx, *args):
        name = ''
        for i in range(len(args)):
            name = name + ' ' + args[i]
        name = name[1:]
        collection = MongoDB.collection.find_one(ctx.guild.id)
        region = collection["region"]
        my_str = Main_Functions.getranklol(name, region)
        if my_str == "Summoner name " + name + " not found":
            await ctx.send(my_str)
        else:
            embed = discord.Embed(title=name, color=0xFFDF00)
            embed.add_field(name='Solo Queue Rank',
                            value=my_str[0] + '\n' + my_str[1] + '\n' + my_str[2],
                            inline=True)
            embed.add_field(name='Flex Queue Rank',
                            value=my_str[3] + '\n' + my_str[4] + '\n' + my_str[5],
                            inline=True)
            embed.add_field(name='Champion Mastery',
                            value=my_str[7])
            embed.add_field(name='Live Game',
                            value=my_str[6],
                            inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="ranktft",
                      description='Gets the rank of the inputted summoner in TFT',
                      brief="Gets TFT Rank",
                      case_insensitive=True)
    async def ranktft(self, ctx, *args):
        name = ''
        for i in range(len(args)):
            name = name + ' ' + args[i]
        name = name[1:]
        collection = MongoDB.collection.find_one(ctx.guild.id)
        region = collection["region"]
        my_str = Main_Functions.get_rank_tft(name, region)
        if my_str == "Summoner name " + name + " not found":
            await ctx.send(my_str)
        else:
            embed = discord.Embed(title=name, color=0xFFDF00)
            embed.add_field(name='TFT Rank',
                            value=my_str[0] + '\n' + my_str[1],
                            inline=True)
            await ctx.send(embed=embed)

    @commands.command(name="rankregion",
                      description='Gets the rank of the Summoner for the given region. '
                                  'Use ?rankregion [region] [summoner]',
                      brief='Gets rank for LoL',
                      case_insensitive=True)
    async def rankregion(self, ctx, *args):
        name = ''
        region = args[0]
        for i in range(1, len(args)):
            name = name + ' ' + args[i]
        name = name[1:]
        if Main_Functions.region_converter_backwards(region) == "Invalid region. Use ?helpsetup for a list of valid " \
                                                                "regions!":
            await ctx.send(Main_Functions.region_converter_backwards(region))
            return
        my_str = Main_Functions.getranklol(name, Main_Functions.region_converter_backwards(region))
        if my_str == "Summoner name " + name + " not found":
            await ctx.send(my_str)
        else:
            embed = discord.Embed(title=name, color=0xFFDF00)
            embed.add_field(name='Solo Queue Rank',
                            value=my_str[0] + '\n' + my_str[1] + '\n' + my_str[2],
                            inline=True)
            embed.add_field(name='Flex Queue Rank',
                            value=my_str[3] + '\n' + my_str[4] + '\n' + my_str[5],
                            inline=True)
            embed.add_field(name='Live Game',
                            value=my_str[6],
                            inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="rankregiontft",
                      description='Gets the rank of the Summoner for the given region. Use ?rankregion [region] '
                                  '[summoner]',
                      brief='Gets rank for TFT',
                      case_insensitive=True)
    async def rankregiontft(self, ctx, region, *args):
        name = ''
        for i in range(len(args)):
            name = name + ' ' + args[i]
        name = name[1:]
        if Main_Functions.region_converter_backwards(
                region) == "Invalid region. Use ?helpsetup for a list of valid regions!":
            await ctx.send(Main_Functions.region_converter_backwards(region))
            return
        my_str = Main_Functions.get_rank_tft(name, Main_Functions.region_converter_backwards(region))
        if my_str == "Summoner name " + name + " not found":
            await ctx.send(my_str)
        else:
            embed = discord.Embed(title=name, color=0xFFDF00)
            embed.add_field(name='TFT Rank',
                            value=my_str[0] + '\n' + my_str[1],
                            inline=True)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(RankCommands(bot))
