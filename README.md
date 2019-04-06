# If you just want to use my bot on your server:
* Create one channel with "level" (without commas) in it's name. My bot only accepts commands sent in channels that contains level in it's name, commands in other channels will be deleted automatically(If you give it permissions to see and delete messages in the other channels ofc).
* (Optional) Create roles for level ranges, so the !lvl command will work on your server too. You can create any level range roles, but they should be formatted as X+ being X the numbers of the levels. (Example of role names: 10+, 50+, 150+)
* (Optional) Create a channel with "welcome" in it's name(if you are in Brazil, create one with "bem-vindo" instead), this channel will be the one where you can stick a message with the Apex Legends reactions so the bot will auto-role. 
* There is a new function called !kills that also auto-roles but FOR NOW it only auto-roles if you create a role called "10 + K/L" but i'll work to make it work for all roles you create that has "K/L" in it.
* [Add Bot to Server](https://discordapp.com/api/oauth2/authorize?client_id=547439065801162763&permissions=0&scope=bot)

# Functions:
* Auto-role on reaction: If you create reactions for all the legends on Apex and a role with the SAME name, when the reaction is clicked, the bot will auto-role. Same works for platform roles. Actually, any reaction you add that you also add a role with the SAME name the bot can do that for you. Ex: (Reaction: Wraith, Role: Wraith)
* !register PLATFORM NICKNAME: Register your platform and nickname along your discord_id on the database, so you won't need to always type them again when auto-roling.
* !lvl PLATFORM NICKNAME: Searchs for this Origin nickname, check it's level on apex, and autorole the message author with the related role. Also adds the level right next to the nickname. If you have registered your platform and nickname, you can use only !lvl.
* !kills PLATFORM NICKNAME: Searchs for this Origin nickname, check it's kills on apex, tells how many kills and kills per level the message author has and autorole the message author with the related role.
* !check_level PLATFORM NICKNAME: Searchs for this Origin nickname, check it's level on apex tells the level but doens't autorole
* !check_kills PLATFORM NICKNAME: Searchs for this Origin nickname, check it's number of kills and tells it.
* !list_commands: Help function, unfortunately i couldn't manage to override the help function, so i made another with different name.

# If not, you can modify it according to your needs following the steps below:

## Pre-requisites:
* Have  2.7>Python Version<3.7.X installed (you don't need it if you aren't planning to run it on your PC though) 
* Have Discord.py installed, see [Discord.py](https://github.com/Rapptz/discord.py) for that.
## Step-By-Step:
* Rename the ConfigExample.py to config.py
* Go to [Apex API](https://apex.tracker.gg/site-api) and request your API Key.
* Create your Discord App on [Discord Developers](https://discordapp.com/login?redirect_to=%2Fdevelopers%2Fapplications%2F) (There are many youtube videos teaching that) and get your discord token.
* Once you have your 2 needed keys, replace them on the specified place at the config.py
* Go to Firebase Console, create your project and replace your config JSON on the specified place(Or ignore this part and delete Firebase related code from project).
* Replace all fields on your config.py file.
* That's it.

## Running on Heroku (Optional)
In case you want to host your bot 24/7 on Heroku, i have provided the needed files altogether (main.py, requirements.txt, Procfile), all you need to do is:
* Upload your project to your github
* Go on Heroku, create your app, then go on Deploy and sync it with the right repository on github
* Go on Setting and add a buildpack (heroku/python)
* Go back on Deploy and deploy the branch.
* That's it
