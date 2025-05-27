import os
import json
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

_browser = None
_context = None
_page = None
_playwright = None

async def _init_browser():
    global _playwright, _browser, _context, _page
    if _playwright is None:
        _playwright = await async_playwright().start()
    if _browser is None:
        _browser = await _playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-zygote',
                '--single-process',
                '--disable-gpu',
            ]
        )
    if _context is None:
        _context = await _browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 800, "height": 600},
            extra_http_headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://servers-frontend.fivem.net/",
                "Origin": "https://servers-frontend.fivem.net"
            }
        )
    if _page is None:
        _page = await _context.new_page()

async def _close_browser():
    global _playwright, _browser, _context, _page
    if _page:
        await _page.close()
        _page = None
    if _context:
        await _context.close()
        _context = None
    if _browser:
        await _browser.close()
        _browser = None
    if _playwright:
        await _playwright.stop()
        _playwright = None

async def GetFivemServerInfo(joinId: str, filterKeyword: str = ""):
    await _init_browser()
    apiUrl = f"{os.getenv('FIVEM_API_BASE')}/{joinId}"

    try:
        response = await _page.goto(apiUrl, wait_until="domcontentloaded", timeout=10000)
        if not response or response.status != 200:
            return {"error": f"HTTP error {response.status if response else 'No response'}"}

        content = await response.text()
        data = json.loads(content)

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

    except PlaywrightTimeoutError:
        return {"error": "Request timeout (10s)"}
    except Exception as error:
        return {"error": str(error)}
