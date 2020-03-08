import discord
from discord.ext import commands
import random
import requests
import pyrebase
from config import *


firebase = pyrebase.initialize_app(config)
db = firebase.database()

async def getUser(discord_id):
    try:
        db = firebase.database()
        user = db.child("User").child("{}".format(discord_id)).get().val()
        return user
    except:
        print("User does not exists")
        #

async def pushNewNickname(discord_id,origin_nickname,platform):
    try:
        db = firebase.database()
        data = {
            "discord_id": discord_id,
            "origin_nickname": origin_nickname,
            "platform": platform
        }
        db.child("User").child("{}".format(discord_id)).set(data)
    except:
        print("Couldn't set data.")
        #

def getLevelRoleToAdd(level,server):
    lastRoleValue = (0,None)
    for i in server.roles:
        if "+" in i.name and "K/L" not in i.name:
            number = i.name.split("+")[0]
            woSpace = number.split(" ")[0]
            if woSpace.isdigit():
                if level >= int(woSpace):
                    if int(woSpace) >= lastRoleValue[0]:
                        lastRoleValue = (int(woSpace),i)
    return lastRoleValue[1]


def getKillsRoleToAdd(killsPerLevel, server):
    lastKillRoleValue = (0, None)
    for i in server.roles:
        if "+ K/L" in i.name:
            number = i.name.split("+ K/L")[0]
            woSpace = number.split(" ")[0]
            if woSpace.isdigit():
                if killsPerLevel >= int(woSpace):
                    if int(woSpace) >= lastKillRoleValue[0]:
                        lastKillRoleValue = (int(woSpace),i)
    return lastKillRoleValue[1]

def getRankRoleToAdd(rankScore, server):
    lastRankRoleValue = (0, "None", "None")
    roleToReturn = None
    for i in ranks:
        if rankScore >= i[0]:
            if i[0] >= lastRankRoleValue[0]:
                lastRankRoleValue = i
    if rankScore == -1:
        lastRankRoleValue = (-1, "Predator", "Predador")
    for j in server.roles:
        if j.name == lastRankRoleValue[1] or j.name == lastRankRoleValue[2]:
            roleToReturn = j
    print("found role to return : {}".format(roleToReturn))
    return roleToReturn
    

def getLevelRolesToRemove(roles):
    rolesToRemove = []
    for i in roles:
        if "+" in i.name and "K/L" not in i.name:
            number = i.name.split("+")[0]
            woSpace = number.split(" ")[0]
            if woSpace.isdigit():
                rolesToRemove.append(i)
    return rolesToRemove

def getKillRolesToRemove(roles):
    rolesToRemove = []
    for i in roles:
        if "K/L" in i.name:
            number = i.name.split("+ K/L")[0]
            woSpace = number.split(" ")[0]
            if woSpace.isdigit():
                rolesToRemove.append(i)
    return rolesToRemove

def getRankRolesToRemove(roles):
    rolesToRemove = []
    for i in roles:
        for j in ranks:
            if i.name == j[1] or i.name == j[2]:
                rolesToRemove.append(i)
    return rolesToRemove

def checkRankScore(stats):
    aux = False
    for i in stats:
        if "Rank Score" in i["metadata"]["name"]:
            rankScore = int(i["value"])
            if rankScore > 10000 and checkSeasonRank(stats) <=500:
                rankScore = -1
            aux = True
    if aux == False :
        rankScore = 0
    return rankScore

def checkSeasonRank(stats):
    biggestSeasonValue = 0
    for i in stats:
        metadataName = i["metadata"]["name"]
        if "Season" in metadataName and "Wins" in metadataName:
            value = int(metadataName.split("Season")[1].split("Wins")[0])
            if value > biggestSeasonValue:
                biggestSeasonValue = value
                stat = i
    return i["rank"]



def getPlatformId(platform):
    if(platform == "pc" or platform == "PC"):
        return 5
    elif (platform == "xbox" or platform == "XBOX" or platform == "Xbox"):
        return 1
    elif (platform == "ps4" or platform == "PS4"):
        return 2

