import requests
from bs4 import BeautifulSoup
import json
from dotenv import dotenv_values

CONFIG = dotenv_values()

DISCORD_WEBHOOK = CONFIG['DISCORD_WEBHOOK']
URL_TO_SCRAPE = CONFIG['URL_TO_SCRAPE']
SEARCH_GUILD = CONFIG['SEARCH_GUILD']
PLAYED_SERVER = CONFIG['PLAYED_SERVER']
DARK_SIDE = bool(int(CONFIG['DARK_SIDE']))


def position_as_ordinal_number(position: str or int):
    position_as_int = int(position)
    namings = {
        1: "st",
        2: "nd",
        3: "rd",
    }

    naming_key = 4 if 10 <= position_as_int % 100 < 20 else position_as_int % 10
    get_naming = namings.get(naming_key, "th")

    return get_naming


def find_guild_position(rows):
    faction_css_class = "faction-1" if DARK_SIDE else "faction-0"

    position = 0
    result = {}
    for row in rows:
        row_data = row.find_all("td")

        faction_div = row_data[1].find("div")
        faction_div_classes = faction_div.attrs.get("class")

        if faction_css_class in faction_div_classes:
            position += 1

        guild_name = row_data[2].get_text()
        if guild_name != SEARCH_GUILD:
            continue

        result["placement"] = position
        result["ordinal_placement"] = position_as_ordinal_number(position)
        result["points"] = row_data[4].get_text()
        break

    return result


def send_message(message):
    payload = {
        "content": message
    }
    json_payload = json.dumps(payload)

    try:
        requests.post(DISCORD_WEBHOOK, data=json_payload, headers={"Content-Type": "application/json"})
    except Exception as e:
        print(e)


def send_discord_message():
    try:
        response = requests.get(URL_TO_SCRAPE)
        html_as_text = response.text

        soup = BeautifulSoup(html_as_text, "html.parser")
        guild_ranks_tbody = soup.find("table").find("tbody")
        all_rows = guild_ranks_tbody.find_all("tr")

        guild_data = find_guild_position(all_rows)
        side = "Fury" if DARK_SIDE else "Light"

        message = f"@here {SEARCH_GUILD} ranked " \
                  f"{guild_data.get('placement', 'unknown')}{guild_data.get('ordinal_placement', '')} among all {side} guilds " \
                  f"with {guild_data.get('points', '0')} points at - {PLAYED_SERVER}!"
        send_message(message)
    except Exception as e:
        print(e)


send_discord_message()