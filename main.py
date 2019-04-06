import discord
from discord.ext import commands
import random
import requests
import pyrebase
from functions import *
from config import *
import aiohttp


client = commands.Bot(command_prefix = '!')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(status = discord.Status.online, activity = discord.Game(name = "https://github.com/AdautoP/bloodhound-bot"))
    
@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    guild = client.get_guild(payload.guild_id)
    author = guild.get_member(payload.user_id)
    if guild.region == discord.VoiceRegion.brazil:
        if reactionChannelNameBrazil in channel.name:
            for i in guild.roles:
                if i.name == payload.emoji.name:
                    await author.add_roles(i, reason = "Clicou na reaction de {}.".format(i.name))
    else:
        if reactionChannelNameEverywhere in channel.name:
            for i in guild.roles:
                if i.name == payload.emoji.name:
                    await author.add_roles(i)

@client.event
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(payload.channel_id)
    guild = client.get_guild(payload.guild_id)
    author = guild.get_member(payload.user_id)
    if guild.region == discord.VoiceRegion.brazil:
        if reactionChannelNameBrazil in channel.name:
            for i in guild.roles:
                if i.name == payload.emoji.name:
                    await author.remove_roles(i, reason = "Clicou na reaction de {}.".format(i.name))
    else:
        if reactionChannelNameEverywhere in channel.name:
            for i in guild.roles:
                if i.name == payload.emoji.name:
                    await author.remove_roles(i)

@client.event
async def on_guild_join():
    data = {'server_count': len(client.guilds)}
    api_url = 'https://discordbots.org/api/bots/' + str(client.user.id) + '/stats'
    async with aiohttp.ClientSession() as session:
        await session.post(api_url, data=data, headers=dblHeaders)

@client.event
async def on_guild_remove():
    data = {'server_count': len(client.guilds)}
    api_url = 'https://discordbots.org/api/bots/' + str(client.user.id) + '/stats'
    async with aiohttp.ClientSession() as session:
        await session.post(api_url, data=data, headers=dblHeaders)


   

@client.command(pass_context = True)
async def register(ctx, platform, nickname):
    if channelName in ctx.message.channel.name:
        if ctx.message.guild.region == discord.VoiceRegion.brazil:
            await ctx.channel.send("{0.mention}, Registrando seu nickname e plataforma no banco de dados para uso futuro.".format(ctx.message.author))
        else:
            await ctx.channel.send("{0.mention}, Registering your nickname and platform on the database for future use.".format(ctx.message.author))
        await pushNewNickname(ctx.message.author.id,nickname,platform)
        if ctx.message.guild.region == discord.VoiceRegion.brazil:
            await ctx.channel.send("{0.mention}, Registrado! Agora pode usar o comando **!lvl** e o comando **!kills** sem especificar plataforma e nickname.".format(ctx.message.author))
        else:
            await ctx.channel.send("{0.mention}, Registered! Now you can use the **!lvl** and **!kills** commands without specifying platform and nickname.".format(ctx.message.author))
    else:
        await ctx.message.delete()


@client.command(pass_context = True)
async def lvl(ctx, platform = None,nickname = None):
    if channelName in ctx.message.channel.name:
        if ctx.message.guild.region == discord.VoiceRegion.brazil:
            await ctx.channel.send("{0.mention}, Pesquisando seu level".format(ctx.message.author))
        else:
            await ctx.channel.send("{0.mention}, Searching your level".format(ctx.message.author))
        if nickname is not None and platform is not None:
            await levelAutoRole(ctx,nickname,platform)
        else:
            user = await getUser(ctx.message.author.id)
            print(user)
            if user is not None:
                await levelAutoRole(ctx,user["origin_nickname"],user["platform"])
            else:
                if ctx.message.guild.region == discord.VoiceRegion.brazil:
                    await ctx.channel.send("{0.mention}, Usuário não registrado.".format(ctx.message.author))
                    embed = discord.Embed(
                        title = "**Escreva esse comando para registrar seu nickname e plataforma:**",
                        description = "**!register PLATAFORMA NICKNAME**, Exemplo: !register pc NRG_dizzy",
                        colour = discord.Colour.red()
                    )
                    await ctx.channel.send(embed = embed)
                else:
                    await ctx.channel.send("{0.mention}, User not registered".format(ctx.message.author))
                    embed = discord.Embed(
                        title = "**Write this command to register your nickname and platform:**",
                        description = "**!register PLATFORM NICKNAME**, Example: !register pc NRG_dizzy",
                        colour = discord.Colour.red()
                    )
                    await ctx.channel.send(embed = embed)

    else:
        await ctx.message.delete()

