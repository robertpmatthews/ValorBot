from discord.ext import commands, tasks
import discord
import asyncio
import MongoDB
import Credentials
import PatchNotes

BOT_PREFIX = "?"

bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)

# Removing the help command so that we can implement our own
bot.remove_command('help')

client = discord.Client()

'''
This add the guild to the database when it joins for the first time, it also displays an informative welcome message.
'''


@bot.event
async def on_guild_join(guild):
    if not guild.unavailable:
        MongoDB.insert_post(guild.id, guild.name, guild.member_count)
    else:
        MongoDB.insert_post(guild.id, "Placeholder", 0)
    async for entry in guild.audit_logs(action=discord.AuditLogAction.bot_add, limit=5):
        user_id = int('{0.user.id}'.format(entry))
        target_id = int('{0.target.id}'.format(entry))
        if target_id == 712422704644489267:
            print("true")
            user = bot.get_user(user_id)
            embed = discord.Embed(title='__**Valor Bot Setup Commands**__',
                                  description='**Please reference these commands if this is your first time using '
                                              'Valor Bot on this server!**' + '\n' + 'Here are some '
                                              '**acceptable forms of each game input**: '
                                              + '\n' + "**League of Legends:** LoL, League, League of Legends, or lol"
                                              + '\n' +
                                              "**Valorant:** val, Valorant, or valorant" + '\n' +
                                              "**Teamfight Tactics:** TFT, Teamfight Tactics, Team fight Tactics, tft, "
                                              "team fight tactics, "
                                              "or teamfight tactics" + '\n' +
                                              "**Legends of Runeterra:** lor, LoR, Legends of Runeterra, or legends of "
                                              "runeterra" + '\n' +
                                              "**Riot Games: **riot, Riot Games, Riot.")
            embed.add_field(name='__**Server Setup Commands**__ - These commands are for admins only',
                            value='**?setregion region** - This command sets the default region for this server. '
                                  'Current options: na, euw, eune, oce, kr, jp, br, las, lan, ru, and tr '
                                  '(capatalization does not matter)'
                                  + '\n' +
                                  '**?sendtweets game** - Use this command to set up the text channel that you wish to '
                                  'receive live tweets in, you will not receive these tweets until you run this '
                                  'command. If you wish to change the channel simply run this command again.' + '\n' +
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
            await user.send(embed=embed)
            await user.send("Use ?help for other commands and ?helptz for timezone help.")
            return

'''
This removes the guild from the database if they kick it from the server
'''


@bot.event
async def on_guild_remove(guild):
    MongoDB.collection.delete_one({'_id': guild.id})
    channel = bot.get_channel(739947843011477635)
    await channel.send(str(guild.name) + " removed the bot :(")

'''
This removes the group from the database if a user leaves the server
'''


@bot.event
async def on_member_remove(member):
    MongoDB.delete_group(member.guild.id, member)
    MongoDB.delete_group_tft(member.guild.id, member)


'''
This is a command that gets the bots automatically generated stats immediately, it can only be called upon by the two
owners of the bot
'''


@bot.command(name='getstats', case_insensitive=True)
async def get_stats(ctx):
    if ctx.author.id == 197858253089144832 or ctx.author.id == 360536914111102976:
        await bot.wait_until_ready()
        # members = (len(set(bot.get_all_members())))
        guildlist = bot.guilds
        servercount = 0
        membercount = 0
        largecount = 0
        for guild in guildlist:
            servercount += 1
            if not guild.unavailable:
                membercount += guild.member_count
                if guild.large:
                    largecount += 1
        embed = discord.Embed(title='__**ValorBot Stats**__',
                              description='Servers: ' + str(servercount) + '\n' +
                                          'Users: ' + str(membercount) + '\n' +
                                          'Large Servers: ' + str(largecount))
        await ctx.send(embed=embed)


'''
This forces the patch in case the patches do not work takes in the game as an input, can only be used by the bot devs
'''


@bot.command(name='ForcePatchBecauseRiotIsE')
async def forcepatch(ctx, game):
    if ctx.author.id == 360536914111102976 or ctx.author.id == 197858253089144832:
        if game == 'lol' or game == 'LOL' or game == 'League':
            MongoDB.insert_new_patch('xd', 'League of Legends')
            guild_list = MongoDB.collection.find({})
            if MongoDB.insert_new_patch(PatchNotes.currentpatchpic('League of Legends'), 'League of Legends'):
                for guilds in guild_list:
                    if guilds['patchdict']['League of Legends']:
                        my_channel = guilds["patchdict"]["League of Legends"]
                        await bot.wait_until_ready()
                        live_patch_channel = bot.get_channel(my_channel)
                        if live_patch_channel:
                            try:
                                imageurl = PatchNotes.currentpatchpic('League of Legends')
                            except:
                                imageurl = PatchNotes.currentpatchpicmetadata('League of Legends')
                            metadata = PatchNotes.metadata(PatchNotes.currentpatch('League of Legends'))
                            if '&#x27;' in metadata['description']:
                                metadata['description'] = metadata['description'].replace('&#x27;', "'")
                            embed2 = discord.Embed(title=metadata['title'], description=metadata['description'],
                                                   url=PatchNotes.currentpatch('League of Legends'))
                            embed2.set_image(url=imageurl)
                            embed2.set_thumbnail(url=metadata['thumbnail'])
                            try:
                                await live_patch_channel.send(embed=embed2)
                            except:
                                pass
                        else:
                            pass
        if game == 'Val' or game == 'val' or game == 'VAL' or game == 'Valorant':
            MongoDB.insert_new_patch('xd', 'Valorant')
            guild_list = MongoDB.collection.find({})
            if MongoDB.insert_new_patch(PatchNotes.findpatchesval(), 'Valorant'):
                for guilds in guild_list:
                    if guilds["patchdict"]["Valorant"]:
                        my_channel = guilds["patchdict"]["Valorant"]
                        await bot.wait_until_ready()
                        live_patch_channel = bot.get_channel(my_channel)
                        if live_patch_channel:
                            imageurl = PatchNotes.currentpatchpic('Valorant')
                            metadata = PatchNotes.metadata(PatchNotes.currentpatch('Valorant'))
                            if '&#x27;' in metadata['description']:
                                metadata['description'] = metadata['description'].replace('&#x27;', "'")
                            embed = discord.Embed(title=metadata['title'], description=metadata['description'],
                                                  url=PatchNotes.currentpatch('Valorant'))
                            embed.set_image(url=imageurl)
                            embed.set_thumbnail(url=metadata['thumbnail'])
                            try:
                                await live_patch_channel.send(embed=embed2)
                            except:
                                pass
                        else:
                            pass
        if game == 'TFT' or game == 'tft' or game == 'Teamfight Tactics':
            MongoDB.insert_new_patch('xd', 'Teamfight Tactics')
            guild_list = MongoDB.collection.find({})
            if MongoDB.insert_new_patch(PatchNotes.currentpatchpic('Teamfight Tactics'), 'Teamfight Tactics'):
                for guilds in guild_list:
                    if guilds["patchdict"]["Teamfight Tactics"]:
                        my_channel = guilds["patchdict"]["Teamfight Tactics"]
                        await bot.wait_until_ready()
                        try:
                            live_patch_channel = bot.get_channel(my_channel)
                            if live_patch_channel:
                                try:
                                    imageurl = PatchNotes.currentpatchpic("Teamfight Tactics")
                                except:
                                    imageurl = PatchNotes.currentpatchpicmetadata('Teamfight Tactics')
                                metadata = PatchNotes.metadata(PatchNotes.currentpatch('Teamfight Tactics'))
                                if '&#x27;' in metadata['description']:
                                    metadata['description'] = metadata['description'].replace('&#x27;', "'")
                                embed = discord.Embed(title=metadata['title'], description=metadata['description'],
                                                      url=PatchNotes.currentpatch('Teamfight Tactics'))
                                embed.set_image(url=imageurl)
                                embed.set_thumbnail(url=metadata['thumbnail'])
                                try:
                                    await live_patch_channel.send(embed=embed2)
                                except:
                                    pass
                            else:
                                pass
                        except:
                            pass
    else:
        pass


'''
When the server starts up this calculates the number of users, unique users, servers, and large servers
Param: None
Returns: None
'''


@bot.event
async def on_ready():
    members = (len(set(bot.get_all_members())))
    print("Riot bot serves " + str(members) + " unique users")
    guildlist = bot.guilds
    servercount = 0
    membercount = 0
    largecount = 0
    # emojiids = [715967443075334196, 715967488541851689, 715969440113491998, 715970985915973712]
    mongo_list = MongoDB.collection.find({})
    mongos = list()
    my_guilds = []
    for mongo in mongo_list:
        mongos.append(mongo["_id"])
    for guild in guildlist:
        servercount += 1
        if not guild.unavailable:
            local_member_count = guild.member_count
            membercount += local_member_count
            local_name = guild.name
            if guild.large:
                largecount += 1
        else:
            local_member_count = 0
            local_name = 'Placeholder'
        MongoDB.insert_post(guild.id, local_name, local_member_count)
        my_guilds.append(guild.id)
        '''
        if guild.id in emojiids:
            for emoji in guild.emojis:
                formatting = ''
                for data in emoji:
                    if data[0] == 'id':
                        formatting = str(data[1]) + '>'
                    if data[0] == 'name':
                        formatting = '<:' + data[1] + ':' + formatting
                        break
                Emojis.append(formatting)
    print(Emojis)
    '''
    for my_mongo in mongos:
        if my_mongo not in my_guilds:
            MongoDB.collection.delete_one({"_id": my_mongo})
    MongoDB.leaderboard_startup()
    MongoDB.leaderboard_startup_tft()
    MongoDB.collection6.delete_many({})
    print("Riot bot serves " + str(servercount) + " servers")
    print("Riot bot serves " + str(membercount) + " non-unique users")
    print("Riot bot serves " + str(largecount) + " large servers")


'''
This actively sets the bots status to ?help|?invite|?support
'''


async def active_processes():
    await bot.wait_until_ready()

    status = '?help|?invite|?support'

    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game(status))

        await asyncio.sleep(15)


