import requests
from bs4 import BeautifulSoup
import json
from dotenv import dotenv_values

CONFIG = dotenv_values()

DISCORD_WEBHOOK = CONFIG['DISCORD_WEBHOOK']
URL_TO_SCRAPE = CONFIG['URL_TO_SCRAPE']
SEARCH_GUILD = CONFIG['SEARCH_GUILD']
PLAYED_SERVER = CONFIG['PLAYED_SERVER']


def position_as_ordinal_number(position: str):
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
    result = {}
    for row in rows:
        ranked_place, _, guild_name, _, guild_points, _ = [td.get_text() for td in row.find_all("td")]

        if guild_name != SEARCH_GUILD:
            continue

        result["placement"] = ranked_place
        result["ordinal_placement"] = position_as_ordinal_number(ranked_place)
        result["points"] = guild_points
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

        message = f"@here {SEARCH_GUILD} ranked " \
                  f"{guild_data.get('placement', 'unknown')}{guild_data.get('ordinal_placement', '')} with " \
                  f"{guild_data.get('points', '0')} points at - {PLAYED_SERVER}!"
        send_message(message)
    except Exception as e:
        print(e)


send_discord_message()