from discord.ext import commands
from discord.ext.commands import MissingPermissions
import MongoDB
import discord


class Timezone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["settz", "settimezone"],
                      description='Sets timezone for the server.',
                      brief="Timezone set for clash events!",
                      case_insensitive=True)
    async def set_time(self, ctx, tz):
        listtz = ["gmt", "bst", "cest", "eest", "edt", "cdt", "mdt", "pdt", "msk"]
        if tz.lower() not in listtz:
            await ctx.send("Sorry that is not a supported timezone. See ?helptz for valid timezones.")
            return
        else:
            MongoDB.collection.update({"_id": ctx.guild.id}, {'$set': {'tz': tz.lower()}})
            embed = discord.Embed(title="Your timezone has been set to " + tz.upper() + "!",
                                  color=0x0000FF)
            await ctx.send(embed=embed)

    @set_time.error
    async def set_region_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have the permission for this command".format(ctx.message.author.mention)
            await ctx.send(text)

    @commands.command(aliases=["mytz", "mytimezone"],
                      description='Sets timezone for the server.',
                      brief="Timezone set for clash events!",
                      case_insensitive=True)
    async def my_time(self, ctx):
        mine = MongoDB.collection.find_one({"_id": ctx.guild.id})
        embed = discord.Embed(title="Your timezone is " + mine["tz"].upper() + "!",
                              color=0x0000FF)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Timezone(bot))