@client.command(pass_context = True)
async def kills(ctx, platform = "pc", nickname = None):
    if channelName in ctx.message.channel.name:
        if ctx.message.guild.region == discord.VoiceRegion.brazil:
            await ctx.channel.send("{0.mention}, Pesquisando suas kills.".format(ctx.message.author))
        else:
            await ctx.channel.send("{0.mention}, Searching your kills.".format(ctx.message.author))
        if nickname is not None:
            await killsAutoRole(ctx,nickname,platform)    
        else:
            user = await getUser(ctx.message.author.id)
            print(user)
            if user is not None:
                await killsAutoRole(ctx,user["origin_nickname"],user["platform"])
            else:
                if ctx.message.guild.region == discord.VoiceRegion.brazil:
                    await ctx.channel.send("{0.mention}, Usuário não registrado.".format(ctx.message.author))
                    embed = discord.Embed(
                        title = "**Escreva esse comando para registrar seu nickname e plataforma:**",
                        description = "**!register PLATAFORMA NICKNAME**, Exemplo: !register pc NRG_dizzy",
                        colour = discord.Colour.red()
                    )
                    await ctx.channel.send(embed = embed)
                else:
                    await ctx.channel.send("{0.mention}, User not registered".format(ctx.message.author))
                    embed = discord.Embed(
                        title = "**Write this command to register your nickname and platform:**",
                        description = "**!register PLATFORM NICKNAME**, Example: !register pc NRG_dizzy",
                        colour = discord.Colour.red()
                    )
                    await ctx.channel.send(embed = embed)
    else:
        await ctx.message.delete()



@client.command(pass_context = True)
async def check_level(ctx, platform = None, nickname = None):
    if channelName in ctx.message.channel.name:
        if nickname is not None and platform is not None:
            platformID = getPlatformId(platform)
            if ctx.message.guild.region == discord.VoiceRegion.brazil:
                await ctx.channel.send("{0.mention}, Pesquisando o level de **{1}**.".format(ctx.message.author,nickname))
            else:
                await ctx.channel.send("{0.mention}, Searching for **{1}'s** level.".format(ctx.message.author,nickname))
        
            headers = {
            "TRN-Api-Key": random.choice(trnApiKey)
            }

            request = requests.get("{}{}/{}".format(getLevel,platformID,nickname),headers=headers)
            json = request.json()
            if "data" in json:
                level = int(json["data"]["stats"][0]["value"])
                if ctx.message.guild.region == discord.VoiceRegion.brazil:
                    await ctx.channel.send("{0.mention}, O level de **{1}** é **{2}**.".format(ctx.message.author,nickname,level))
                else:
                    await ctx.channel.send("{0.mention}, **{1}** is level **{2}**.".format(ctx.message.author,nickname,level))
            elif "errors" in json:
                await ctx.channel.send("{0.mention}, ".format(ctx.message.author)+json["errors"][0]["message"])
            else:
                await ctx.channel.send("{0.mention}, ".format(ctx.message.author)+json["error"])    
        else:
            if ctx.message.guild.region == discord.VoiceRegion.brazil:
                await ctx.channel.send("{0.mention}, Você esqueceu de passar os parâmetros corretos.".format(ctx.message.author))
            else:
                await ctx.channel.send("{0.mention}, You forgot to pass the right parameters.".format(ctx.message.author))

    else:
        await ctx.message.delete()

