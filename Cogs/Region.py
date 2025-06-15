from discord.ext import commands
import MongoDB
import discord
from discord.ext.commands import MissingPermissions
import Main_Functions


class Region(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="setregion",
                      description='Enter the region you want to use!',
                      brief="Set the region for the server",
                      case_insensitive=True)
    async def set_region(self, ctx, *args):
        name = ''
        for i in range(len(args)):
            name = name + ' ' + args[i]
        name = name[1:]
        if name.lower() == "na":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "na1"}})
            embed = discord.Embed(title="Region has been set to NA!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "euw":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "euw1"}})
            embed = discord.Embed(title="Region has been set to EUW!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "eune":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "eun1"}})
            embed = discord.Embed(title="Region has been set to EUNE!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "oce":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "oc1"}})
            embed = discord.Embed(title="Region has been set to OCE!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "kr":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "kr"}})
            embed = discord.Embed(title="Region has been set to KR!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "jp":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "jp1"}})
            embed = discord.Embed(title="Region has been set to JP!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "br":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "br1"}})
            embed = discord.Embed(title="Region has been set to BR!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "las":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "la1"}})
            embed = discord.Embed(title="Region has been set to LAS!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "lan":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "la2"}})
            embed = discord.Embed(title="Region has been set to LAN!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "ru":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "ru"}})
            embed = discord.Embed(title="Region has been set to RU!", color=0x0000FF)
            await ctx.send(embed=embed)
        elif name.lower() == "tr":
            MongoDB.collection.update({"_id": ctx.guild.id}, {"$set": {"region": "tr1"}})
            embed = discord.Embed(title="Region has been set to TR!", color=0x0000FF)
            await ctx.send(embed=embed)
        else:
            text = "Sorry {} that region doesn't exist! Try using ?helpsetup to see accepted regions!"
            text2 = text.format(ctx.message.author.mention)
            await ctx.send(text2)

    @set_region.error
    async def set_region_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have the permission for this command".format(ctx.message.author.mention)
            await ctx.send(text)

    @commands.command(name="myregion",
                      description='Gets region of server!',
                      brief="Get the region for the server",
                      case_insensitive=True)
    async def my_region(self, ctx):
        guild = MongoDB.collection.find_one({"_id": ctx.guild.id})
        my_region = guild["region"]
        embed = discord.Embed(title="Your region is " +
                                    Main_Functions.region_converter(my_region) + "!", color=0x0000FF)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Region(bot))
