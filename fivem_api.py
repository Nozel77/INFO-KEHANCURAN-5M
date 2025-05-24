import requests
import os

async def GetFivemServerInfo(joinId: str, filterKeyword: str = ""):
    apiUrl = f"{os.getenv('FIVEM_API_BASE')}/{joinId}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://servers.fivem.net/",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(apiUrl, headers=headers)
        response.raise_for_status()
        data = response.json()

        serverData = data.get("Data", {})
        svMaxclients = serverData.get("svMaxclients", 0)
        varsData = serverData.get("vars", {})

        projectName = varsData.get("sv_projectName") or serverData.get("hostname", "Unknown Server")
        bannerUrl = varsData.get("banner_connecting", None)
        playerCount = serverData.get("clients", 0)

        players = serverData.get("players", [])
        filteredPlayers = [
            {
                "id": player.get("id", player.get("endpoint_id", player.get("src", "UnknownID"))),
                "name": player.get("name", "Unknown")
            }
            for player in players
            if filterKeyword.lower() in player.get("name", "").lower()
        ]

        if not filteredPlayers:
            playerList = "Tidak ada pemain yang cocok dengan filter."
        else:
            playerList = "\n".join(
                f"{i + 1}. {p['name']} ({p['id']})" for i, p in enumerate(filteredPlayers)
            )

        return {
            "projectName": projectName,
            "playerCount": playerCount,
            "filteredPlayers": playerList,
            "rawFilteredPlayers": filteredPlayers,
            "svMaxclients": svMaxclients,
            "bannerUrl": bannerUrl
        }

    except Exception as error:
        return {"error": str(error)}
