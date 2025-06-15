from discord.ext import commands
import Clash
import discord
import MongoDB


class ClashInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clash",
                      description='Displays information about upcoming clash tournaments.',
                      brief="Upcoming clash events!",
                      case_insensitive=True)
    async def clash_info(self, ctx):
        collection = MongoDB.collection.find_one(ctx.guild.id)
        region = collection["region"]
        tz = collection["tz"]
        info = Clash.getclashdate(region, tz)
        name = ''
        reg = ''
        start = ''
        embed = discord.Embed(title="Upcoming Clash Tournaments", color=0x0000FF)
        for key in Clash.sort(info):
            name = name + key + "\n"
            reg = reg + info[key][0] + " " + collection["tz"].upper() + "\n"
            start = start + info[key][1] + " " + collection["tz"].upper() + "\n"
        if name:
            embed.add_field(name='Tournament Name',
                            value=name,
                            inline=True)
            embed.add_field(name='Registration Time',
                            value=reg,
                            inline=True)
            embed.add_field(name='Start Time',
                            value=start,
                            inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('No clash dates were found in the near future')


def setup(bot):
    bot.add_cog(ClashInfo(bot))