'''
This will update the stats for our member count of each server in our database every 12 hours. 
'''
@tasks.loop(seconds=10800)
async def update_stats():
    guild_list = bot.guilds
    for guilds in guild_list:
        if not guilds.unavailable:
            MongoDB.collection.update_one({"_id": guilds.id}, {"$set": {"members": guilds.member_count}})


'''
This loops to check if there are any new live tweets in the database 
Param: None
Output: A message sent in the channel that the server admins decide upon setup
'''


@tasks.loop(seconds=5)
async def live_tweets():
    guild_list = MongoDB.collection.find({})
    val_tweets = MongoDB.collection1.find({"screen_name": "PlayVALORANT"})
    tweetsval = []
    for tweet in val_tweets:
        tweetsval.append(tweet["_id"])
        MongoDB.collection1.delete_one(tweet)
    for tweet in tweetsval:
        for guilds in guild_list:
            if guilds["tweetdict"]["Valorant"]:
                channel = guilds["tweetdict"]["Valorant"]
                await bot.wait_until_ready()
                live_tweet_channel = bot.get_channel(channel)
                if live_tweet_channel:
                    try:
                        await live_tweet_channel.send(tweet)
                    except:
                        pass
    lol_tweets = MongoDB.collection1.find({"screen_name": "LeagueOfLegends"})
    tweetslol = []
    for tweet in lol_tweets:
        tweetslol.append(tweet["_id"])
        MongoDB.collection1.delete_one(tweet)
    for tweet in tweetslol:
        for guilds in guild_list:
            if guilds["tweetdict"]["League of Legends"]:
                channel = guilds["tweetdict"]["League of Legends"]
                await bot.wait_until_ready()
                live_tweet_channel = bot.get_channel(channel)
                if live_tweet_channel:
                    try:
                        await live_tweet_channel.send(tweet)
                    except:
                        pass
    tft_tweets = MongoDB.collection1.find({"screen_name": "TFT"})
    tweetstft = []
    for tweet in tft_tweets:
        tweetstft.append(tweet["_id"])
        MongoDB.collection1.delete_one(tweet)
    for tweet in tweetstft:
        for guilds in guild_list:
            if guilds["tweetdict"]["Teamfight Tactics"]:
                channel = guilds["tweetdict"]["Teamfight Tactics"]
                await bot.wait_until_ready()
                live_tweet_channel = bot.get_channel(channel)
                if live_tweet_channel:
                    try:
                        await live_tweet_channel.send(tweet)
                    except:
                        pass
    lor_tweets = MongoDB.collection1.find({"screen_name": "PlayRuneterra"})
    tweetslor =[]
    for tweet in lor_tweets:
        tweetslor.append(tweet["_id"])
        MongoDB.collection1.delete_one(tweet)
    for tweet in tweetslor:
        for guilds in guild_list:
            if guilds["tweetdict"]["Legends of Runeterra"]:
                channel = guilds["tweetdict"]["Legends of Runeterra"]
                await bot.wait_until_ready()
                live_tweet_channel = bot.get_channel(channel)
                if live_tweet_channel:
                    try:
                        await live_tweet_channel.send(tweet)
                    except:
                        pass
    slob_tweets = MongoDB.collection1.find({"screen_name": "CoSlobby"})
    tweetsslob = []
    for tweet in slob_tweets:
        tweetsslob.append(tweet["_id"])
        MongoDB.collection1.delete_one(tweet)
    for tweet in tweetsslob:
        for guilds in guild_list:
            if guilds["tweetdict"]["Valorant"]:
                channel = guilds["tweetdict"]["Valorant"]
                await bot.wait_until_ready()
                live_tweet_channel = bot.get_channel(712422403669753870)
                if live_tweet_channel:
                    try:
                        await live_tweet_channel.send(tweet)
                    except:
                        pass
    riot_tweets = MongoDB.collection1.find({"screen_name": "riotgames"})
    tweetsriot = []
    for tweet in riot_tweets:
        tweetsriot.append(tweet["_id"])
        MongoDB.collection1.delete_one(tweet)
    for tweet in tweetsriot:
        for guilds in guild_list:
            if guilds["tweetdict"]["Riot Games"]:
                channel = guilds["tweetdict"]["Riot Games"]
                await bot.wait_until_ready()
                live_tweet_channel = bot.get_channel(channel)
                if live_tweet_channel:
                    try:
                        await live_tweet_channel.send(tweet)
                    except:
                        pass


