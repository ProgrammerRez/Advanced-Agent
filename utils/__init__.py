from bs4 import BeautifulSoup
import aiohttp


# =========================
# UTILS
# =========================

def extract_clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "nav", "footer", "aside", "noscript"]):
        tag.decompose()

    main = soup.find("article") or soup.find("main") or soup.body
    if not main:
        return ""

    text = "\n".join(
        p.get_text(strip=True)
        for p in main.find_all(["p", "h1", "h2", "h3"])
        if len(p.get_text(strip=True)) > 40
    )

    return text[:1200]


async def fetch_page(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url, timeout=6) as resp:
            if resp.status == 200:
                html = await resp.text()
                text = extract_clean_text(html)
                if text:
                    return url, text
    except Exception:
        return None
