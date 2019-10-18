# Import Modules
import os
import gspread
import discord
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("DanMemoStats").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Connects bot to discord

client = discord.Client()

# Output to Console if Bot is Connected

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#Returns Output from Command

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!AssistAlliesMRes':
        for mres in list_of_hashes: 
            if r'[Allies] M. Resist' in mres['Ability']:
                response = mres['Name']
                await message.channel.send(response)
    if message.content == '!AssistAlliesPRes':
        for mres in list_of_hashes: 
            if r'[Allies] P. Resist' in mres['Ability']:
                response = mres['Name']
                await (response)
    if message.content == '!AssistAlliesStunRes':
        for mres in list_of_hashes: 
            if r'[Allies] Stun' in mres['Ability']:
                embed = discord.Embed(title=mres['Name'], color=0x00ff00 )
                embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
                Stats = f''' 
                HP:\t{mres['HP']}
                MP:\t{mres['MP']}
                P. AT:\t{mres['P. AT']}
                M. AT:\t{mres['M. AT']}
                DEF:\t{mres['DEF']}               
                '''
                Stats2 = f''' 
                STR:\t{mres['Str']}
                END:\t{mres['End']}
                DEX:\t{mres['Dex']}
                AGI:\t{mres['Agi']}
                MAG:\t{mres['Mag']}               
                '''
                Abilities = f"{mres['Ability']} {mres['Ability Change']}"
                embed.add_field(name="Stats Primary",value=Stats, inline=True)
                embed.add_field(name="Stats Secondary",value=Stats2, inline=True)
                embed.add_field(name="Abilities",value=Abilities, inline=False)
                await message.channel.send(embed=embed)           

client.run(token)