@client.command(pass_context = True)
async def check_kills(ctx, platform = None, nickname = None):
    if channelName in ctx.message.channel.name:
        if nickname is not None and platform is not None:
            platformID = getPlatformId(platform)
            if ctx.message.guild.region == discord.VoiceRegion.brazil:
                await ctx.channel.send("{0.mention}, Pesquisando as kills de **{1}**.".format(ctx.message.author,nickname))
            else:
                await ctx.channel.send("{0.mention}, Searching for **{1}'s** kills.".format(ctx.message.author,nickname))
            headers = {
            "TRN-Api-Key": random.choice(trnApiKey)
            }

            request = requests.get("{}{}/{}".format(getLevel,platformID,nickname),headers=headers)
            json = request.json()
            if "data" in json:
                kills = int(json["data"]["stats"][1]["value"])
                if ctx.message.guild.region == discord.VoiceRegion.brazil:
                    await ctx.channel.send("{0.mention}, **{1}** tem **{2}** kills.".format(ctx.message.author,nickname,kills))
                else:
                    await ctx.channel.send("{0.mention}, **{1}** has **{2}** kills.".format(ctx.message.author,nickname,kills))
            elif "errors" in json:
                await ctx.channel.send("{0.mention}, ".format(ctx.message.author)+json["errors"][0]["message"])
            else:
                await ctx.channel.send("{0.mention}, ".format(ctx.message.author)+json["error"])
        else:
            if ctx.message.guild.region == discord.VoiceRegion.brazil:
                await ctx.channel.send("{0.mention}, Você esqueceu de passar os parâmetros corretos.".format(ctx.message.author))
            else:
                await ctx.channel.send("{0.mention}, You forgot to pass the right parameters.".format(ctx.message.author))
    else:
        await ctx.message.delete()
        

@client.command(pass_context = True)
async def list_commands(ctx):
    if ctx.message.guild.region == discord.VoiceRegion.brazil:
        embed = discord.Embed(
            title = "Ajuda",
            description = "Plataformas suportadas: pc, xbox, ps4",
            colour = discord.Colour.red()
        )
        embed.add_field(name = "!register", value = "Salva seu discord_id, origin_nickname e platforma no banco de dados.",inline = False)
        embed.add_field(name = "Exemplo:", value = "!register pc NRG_dizzy",inline = False)
        embed.add_field(name = "!lvl", value = "Pesquisa pelo seu nick da Origin e te dá o cargo referente ao seu level atual no Apex. Se você já tiver registrado seu nickname e plataforma, pode usar apenas !lvl.",inline = False)
        embed.add_field(name = "Exemplo:", value = "!lvl pc NRG_dizzy **OU APENAS** !lvl",inline = False)
        embed.add_field(name = "!kills", value = "Pesquisa pelo seu nick da Origin e te dá o cargo referente ao seu K/L atual no Apex. Se você já tiver registrado seu nickname e plataforma, pode usar apenas !kills.",inline = False)
        embed.add_field(name = "Exemplo:", value = "!kills pc NRG_dizzy **OU APENAS** !kills",inline = False)
        embed.add_field(name = "!check_level", value = "Pesquisa pelo nick da Origin e diz o level atual no Apex.",inline = False)
        embed.add_field(name = "Exemplo:", value = "!check_level pc NRG_dizzy",inline = False)
        embed.add_field(name = "!check_kills", value = "Pesquisa pelo nick da Origin e diz o número de kills no Apex.",inline = False)
        embed.add_field(name = "Exemplo:", value = "!check_kills pc NRG_dizzy",inline = False)
        embed.set_footer(text = "Bot feito por Adauto Pinheiro, github: https://github.com/AdautoP")
    else:
        embed = discord.Embed(
            title = "Help",
            description = "Supported platforms: pc, xbox, ps4",
            colour = discord.Colour.red()
        )
        embed.add_field(name = "!register", value = "Saves your discord_id, origin_nickname and platform on the database.",inline = False)
        embed.add_field(name = "Example:", value = "!register pc NRG_dizzy",inline = False)
        embed.add_field(name = "!lvl", value = "Searchs for your Origin nickname and gives you the role related to your Apex level. If you have registered your nickname and platform previously, you can use just !lvl.",inline = False)
        embed.add_field(name = "Example:", value = "!lvl pc NRG_dizzy **OR JUST** !lvl",inline = False)
        embed.add_field(name = "!kills", value = "Searchs for your Origin nickname and gives you the role related to your K/L in Apex. If you have registered your nickname and platform previously, you can use just !kills.",inline = False)
        embed.add_field(name = "Example:", value = "!kills pc NRG_dizzy **OR JUST** !kills",inline = False)
        embed.add_field(name = "!check_level", value = "Searchs for on Origin nickname and tells the actual level.",inline = False)
        embed.add_field(name = "Example:", value = "!check_level pc NRG_dizzy",inline = False)
        embed.add_field(name = "!check_kills", value = "Searchs for on Origin nickname and tells the amount of kills.",inline = False)
        embed.add_field(name = "Example:", value = "!check_kills pc NRG_dizzy",inline = False)
        embed.set_footer(text = "Bot made By Adauto Pinheiro, github: https://github.com/AdautoP")

    await ctx.channel.send(embed = embed)

client.run(TOKEN)