''''
This loops to check if there are any new live patches for val in the database 
Param: None
Return: A message sent in the channel that the server admins decide upon setup
'''


@tasks.loop(seconds=300)
async def live_patches_val():
    await bot.wait_until_ready()
    guild_list = MongoDB.collection.find({})
    print("val working")
    if MongoDB.insert_new_patch(PatchNotes.currentpatch('Valorant'), 'Valorant'):
        print("val here")
        for guilds in guild_list:
            if guilds["patchdict"]["Valorant"]:
                my_channel = guilds["patchdict"]["Valorant"]
                await bot.wait_until_ready()
                live_patch_channel = bot.get_channel(my_channel)
                if live_patch_channel:
                    imageurl = PatchNotes.currentpatchpic('Valorant')
                    metadata = PatchNotes.metadata(PatchNotes.currentpatch('Valorant'))
                    if '&#x27;' in metadata['description']:
                        metadata['description'] = metadata['description'].replace('&#x27;', "'")
                    embed = discord.Embed(title=metadata['title'], description=metadata['description'],
                                          url=PatchNotes.currentpatch('Valorant'))
                    embed.set_image(url=imageurl)
                    embed.set_thumbnail(url=metadata['thumbnail'])
                    try:
                        await live_patch_channel.send(embed=embed)
                    except:
                        pass
                else:
                    pass


