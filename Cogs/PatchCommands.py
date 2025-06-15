from discord.ext import commands
import discord
import Main_Functions
from discord.ext.commands import MissingPermissions
import MongoDB
import PatchNotes


class PatchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sendpatch",
                      description='Sends live patch notes for the given game in the channel you sent the message. '
                                  'write ?sendpatch [game] to send live patch notes. (Brackets not needed)',
                      brief="Sends live patch notes for a given game.",
                      case_insensitive=True)
    @commands.has_permissions(administrator=True)
    async def sendpat(self, ctx, game):
        server = ctx.guild
        server_stats = MongoDB.collection.find_one(server.id)
        Main_Functions.patchdict = server_stats['patchdict']
        await ctx.send(Main_Functions.send_patch(game, ctx.channel, Main_Functions.patchdict))
        MongoDB.collection.update_one({"_id": server.id}, {"$set": {"patchdict": Main_Functions.patchdict}})
        if game == 'LoL' or game.lower() == 'league' or game.lower() == 'league of legends' or game.lower() == 'lol':
            try:
                imageurl = PatchNotes.currentpatchpic('lol')
            except AttributeError:
                imageurl = PatchNotes.currentpatchpicmetadata('lol')
            metadata = PatchNotes.metadata(PatchNotes.currentpatch('lol'))
            if '&#x27;' in metadata['description']:
                metadata['description'] = metadata['description'].replace('&#x27;', "'")
            embed = discord.Embed(title=metadata['title'], description=metadata['description'],
                                  url=PatchNotes.currentpatch('lol'), color=0x33FFEE)
            embed.set_image(url=imageurl)
            embed.set_thumbnail(url=metadata['thumbnail'])
            await ctx.send(embed=embed)
        elif game == 'TFT' or game == 'Teamfight Tactics' or game == 'Team fight Tactics' or game.lower() == 'tft' \
                or game.lower() == 'team fight tactics' or game.lower() == 'teamfight tactics':
            try:
                imageurl = PatchNotes.currentpatchpic('tft')
            except AttributeError:
                imageurl = PatchNotes.currentpatchpicmetadata('tft')
            metadata = PatchNotes.metadata(PatchNotes.currentpatch('tft'))
            if '&#x27;' in metadata['description']:
                metadata['description'] = metadata['description'].replace('&#x27;', "'")
            embed = discord.Embed(title=metadata['title'], description=metadata['description'],
                                  url=PatchNotes.currentpatch(game), color=0x33FFEE)
            embed.set_image(url=imageurl)
            embed.set_thumbnail(url=metadata['thumbnail'])
            await ctx.send(embed=embed)
        elif game == 'Valorant' or game.lower() == 'val' or game.lower() == 'valorant' or game == 'Val':
            try:
                imageurl = PatchNotes.currentpatchpic('val')
            except AttributeError:
                imageurl = PatchNotes.currentpatchpicmetadata('val')
            metadata = PatchNotes.metadata(PatchNotes.currentpatch('val'))
            if '&#x27;' in metadata['description']:
                metadata['description'] = metadata['description'].replace('&#x27;', "'")
            embed = discord.Embed(title=metadata['title'], description=metadata['description'],
                                  url=PatchNotes.currentpatch('val'), color=0x33FFEE)
            embed.set_image(url=imageurl)
            embed.set_thumbnail(url=metadata['thumbnail'])
            await ctx.send(embed=embed)

    @sendpat.error
    async def sendpat_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have the permission for this command".format(ctx.message.author.mention)
            await ctx.send(text)

    @commands.command(aliases=["stoppatch", "stoppatches"],
                      description='Stops sending live patch notes for the given game in the channel you sent the '
                                  'message. write ?stoppatch [game] to stop receiving live patch notes. '
                                  '(Brackets not needed)',
                      brief="Stops sending live patch notes for a given game.",
                      case_insensitive=True)
    @commands.has_permissions(administrator=True)
    async def stoppat(self, ctx, game):
        server = ctx.guild
        server_stats = MongoDB.collection.find_one(server.id)
        Main_Functions.patchdict = server_stats['patchdict']
        await ctx.send(Main_Functions.stop_patch(game, ctx.channel, Main_Functions.patchdict))
        MongoDB.collection.update_one({"_id": server.id}, {"$set": {"patchdict": Main_Functions.patchdict}})

    @stoppat.error
    async def stoppat_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have the permission for this command".format(ctx.message.author.mention)
            await ctx.send(text)

    @commands.command(name="patch",
                      description='Displays a list of the games where live patch notes are currently active. '
                                  'write ?patch',
                      brief="Displays subscribed live patch notes",
                      case_insensitive=True)
    async def pat(self, ctx):
        server = ctx.guild
        server_stats = MongoDB.collection.find_one(server.id)
        Main_Functions.patchdict = server_stats['patchdict']
        await ctx.send(Main_Functions.patchnotes(Main_Functions.patchdict))

    @commands.command(aliases=["currentpatch", "cp", "cpatch"],
                      description='Displays the current patch notes for a game given the patch notes. Written in the'
                                  'format ?currentpatch [game] to choose the game. (brackets not include)',
                      brief="Gets the current patch for a given game",
                      case_insensitive=True)
    async def currentpat(self, ctx, game):
        try:
            imageurl = PatchNotes.currentpatchpic(game)
        except AttributeError:
            imageurl = PatchNotes.currentpatchpicmetadata(game)
        metadata = PatchNotes.metadata(PatchNotes.currentpatch(game))
        if '&#x27;' in metadata['description']:
            metadata['description'] = metadata['description'].replace('&#x27;', "'")
        embed = discord.Embed(title=metadata['title'], description=metadata['description'],
                              url=PatchNotes.currentpatch(game), color=0x33FFEE)
        embed.set_image(url=imageurl)
        embed.set_thumbnail(url=metadata['thumbnail'])
        await ctx.send(embed=embed)
        return


def setup(bot):
    bot.add_cog(PatchCommands(bot))
