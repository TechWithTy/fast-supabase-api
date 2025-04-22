from .Requests import *
import random
from .text import *
from .useragent import user_agent


async def spamcalls(p_n):
    print(f"\n [{GREEN}>{WHITE}] Spamcalls")

    url = f"https://spamcalls.net/en/number/{p_n}"

    r = await Request(url, headers={'user-agent': random.choice(user_agent)}).get()

    if r.status_code == 200:
        print(f"  └── {RED}!{WHITE} Spammer")
        return True
    else:
        print(f"  └── {GREEN}>{WHITE} Not spammer")
        return False