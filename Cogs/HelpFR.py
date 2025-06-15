from discord.ext import commands
import discord


class HelpFR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="helpfr",
                      brief="Displays all the commands for the server and a description on what they do",
                      case_insensitive=True)
    async def helpfr(self, ctx):
        embed = discord.Embed(title='__**Valor Bot Commands**__',
                              description='Voici les différents nom **acceptés par le bot pour chaque jeux**: '
                              + '\n' + "**League of Legends:** LoL, League, League of Legends, ou lol" + '\n' +
                              "**Valorant:** val, Valorant, ou valorant" + '\n' +
                              "**Teamfight Tactics:** TFT, Teamfight Tactics, Team fight Tactics, tft, team fight "
                              "tactics, ou teamfight tactics" + '\n' +
                              "**Legends of Runeterra:** lor, LoR, Legends of Runeterra, ou legends of runeterra")
        embed.add_field(name='__**Commandes Tweeter**__',
                        value='**?tweets** - Cela vous permettra de voir quels jeux le bot à activer le partage des '
                              'tweets sur votre serveur',
                        inline=False)
        embed.add_field(name='__**Patch Notes Commands**__ *Does not support Legends of Runeterra*',
                        value='**?currentpatch game** - Cette commande affichera le patch actif sur le jeu choisit ' +
                              '\n' +
                              '**?patch** - Cela vous permets de savoir quels jeux à le partage en direct des patchs '
                              'actifs sur ce serveur.',
                        inline=False)
        embed.add_field(name='__**Commandes League of Legends**__',
                        value="**?ranklol summoner-name** -  Vous donne votre rang d’invocateur en classé solo, "
                              "flex et si vous êtes en partie multijoueur actuellement ! Utilisez ?ranktft pour le "
                              "TFT" + '\n' +
                              "**?rankregion region summoner-name** Vous permets d’obtenir le rang d’un invocateur "
                              "d’une région différente que celle du serveur" + '\n' +
                              '**?livegame summoner-name** - Vous donnes les informations de la partie en cours d’un '
                              'invocateur, si il est en partie.' + '\n' +
                              "**?livegameregion region summoner-name** - Vous donnes les informations en direct de la "
                              "partie d’un invocateur d’autres régions" + "\n" +
                              '**?clash** - Cela vous donnera les dates des Clashs à venir' + '\n' +
                              '**?freechamps** - Cette commande vous donnera la rotation des champions pour touts '
                              ' invocateurs (hors PBE)' + '\n' +
                              '**?myregion** - Regarde la région de votre serveur',
                        inline=False)
        embed.add_field(name='__**Leaderboards**__ *Ne fonctionne qu’avec League of Legends et TFT*',
                        value='**?helpleaderboardfr** - Vous donne l’ensemble des commandes en rapport avec la fonction'
                              ' leaderboard de Valor Bot!',
                        inline=False)
        embed.add_field(name='__**Invite and Support**__',
                        value='**?invite** - Utilisez cette commande pour obtenir le lien d’invitation de ValorBot sur '
                              'votre serveur' + '\n' +
                              '**?support** - Utilisez pour obtenir le lien d’invitation au serveur discord de support '
                              'du ValorBot afin de posez vos questions, de donner des suggestions, de rapporter des '
                              'bugs ou pour parler au développeur',
                        inline=False)
        embed.set_footer(text='Si vous avez des questions concernant Valor Bot, le meilleur endroit pour contacter les '
                              'développeurs est notre Serveur de support Discord https://discord.gg/sqNChCw')
        await ctx.send(embed=embed)

    @commands.command(name='helpsetupfr',
                      brief='Displays all the commands for server setup',
                      case_insensitive=True)
    async def helpsetupfr(self, ctx):
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
        embed.add_field(name='__**Commandes de Setup du serveur**__ - C’est commande son réservé aux admins',
                        value='**?setregion region** - C’est commandes définissent la région par défaut du serveur. '
                              'Options disponibles: '
                              'na, euw, eune, oce, kr, jp, br, las, lan, ru, and tr (capatalization does not matter)'
                              + '\n' +
                              '**?sendtweets game** - Utilisez cette commande pour choisir le channel écrit dans lequel'
                              ' vous souhaitez recevoir les tweets, vous ne recevrez pas les tweets avant que vous ayez'
                              ' mis en route cette commande. Si vous souhaitez changez le channel choisit, retapez'
                              ' directement la commande avec le channel voulu.' + '\n' +
                              '**?sendpatch game** - Utilisez cette commande pour choisir le channel écrit dans lequel '
                              'vous souhaitez recevoir les patchs, vous ne recevrez pas les patchs avant que vous ayez'
                              ' mis en route cette commande. Si vous souhaitez changez le channel choisit, retapez'
                              ' directement la commande' +
                              '\n' +
                              '**?stoptweets game** - Commande pour désactiver l’envoi des tweets'
                              + '\n' +
                              '**?stoppatch game** - Commande pour désactiver l’envoi des patchs',
                        inline=False)
        embed.set_footer(text='Si vous avez des questions concernant Valor Bot, le meilleur endroit pour contacter les'
                              ' développeurs est notre Serveur de support Discord: https://discord.gg/sqNChCw')
        await ctx.send(embed=embed)

    @commands.command(name='helpleaderboardfr',
                      brief='Displays all the commands for leaderboards, only currently applies to League of '
                            'Legends/TFT',
                      case_insensitive=True)
    async def helpleaderboardfr(self, ctx):
        embed = discord.Embed(title='__**Commandes Du Leaderboard Valor Bot**__',
                              description='Il s’agit du leaderboards local, c’est une feature vous permetant de créer '
                                          'un groupe avec vos amis afin de voir vos rangs et de voir qui est le plus '
                                          'fort. Ajouter tft à la fin de chaque commande pour un leaderboard TFT!')
        embed.add_field(name='__**Leaderboards**__ *N’est supporter que pour League of Legends/TFT, utilisez ?makegroup'
                             ' en premier!*',
                        value='**?makegroup group-name** - Créer un groupe leaderboard. Peut importe le nom que vous '
                              'choisissez, il s’agira du nom référencer sur le leaderboard. Soyez sûr de vous en'
                              ' souvenir.' + '\n' +
                              "**?makegroupregion region group-name** - Créer un groupe d’une région différente que "
                              "celle du serveur" + "\n" +
                              '**?addplayer summoner-name** - Ajoute un invocateur à votre groupe, seul le leader du '
                              'groupe peut faire cela' + '\n' +
                              '**?leaderboard group-name** - Tapez le nom du groupe dont vous voulez voir les stats, '
                              'tout le monde peut le faire et n’a pas besoin d’en être membre!',
                        inline=False)
        embed.add_field(name='__**Leaderboard Administrative Commands**__ *Soyez sûr d’être le créateur du groupe '
                             'avant d’entrer ces commandes*',
                        value='**?mygroup** - Vous donne le nom du groupe que vous possédez (Si vous avez un).' + '\n' +
                              '**?deleteplayer summoner name** - Exclu un invocateur de votre groupe, seul le leader du'
                              ' groupe peut faire cela' + '\n' +
                              '**?renamegroup new-group-name** - Tapez le nouveau nom de groupe que vous souhaitez '
                              'avoir' + '\n' +
                              '**?deletegroup** - Cela supprime le groupe que vous avez créer',
                        inline=False)
        embed.set_footer(text='Si vous avez des questions concernant Valor Bot, le meilleur endroit pour contacter les'
                              ' développeurs est notre Serveur de support Discord: https://discord.gg/sqNChCw')
        await ctx.send(embed=embed)

    @commands.command(name='helptzfr',
                      brief='Displays all valid timezones for upcoming clash dates',
                      case_insensitive=True)
    async def helptzfr(self, ctx):
        embed = discord.Embed(title='__**Aide Timezone Valor Bot**__',
                              description="Timezones Valides(actuellement): **edt** (New York, USA), **cdt** (Chicago, "
                                          "USA), **mdt** (Edmonton, Alberta), " 
                                          "**pdt** (Los Angeles, USA), **gmt** (greenwich mean time), **bst** (London, "
                                          "UK), **cest** (Brussels, Belgium), " 
                                          "**eest** (Bucharest, Romania), **msk** (Moscow, Russia)",)
        embed.add_field(name='__**Timezone Commands**__',
                        value='**?settz/settimezone** - Règle le serveur sur une des timezones ci-dessus '
                              '(Exclusif aux admins)' + '\n' +
                        '**?mytz/mytimezone** - Vous donne la timezone à laquelle le serveur est relié'
                        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpFR(bot))
