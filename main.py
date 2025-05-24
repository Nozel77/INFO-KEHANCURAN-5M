import asyncio
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

async def main():
    await Commands.info(bot)
    await Commands.listkota(bot)
    await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Bot dihentikan oleh user")