''''
This loops to check if there are any new live patches for tft in the database 
Param: None
Return: A message sent in the channel that the server admins decide upon setup
'''


@tasks.loop(seconds=300)
async def live_patches_tft():
    await bot.wait_until_ready()
    guild_list = MongoDB.collection.find({})
    print("tft working")
    patchlink = PatchNotes.currentpatch('Teamfight Tactics')
    try:
        patchpic = PatchNotes.currentpatchpic('Teamfight Tactics')
    except AttributeError:
        try:
            patchpic = PatchNotes.currentpatchpicmetadata('Teamfight Tactics')
        except AttributeError:
            return
    if MongoDB.insert_new_patch(patchlink, 'Teamfight Tactics'):
        print("tft here")
        for guilds in guild_list:
            if guilds["patchdict"]["Teamfight Tactics"]:
                my_channel = guilds["patchdict"]["Teamfight Tactics"]
                await bot.wait_until_ready()
                try:
                    live_patch_channel = bot.get_channel(my_channel)
                    if live_patch_channel:
                        metadata = PatchNotes.metadata(PatchNotes.currentpatch('Teamfight Tactics'))
                        if '&#x27;' in metadata['description']:
                            metadata['description'] = metadata['description'].replace('&#x27;', "'")
                        embed = discord.Embed(title=metadata['title'], description=metadata['description'],
                                              url=PatchNotes.currentpatch('Teamfight Tactics'))
                        embed.set_image(url=patchpic)
                        embed.set_thumbnail(url=metadata['thumbnail'])
                        try:
                            await live_patch_channel.send(embed=embed)
                        except:
                            pass
                    else:
                        pass
                except:
                    pass

