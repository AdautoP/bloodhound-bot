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
    if server.id == serverID:
        for i in server.roles:
            if("-" in i.name):
                array = i.name.split("-")
                if array[0].isdigit() and array[1].isdigit():
                    if(level>= int(array[0]) and level <int(array[1])):
                        return i
            else:
                if("Lenda" in i.name):
                    if(level >= 100):
                        return i
    else:
        for i in server.roles:
            if("-" in i.name):
                array = i.name.split("-")
                if array[0].isdigit() and array[1].isdigit():
                    if(level>= int(array[0]) and level <int(array[1])):
                        return i

def getRolesToRemove(roles):
    rolesToRemove = []
    for role in roles:
        if ("-" in role.name):
            array = role.name.split("-")
            if array[0].isdigit() and array[1].isdigit():
                rolesToRemove.append(role)
    return rolesToRemove

def getPlatformId(platform):
    if(platform == "pc" or platform == "PC"):
        return 5
    elif (platform == "xbox" or platform == "XBOX" or platform == "Xbox"):
        return 1
    elif (platform == "ps4" or platform == "PS4"):
        return 2

async def autorole(ctx,origin_nickname, platform):
    platformID = getPlatformId(platform)
    headers = {
    "TRN-Api-Key": random.choice(trnApiKey)
    }

    request = requests.get("{}{}/{}".format(getLevel,platformID,origin_nickname),headers=headers)
    json = request.json()
    if "data" in json:
        level = int(json["data"]["stats"][0]["value"])
        memberRoles = ctx.message.author.roles #GETTING ALL THE ROLES THE MEMBER HAS
        rolesToRemove = getRolesToRemove(memberRoles) #GETTING THE LEVEL RELATED ROLES THE MEMBER ALREADY HAVE TO REMOVE BEFORE GIVING NEW ONE
        await ctx.message.author.remove_roles(*rolesToRemove) #REMOVING THE ROLE
        role = getLevelRoleToAdd(level,ctx.message.guild) #GETTING THE NEW ROLE BASED ON THE LEVEL THE MEMBER HAS NOW
        if ctx.message.guild.region == discord.VoiceRegion.brazil:
            embed = discord.Embed(
                title = "{0.name}".format(ctx.message.author),
                description = "Seu level é {0}, foi lhe dado o cargo {1.mention}.".format(level,role),
                colour = discord.Colour.red()
            )
            await ctx.channel.send(embed = embed)
        else:
            embed = discord.Embed(
                title = "{0.name}".format(ctx.message.author),
                description = "Your level is {0}, it has been given you the {1.mention} role.".format(level,role),
                colour = discord.Colour.red()
            )
            await ctx.channel.send(embed = embed)
        await ctx.message.author.add_roles(role) #ADDING THE NEW ROLE TO THE MEMBER
        try:
            if ("★" in ctx.message.author.nick):
                nickAux = ctx.message.author.nick.split("★")
                woSpace = nickAux[0].split(" ")
                if woSpace[0].isdigit():
                    woSpace = nickAux[1].split("")
                    await ctx.message.author.edit(nick = "{} {} {}".format(level,"★",woSpace[0]))
                else:
                    await ctx.message.author.edit(nick = "{} {} {}".format(level ,"★",woSpace[0] ))
            else:
                await ctx.message.author.edit(nick = "{} {} {}".format(level,"★",ctx.message.author.nick))    
        except:
            await ctx.message.author.edit(nick = "{} {} {}".format(level,"★",ctx.message.author.name))
    elif "errors" in json:
        await ctx.channel.send(json["errors"][0]["message"])
    else:
        await ctx.channel.send(json["error"])
