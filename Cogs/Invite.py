from discord.ext import commands
import discord


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite",
                      description='Gives invite link for ValorBot.',
                      brief="Invite the bot to your discord server!",
                      case_insensitive=True)
    async def invitation(self, ctx):
        link = 'https://discord.com/api/oauth2/authorize?client_id=712422704644489267&permissions=335898816&scope=bot'
        embed = discord.Embed(title='Invite Link',
                              description='Use this to add ValorBot to your server!',
                              url=link, color=0x33FFEE)
        await ctx.send(embed=embed)

    @commands.command(name="support",
                      description='Gives support server link for ValorBot.',
                      brief="Join the ValorBot support Server!",
                      case_insensitive=True)
    async def support(self, ctx):
        link = 'https://discord.gg/sqNChCw'
        embed = discord.Embed(title='Support Link',
                              description='Use this to join the ValorBot support server!',
                              url=link, color=0x33FFEE)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Invite(bot))
