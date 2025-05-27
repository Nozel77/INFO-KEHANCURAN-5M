import os
import discord
from utils import ServerFunctionality
import json

serverMap = json.loads(os.getenv("SERVER_MAP"))

class Commands:
    def info(bot):
        @bot.command(name="info")
        async def InfoCommand(ctx, serverName: str, *, filterKeyword: str = ""):
            joinId = serverMap.get(serverName.lower())
            if not joinId:
                await ctx.send(f"❌ Server `{serverName}` tidak ditemukan.")
                return

            await ServerFunctionality.SendServerInfo(ctx, joinId, filterKeyword)
            
    def listkota(bot):
        @bot.command(name="listkota")
        async def ListKotaCommand(ctx):
            if not serverMap:
                await ctx.send("⚠️ Belum ada kota/server yang terdaftar.")
                return

            kota_list = "\n".join(f"- `{key}`" for key in serverMap.keys())

            embed = discord.Embed(
                title="🗺️ Daftar Kota/Server yang Tersedia",
                description=kota_list,
                color=0x00bfff
            )
            embed.set_footer(text="Gunakan !info <nama_kota> untuk melihat info server.")

            await ctx.send(embed=embed)