''''
This loops to check if there are any new live patches for lol in the database 
Param: None
Return: A message sent in the channel that the server admins decide upon setup
'''


@tasks.loop(seconds=300)
async def live_patches_lol():
    await bot.wait_until_ready()
    guild_list = MongoDB.collection.find({})
    print("lol working")
    patchlink = PatchNotes.currentpatch('League of Legends')
    try:
        patchpic = PatchNotes.currentpatchpic('League of Legends')
    except AttributeError:
        try:
            patchpic = PatchNotes.currentpatchpicmetadata('League of Legends')
        except AttributeError:
            return
    if MongoDB.insert_new_patch(patchlink, 'League of Legends'):
        print("lol here")
        for guilds in guild_list:
            if guilds['patchdict']['League of Legends']:
                my_channel = guilds["patchdict"]["League of Legends"]
                await bot.wait_until_ready()
                live_patch_channel = bot.get_channel(my_channel)
                if live_patch_channel:
                    metadata = PatchNotes.metadata(PatchNotes.currentpatch('League of Legends'))
                    if '&#x27;' in metadata['description']:
                        metadata['description'] = metadata['description'].replace('&#x27;', "'")
                    embed2 = discord.Embed(title=metadata['title'], description=metadata['description'],
                                           url=PatchNotes.currentpatch('League of Legends'))
                    embed2.set_image(url=patchpic)
                    embed2.set_thumbnail(url=metadata['thumbnail'])
                    try:
                        await live_patch_channel.send(embed=embed2)
                    except:
                        pass
                else:
                    pass


'''
This loops to give updated bot-stats in our server
'''


@tasks.loop(hours=12)
async def bot_stats():
    await bot.wait_until_ready()
    guildlist = bot.guilds
    servercount = 0
    membercount = 0
    largecount = 0
    for guild in guildlist:
        servercount += 1
        if not guild.unavailable:
            membercount += guild.member_count
            if guild.large:
                largecount += 1
    embed = discord.Embed(title='__**ValorBot Stats**__',
                          description='Servers: ' + str(servercount) + '\n' +
                          'Users: ' + str(membercount) + '\n' +
                          'Large Servers: ' + str(largecount))
    channel = bot.get_channel(722543402524082242)
    await channel.send(embed=embed, delete_after=43200)


'''
This starts up all of the loops for our patches, tweets, bot-stats, and server-stats. 
'''

live_tweets.start()
live_patches_val.start()
live_patches_tft.start()
live_patches_lol.start()
bot_stats.start()
update_stats.start()

'''
This pulls our cogs file and sets up each class so that the bot can load them before it runs.
'''

extensions = ['Cogs.RankCommands', 'Cogs.TwitterCommands', 'Cogs.ClashInfo',
              'Cogs.PatchCommands', 'Cogs.Leaderboards', 'Cogs.LiveGame', 'Cogs.ChampionRotation', 'Cogs.Help',
              'Cogs.Region', 'Cogs.Invite', 'Cogs.TFTLeaderboards', 'Cogs.Timezone', 'Cogs.TopGG', 'Cogs.HelpFR']

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)
    bot.loop.create_task(active_processes())
    # Credentials.TOKEN is a bot token given by discord
    bot.run(Credentials.TOKEN)
