from discord.ext import commands
import Main_Functions
from discord.ext.commands import MissingPermissions
import MongoDB


class TwitterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    '''
    Commands related to Twitter
    '''

    @commands.command(name="sendtweets",
                      description='Choose the channel you want to send tweets for a specific game '
                                  'write ?sendtweets [game] to send live tweets in the channel you typed the command.'
                                  '(Brackets not needed)',
                      brief="Streams live tweets for a given game.",
                      case_insensitive=True)
    @commands.has_permissions(administrator=True)
    async def tweet_send(self, ctx, game):
        server = ctx.guild
        server_stats = MongoDB.collection.find_one(server.id)
        Main_Functions.tweetdict = server_stats['tweetdict']
        await ctx.send(Main_Functions.send_tweets(game, ctx.channel, Main_Functions.tweetdict))
        MongoDB.collection.update_one({"_id": server.id}, {"$set": {"tweetdict": Main_Functions.tweetdict}})

    '''
    Handles the error for when a user tries to call this command and is not an administrator
    '''
    @tweet_send.error
    async def send_tweet_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have the permission for this command".format(ctx.message.author.mention)
            await ctx.send(text)

    @commands.command(name="stoptweets",
                      description='Choose the channel you want to stop sending tweets for a specific game '
                                  'write ?stoptweets [game] to stop sending live tweets in the channel you typed the '
                                  'command.(Brackets not needed)',
                      brief="Stops streaming live tweets for a given game.",
                      case_insensitive=True)
    @commands.has_permissions(administrator=True)
    async def tweet_stop(self, ctx, game):
        server = ctx.guild
        server_stats = MongoDB.collection.find_one(server.id)
        Main_Functions.tweetdict = server_stats['tweetdict']
        await ctx.send(Main_Functions.stop_tweets(game, ctx.channel, Main_Functions.tweetdict))
        MongoDB.collection.update_one({"_id": server.id}, {"$set": {"tweetdict": Main_Functions.tweetdict}})

    '''
    Handles the error for when a user tries to call this command and is not an administrator
    '''
    @tweet_stop.error
    async def stop_tweet_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have the permission for this command".format(ctx.message.author.mention)
            await ctx.send(text)

    @commands.command(name="tweets",
                      description='Displays a list of the games where live tweets are currently active. '
                                  'write ?tweets',
                      brief="Displays subscribed live tweets",
                      case_insensitive=True)
    async def twit(self, ctx):
        server = ctx.guild
        server_stats = MongoDB.collection.find_one(server.id)
        Main_Functions.tweetdict = server_stats['tweetdict']
        await ctx.send(Main_Functions.tweets(Main_Functions.tweetdict))


def setup(bot):
    bot.add_cog(TwitterCommands(bot))
