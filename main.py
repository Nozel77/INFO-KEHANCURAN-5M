import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from commands import Commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} siap digunakan.")

def register_commands():
    Commands.info(bot)
    Commands.listkota(bot)

if __name__ == "__main__":
    register_commands()
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ Token Discord BOT tidak ditemukan di environment variables!")
        exit(1)
    bot.run(token)