async def levelAutoRole(ctx,origin_nickname, platform):
    platformID = getPlatformId(platform)
    headers = {
    "TRN-Api-Key": random.choice(trnApiKey)
    }

    request = requests.get("{}{}/{}".format(getLevel,platformID,origin_nickname),headers=headers)
    json = request.json()
    if "data" in json:
        level = int(json["data"]["stats"][0]["value"])
        memberRoles = ctx.message.author.roles #GETTING ALL THE ROLES THE MEMBER HAS
        rolesToRemove = getLevelRolesToRemove(memberRoles) #GETTING THE LEVEL RELATED ROLES THE MEMBER ALREADY HAVE TO REMOVE BEFORE GIVING NEW ONE
        await ctx.message.author.remove_roles(*rolesToRemove) #REMOVING THE ROLE
        try:
            role = getLevelRoleToAdd(level,ctx.message.guild) #GETTING THE NEW ROLE BASED ON THE LEVEL THE MEMBER HAS NOW
            if ctx.message.guild.region == discord.VoiceRegion.brazil:
                embed = discord.Embed(
                    title = "**{0.name}**".format(ctx.message.author),
                    description = "Seu level é **{0}**, foi lhe dado o cargo {1.mention}.".format(level,role),
                    colour = discord.Colour.red()
                )
                await ctx.channel.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = "**{0.name}**".format(ctx.message.author),
                    description = "Your level is **{0}**, it has been given you the {1.mention} role.".format(level,role),
                    colour = discord.Colour.red()
                )
                await ctx.channel.send(embed = embed)
            await ctx.message.author.add_roles(role) #ADDING THE NEW ROLE TO THE MEMBER
        except:
            if ctx.message.guild.region == discord.VoiceRegion.brazil:
                embed = discord.Embed(
                    title = "**{0.name}**".format(ctx.message.author),
                    description = "Seu level é **{0}**.".format(level),
                    colour = discord.Colour.red()
                )
                await ctx.channel.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = "**{0.name}**".format(ctx.message.author),
                    description = "Your level is **{0}**.".format(level),
                    colour = discord.Colour.red()
                )
                await ctx.channel.send(embed = embed)
        try:
            if ("★" in ctx.message.author.nick):
                nickAux = ctx.message.author.nick.split("★")
                woSpace = nickAux[0].split(" ")
                if woSpace[0].isdigit():
                    woSpace = nickAux[1].split(" ")
                    await ctx.message.author.edit(nick = "{} {} {}".format(level,"★",woSpace[1]))
                else:
                    await ctx.message.author.edit(nick = "{} {} {}".format(level ,"★",woSpace[0] ))
            else:
                await ctx.message.author.edit(nick = "{} {} {}".format(level,"★",ctx.message.author.nick))    
        except:
            await ctx.message.author.edit(nick = "{} {} {}".format(level,"★",ctx.message.author.name))
    elif "errors" in json:
        if ctx.message.guild.region == discord.VoiceRegion.brazil:
            await ctx.channel.send("Usuário não encontrado. Cheque se a plataforma e o nickname foram inseridos corretos.")
        else:
            await ctx.channel.send("User not found. Check if the platform and nickname were correctly inserted.")
    else:
        await ctx.channel.send(json["error"])



async def killsAutoRole(ctx,origin_nickname, platform):
    platformID = getPlatformId(platform)
    headers = {
    "TRN-Api-Key": random.choice(trnApiKey)
    }

    request = requests.get("{}{}/{}".format(getLevel,platformID,origin_nickname),headers=headers)
    json = request.json()
    
    if "data" in json:
        memberRoles = ctx.message.author.roles #GETTING ALL THE ROLES THE MEMBER HAS
        rolesToRemove = getKillRolesToRemove(memberRoles) #GETTING THE LEVEL RELATED ROLES THE MEMBER ALREADY HAVE TO REMOVE BEFORE GIVING NEW ONE
        await ctx.message.author.remove_roles(*rolesToRemove) #REMOVING THE ROLE
        level = int(json["data"]["stats"][0]["value"])
        if "Kills" in json["data"]["stats"][1]["metadata"]["name"]:
            kills = int(json["data"]["stats"][1]["value"])
        else:
            kills = 0
        killsPerLevel = int(kills/level)
        try:
            role = getKillsRoleToAdd(killsPerLevel, ctx.guild)
            if killsPerLevel >= 10:
                if ctx.message.guild.region == discord.VoiceRegion.brazil:
                    embed = discord.Embed(
                        title = "**{0.name}**".format(ctx.message.author),
                        description = "Você tem **{0}** K/L (**Kills por Level**) e **{1}** kills, você é uma verdadeira lenda!  ".format(killsPerLevel, kills),
                        colour = discord.Colour.red()
                    )
                    embed.add_field(name = "**Parabéns!**", value = "Foi lhe dado o cargo {0.mention}:trophy:".format(role), inline = False)
                    await ctx.channel.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = "**{0.name}**".format(ctx.message.author),
                        description = "You have **{0}** K/L (**Kills per Level**) and **{1}** kills, you are a true legend!".format(killsPerLevel,kills),
                        colour = discord.Colour.red()
                    )
                    embed.add_field(name = "**Congratulations!**", value = "It has been assigned you the role {0.mention}:trophy:".format(role), inline = False)
                    await ctx.channel.send(embed = embed)
            else:
                if ctx.message.guild.region == discord.VoiceRegion.brazil:
                    embed = discord.Embed(
                        title = "**{0.name}**".format(ctx.message.author),
                        description = "Você tem **{0}** K/L (**Kills por Level**) e **{1}** kills, você é uma lenda em ascenção!".format(killsPerLevel,kills),
                        colour = discord.Colour.red()
                    )
                    embed.add_field(name = "**Parabéns!**", value = "Foi lhe dado o cargo {0.mention}:trophy:".format(role), inline = False)
                    await ctx.channel.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = "**{0.name}**".format(ctx.message.author),
                        description = "You have **{0}** K/L (**Kills per Level**) and **{1}** kills, you are a legend in ascension!".format(killsPerLevel,kills),
                        colour = discord.Colour.red()
                    )
                    embed.add_field(name = "**Congratulations!**", value = "It has been assigned you the role {0.mention}:trophy:".format(role), inline = False)
                    await ctx.channel.send(embed = embed)
            await ctx.message.author.add_roles(role) #ADDING THE NEW ROLE TO THE MEMBER
        except:
            if killsPerLevel >= 10:
                if ctx.message.guild.region == discord.VoiceRegion.brazil:
                    embed = discord.Embed(
                        title = "**{0.name}**".format(ctx.message.author),
                        description = "Você tem **{0}** K/L (**Kills por Level**) e **{1}** kills, você é uma verdadeira lenda!  ".format(killsPerLevel,kills),
                        colour = discord.Colour.red()
                    )
                    await ctx.channel.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = "**{0.name}**".format(ctx.message.author),
                        description = "You have **{0}** K/L (**Kills per Level**) and **{1}** kills, you are a true legend!".format(killsPerLevel,kills),
                        colour = discord.Colour.red()
                    )
                    await ctx.channel.send(embed = embed)
            else:
                if ctx.message.guild.region == discord.VoiceRegion.brazil:
                    embed = discord.Embed(
                        title = "**{0.name}**".format(ctx.message.author),
                        description = "Você tem **{0}** K/L (**Kills por Level**) e **{1}** kills, você é uma lenda em ascenção!".format(killsPerLevel,kills),
                        colour = discord.Colour.red()
                    )
                    await ctx.channel.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = "**{0.name}**".format(ctx.message.author),
                        description = "You have **{0}** K/L (**Kills per Level**) and {1} kills, you are a legend in ascension!".format(killsPerLevel,kills),
                        colour = discord.Colour.red()
                    )
                    await ctx.channel.send(embed = embed)
    elif "errors" in json:
        if ctx.message.guild.region == discord.VoiceRegion.brazil:
            await ctx.channel.send("Usuário não encontrado. Cheque se a plataforma e o nickname foram inseridos corretos.")
        else:
            await ctx.channel.send("User not found. Check if the platform and nickname were correctly inserted.")
    else:
        await ctx.channel.send(json["error"])


