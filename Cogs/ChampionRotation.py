from discord.ext import commands
import FreeChamp
import discord
import MongoDB


class ChampionRotation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="freechamps",
                      description='Displays all the free champions for a given region\'s current champion rotation.',
                      brief="Gets free champ rotation!",
                      case_insensitive=True)
    async def free_champs(self, ctx):
        collection = MongoDB.collection.find_one(ctx.guild.id)
        region = collection["region"]
        champs = FreeChamp.champ_rotation(region)
        embed = discord.Embed(title="Free Champion Rotation", color=0x0000FF)
        embed.add_field(name='Champions',
                        value=champs,
                        inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ChampionRotation(bot))
