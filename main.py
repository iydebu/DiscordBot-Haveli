import os
import requests
import json
import discord
import random
from discord import app_commands
from discord.ext import commands
from replit import db

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "-" + json_data[0]['a']
  return quote


def get_joke():
  url = "https://dad-jokes.p.rapidapi.com/random/joke"

  headers = {
    "X-RapidAPI-Key": "f7aac33b84msh891c243ba5636c8p14442cjsn7019b536442c",
    "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
  }

  response = requests.request("GET", url, headers=headers)
  json_data = json.loads(response.text)
  joke = json_data['body'][0]['setup'] + " - " + json_data['body'][0][
    'punchline']
  return joke


def get_news():
  url = ('https://newsapi.org/v2/top-headlines?'
         'country=us&'
         'apiKey=2f46a0a6423443b587917342865febd2')
  response = requests.get(url)
  json_data = json.loads(response.text)
  max = len(json_data['articles'])
  min = 0
  choice = random.randint(min, max)
  news_data = json_data['articles'][int(choice)]
  embed = discord.Embed(title=news_data['title'],
                        description=news_data['description'],
                        colour=discord.Colour.blue())
  embed.set_image(url=f"{news_data['urlToImage']}")
  embed.set_footer(text=f"{news_data['publishedAt']}")
  embed.set_author(
    name=news_data['source']['name'],
    icon_url=
    'https://cdn.discordapp.com/attachments/1038406718041894912/1038408413891276820/Dark_Blue__White_Robot_Logo.png'
  )
  embed.add_field(name="Link:", value=f"{news_data['url']}", inline=False)
  return embed


@bot.event
async def on_ready():
  print("Bot is online")
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands(s)")
  except Exception as e:
    print(e)


@bot.tree.command(name="namaste")
async def namaste(interaction: discord.Interaction):
  await interaction.response.send_message(
    f"Namaste {interaction.user.mention}! haveli me apka swagat hai")


@bot.tree.command(name="bolo")
@app_commands.describe(kya_kahana_hai_muje="mai kya bolu?")
async def say(interaction: discord.Interaction, kya_kahana_hai_muje: str):
  await interaction.response.send_message(
    f"{interaction.user.name} said:'{kya_kahana_hai_muje}'")


@bot.tree.command(name="quote")
async def quote(interaction: discord.Interaction):
  await interaction.response.send_message(get_quote())


@bot.tree.command(name="mere_bare_me")
async def mere_bare_me(interaction: discord.Interaction):
  db_keys = db.keys()
  if (str(interaction.user.mention) in db_keys):
    msg = db.get(str(interaction.user.mention))
    await interaction.response.send_message(msg)
  else:
    await interaction.response.send_message(
      "aapki ka koi message nahi mila ! pahale message ko banaiye is command se '/mai_hu' command"
    )


@bot.tree.command(name="mai_hu")
@app_commands.describe(aap_kon_ho="mai kon hu?")
async def mai_hu(interaction: discord.Interaction, aap_kon_ho: str):
  db[str(interaction.user.mention)] = aap_kon_ho
  await interaction.response.send_message("aapka hukum sarakho me!")


@bot.tree.command(name="majak")
async def majak(interaction: discord.Interaction):
  await interaction.response.send_message(get_joke())


@bot.tree.command(name="iska")
@app_commands.describe(user_ka_naam="user na naam ping karo")
async def iska(interaction: discord.Interaction, user_ka_naam: str):
  print(user_ka_naam)
  db_keys = db.keys()
  if (user_ka_naam in db_keys):
    msg = db.get(user_ka_naam)
    await interaction.response.send_message(user_ka_naam + " : " + msg)
  else:
    await interaction.response.send_message(user_ka_naam + "ye kon hai!")


@bot.tree.command(name="khabar")
async def khabar(interaction: discord.Interaction):
  await interaction.response.send_message(embed=get_news())


my_secret = os.environ['token']
bot.run(my_secret)