async def rankAutoRole(ctx,origin_nickname, platform):
    platformID = getPlatformId(platform)
    headers = {
    "TRN-Api-Key": random.choice(trnApiKey)
    }

    request = requests.get("{}{}/{}".format(getLevel,platformID,origin_nickname),headers=headers)
    json = request.json()
    
    if "data" in json:
        memberRoles = ctx.message.author.roles #GETTING ALL THE ROLES THE MEMBER HAS
        rolesToRemove = getRankRolesToRemove(memberRoles) #GETTING THE LEVEL RELATED ROLES THE MEMBER ALREADY HAVE TO REMOVE BEFORE GIVING NEW ONE
        await ctx.message.author.remove_roles(*rolesToRemove) #REMOVING THE ROLE

        rankScore = checkRankScore(json["data"]["stats"])

        try:
            print("will try to get role")
            role = getRankRoleToAdd(rankScore, ctx.guild)
            print("did get role: {}".format(role))
            if ctx.message.guild.region == discord.VoiceRegion.brazil:
                embed = discord.Embed(
                    title = "**{0.name}**".format(ctx.message.author),
                    description = "Você tem **{0}** ranked score.".format(rankScore),
                    colour = discord.Colour.red()
                )
                embed.add_field(name = "**Parabéns!**", value = "Foi lhe dado o cargo {0.mention}:trophy:".format(role), inline = False)
                await ctx.channel.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = "**{0.name}**".format(ctx.message.author),
                    description = "You have **{0}** ranked score.".format(rankScore),
                    colour = discord.Colour.red()
                )
                embed.add_field(name = "**Congratulations!**", value = "It has been assigned you the role {0.mention}:trophy:".format(role), inline = False)
                await ctx.channel.send(embed = embed)
            await ctx.message.author.add_roles(role) #ADDING THE NEW ROLE TO THE MEMBER
        except:
            if ctx.message.guild.region == discord.VoiceRegion.brazil:
                embed = discord.Embed(
                    title = "**{0.name}**".format(ctx.message.author),
                    description = "Você tem **{0}** ranked score.".format(rankScore),
                    colour = discord.Colour.red()
                )
                await ctx.channel.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = "**{0.name}**".format(ctx.message.author),
                    description = "You have **{0}** ranked score.".format(rankScore),
                    colour = discord.Colour.red()
                )
                await ctx.channel.send(embed = embed)
    elif "errors" in json:
        if ctx.message.guild.region == discord.VoiceRegion.brazil:
            await ctx.channel.send("Usuário não encontrado. Cheque se a plataforma e o nickname foram inseridos corretos.")
        else:
            await ctx.channel.send("User not found. Check if the platform and nickname were correctly inserted.")
    else:
        await ctx.channel.send(json["error"])