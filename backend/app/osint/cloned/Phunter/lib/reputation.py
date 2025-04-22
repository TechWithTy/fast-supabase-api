from .Requests import Request
from bs4 import BeautifulSoup
from .text import *
import random
from .useragent import user_agent


async def reputation(phone_number):
    r = await Request(url="https://www.tellows.fr/num/%2B{}".format(phone_number), headers={"user-agent": random.choice(user_agent)}).get()

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        reputation = soup.find("div", {"class": "col-lg-9"}).findAll("h1")

        try:
            info = f"\n [{GREEN}>{WHITE}] Reputation: {reputation[0].text.strip()}"
        except Exception:
            info = f"\n [-] No reputation found "
        print(info)
        return info
    else:
        info = f"\n [-] No reputation found "
        return info