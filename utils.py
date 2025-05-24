import os
import discord
from fivem_api import GetFivemServerInfo
from views import PlayerListView

class ServerFunctionality:
    async def SendServerInfo(ctx, joinId, keyword):
        result = await GetFivemServerInfo(joinId, keyword)

        if "error" in result:
            await ctx.send(f"❌ Gagal mengambil data server: {result['error']}")
            return

        embed = discord.Embed(
            title="INFO KEHANCURAN",
            color=0x00bfff
        )
        embed.add_field(name="**Server Name**", value=f"{result['projectName']}", inline=False)
        embed.add_field(name="**Player Online**", value=f"{result['playerCount']}/{result['svMaxclients']}", inline=False)

        players_raw = result['rawFilteredPlayers']

        if len(players_raw) > 15:
            view = PlayerListView(players_raw, page_size=15)
            embed.add_field(name=f"**Player List (Page 1/{view.total_pages})**", value=f"```{view.get_page_content()}```", inline=False)
            if result.get("bannerUrl"):
                embed.set_image(url=result["bannerUrl"])
            embed.set_footer(
                icon_url=os.getenv("DISCORD_FOOTER_ICON"),
                text="#NOZELL #BOSENG"
            )
            await ctx.send(embed=embed, view=view)
        else:
            embed.add_field(name="**Player List**", value=f"```{result['filteredPlayers']}```", inline=False)
            if result.get("bannerUrl"):
                embed.set_image(url=result["bannerUrl"])
            embed.set_footer(
                icon_url=os.getenv("DISCORD_FOOTER_ICON"),
                text="#NOZELL #BOSENG"
            )
            await ctx.send(embed=embed)