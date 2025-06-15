from discord.ext import commands
import discord


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help",
                      brief="Displays all the commands for the server and a description on what they do",
                      case_insensitive=True)
    async def help(self, ctx):
        embed = discord.Embed(title='__**Valor Bot Commands**__',
                              description='Here are some **acceptable forms of each game input**: '
                              + '\n' + "**League of Legends:** LoL, League, League of Legends, or lol" + '\n' +
                              "**Valorant:** val, Valorant, or valorant" + '\n' +
                              "**Teamfight Tactics:** TFT, Teamfight Tactics, Team fight Tactics, tft, team fight "
                              "tactics, or teamfight tactics" + '\n' +
                              "**Legends of Runeterra:** lor, LoR, Legends of Runeterra, or legends of runeterra")
        embed.add_field(name='__**Tweet Commands**__',
                        value='**?tweets** - This lets you know which games have live tweets enabled on this server',
                        inline=False)
        embed.add_field(name='__**Patch Notes Commands**__ *Does not support Legends of Runeterra*',
                        value='**?currentpatch game** - This is used to view the current patch of '
                              'whichever game you put.' + '\n' +
                              '**?patch** - This lets you know which games have live patch notes enabled on this '
                              'server',
                        inline=False)
        embed.add_field(name='__**League of Legends Commmands**__',
                        value="**?ranklol summoner-name** -  Tells you the summoner's rank in "
                              'solo queue, flex queue, and if they are in a live game! Use ?ranktft for TFT.' + '\n' +
                              '**?rankregion region summoner-name** - Used to get rank of a summoner that is a '
                              'different region than the servers set region.' + '\n' +
                              '**?livegame summoner-name** - Will give detailed'
                              ' information on the league game that they are currently in, if they are in one.' + '\n' +
                              "**?livegameregion region summoner-name** - Gets live game for summoners in other "
                              "regions!" + "\n" +
                              '**?clash** - This will display when the upcoming clash dates!' + '\n' +
                              '**?freechamps** - This will display all the current free champion rotation for all you '
                              'norms players!' + '\n' +
                              '**?myregion** - Looks up the region of this server',
                        inline=False)
        embed.add_field(name='__**Leaderboards**__ *Only supported for League of Legends and TFT*',
                        value='**?helpleaderboard** - This displays all the commands for our leaderboard feature!',
                        inline=False)
        embed.add_field(name='__**Invite and Support**__',
                        value='**?invite** - Use this to get the invite link to add ValorBot to your server' + '\n' +
                              '**?support** - Use this to get support link to join the ValorBot Discord server to ask '
                              'questions, give suggestions, report bugs, or talk to the devs',
                        inline=False)
        embed.set_footer(text='If you have any questions about Valor Bot, the best place to reach the devs is at '
                              'our discord support server: https://discord.gg/sqNChCw')
        await ctx.send(embed=embed)

    @commands.command(name='helpsetup',
                      brief='Displays all the commands for server setup',
                      case_insensitive=True)
    async def helpsetup(self, ctx):
        embed = discord.Embed(title='__**Valor Bot Setup Commands**__',
                              description='**Please reference these commands if this is your first time using '
                                          'Valor Bot on this server!**' + '\n' + 'Here are some '
                                          '**acceptable forms of each game input**: '
                                          + '\n' + "**League of Legends:** LoL, League, League of Legends, or lol"
                                          + '\n' +
                                          "**Valorant:** val, Valorant, or valorant" + '\n' +
                                          "**Teamfight Tactics:** TFT, Teamfight Tactics, Team fight Tactics, tft, team"
                                          " fight tactics, "
                                          "or teamfight tactics" + '\n' +
                                          "**Legends of Runeterra:** lor, LoR, Legends of Runeterra, or legends of "
                                          "runeterra" + '\n' +
                                          "**Riot Games: **riot, Riot Games, Riot.")
        embed.add_field(name='__**Server Setup Commands**__ - These commands are for admins only',
                        value='**?setregion region** - This command sets the default region for this server. Current '
                              'options: '
                              'na, euw, eune, oce, kr, jp, br, las, lan, ru, and tr (capatalization does not matter)'
                              + '\n' +
                              '**?sendtweets game** - Use this command to set up the text channel that you wish to '
                              'receive live tweets in, you will not receive these tweets until you run this command. '
                              'If you wish to change the channel simply run this command again.' + '\n' +
                              '**?sendpatch game** - Use this command to set up the text channel that you wish to '
                              'receive live patch notes in, this will send tweets to the text channel for the '
                              'respective game if you wish to change the channel simply run this command again.' +
                              '\n' +
                              '**?stoptweets game** - This is used to disable live tweets for this game'
                              + '\n' +
                              '**?stoppatch game** - This is used to disable live patch notes for this game',
                        inline=False)
        embed.set_footer(text='If you have any questions about Valor Bot, the best place to reach the devs is at '
                              'our discord support server: https://discord.gg/sqNChCw')
        await ctx.send(embed=embed)

    @commands.command(name='helpleaderboard',
                      brief='Displays all the commands for leaderboards, only currently applies to League of '
                            'Legends/TFT',
                      case_insensitive=True)
    async def helpleaderboard(self, ctx):
        embed = discord.Embed(title='__**Valor Bot Leaderboard Commands**__',
                              description='This is the local leaderboards, it is a feature that allows you to make a'
                                          'group and track ranks and compete against your friends to see who comes out'
                                          'on top. Add tft to the end of each command for TFT leaderboards!')
        embed.add_field(name='__**Leaderboards**__ *Only supported for League of Legends/TFT, use ?makegroup first!*',
                        value='**?makegroup group-name** - Makes a leaderboard group. '
                              'Whatever name you choose will be how you see the leaderboard later so make sure to name '
                              'it something you can remember.' + '\n' +
                              "**?makegroupregion region group-name** - Makes group for a different region than server "
                              "default." + "\n" +
                              '**?addplayer summoner-name** - Adds a summoner to your group, only the group '
                              'leader can do this!' + '\n' +
                              '**?leaderboard group-name** - Type the group name that you want to lookup, anyone can do'
                              ' this it does not have to be your group!',
                        inline=False)
        embed.add_field(name='__**Leaderboard Administrative Commands**__ *make sure you are a group owner before '
                             'using these commands*',
                        value='**?mygroup** - Displays the leaderboard name that you own (if you own one).' + '\n' +
                              '**?removeplayer summoner name** - Deletes a summoner from your group, only the group '
                              'leader can do this!' + '\n' +
                              '**?renamegroup new-group-name** - Type the new group name that you wish to use' + '\n' +
                              '**?deletegroup** - This deletes the group that you own!',
                        inline=False)
        embed.set_footer(text='If you have any questions about Valor Bot, the best place to reach the devs is at '
                              'our discord support server: https://discord.gg/sqNChCw')
        await ctx.send(embed=embed)

    @commands.command(name='helptz',
                      brief='Displays all valid timezones for upcoming clash dates',
                      case_insensitive=True)
    async def helptz(self, ctx):
        embed = discord.Embed(title='__**Valor Bot Timezone Help**__',
                              description="Valid Timezones (currently): **edt** (New York, USA), **cdt** (Chicago, USA)"
                                          ", **mdt** (Edmonton, Alberta), **pdt** (Los Angeles, USA), **gmt** "
                                          "(greenwich mean time), **bst** (London, UK), **cest** (Brussels, Belgium), "
                                          "**eest** (Bucharest, Romania), **msk** (Moscow, Russia)",)
        embed.add_field(name='__**Timezone Commands**__',
                        value='**?settz/settimezone** - Set timezone to one of above timezones (admin only command).'
                              + '\n' + '**?mytz/mytimezone** - See what time zone the server is set to.'
                        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
