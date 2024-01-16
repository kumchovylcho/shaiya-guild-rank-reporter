import requests
from bs4 import BeautifulSoup
import json
from dotenv import dotenv_values

CONFIG = dotenv_values()

GUILDS_DATA = CONFIG['GUILDS']
PLAYED_SERVER = CONFIG['PLAYED_SERVER']


def guilds_data_as_dict(guilds_data: str):
    as_dict = []
    for guild in guilds_data.split(","):
        if not guild or guild == "\n":
            continue
        name, side, discord_webhook = [pair.split("=")[1] for pair in guild.split(";")]
        as_dict.append({"name": name, "is_fury": bool(int(side)), "discord_webhook": discord_webhook})
    return as_dict


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


def find_guild_position(rows, look_for_guild_name: str, is_fury: bool):
    faction_css_class = "faction_dark" if is_fury else "faction_light"

    position = 0
    result = {}
    for row in rows:
        row_data = row.find_all("td")

        faction_div = row_data[1].find("div")
        faction_div_classes = faction_div.attrs.get("class")

        if faction_css_class in faction_div_classes:
            position += 1

        guild_name = row_data[2].get_text()
        if guild_name != look_for_guild_name:
            continue

        result["placement"] = position
        result["ordinal_placement"] = position_as_ordinal_number(position)
        result["points"] = row_data[4].get_text()
        break

    return result


def send_message(message: str, webhook: str):
    payload = {
        "content": message
    }
    json_payload = json.dumps(payload)

    try:
        requests.post(webhook, data=json_payload, headers={"Content-Type": "application/json"})
    except Exception as e:
        print(e)


def send_discord_messages(guilds_data: list[dict]):
    try:
        html = """
<tbody>

													<tr>
								<td>1</td>
                                <td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
                                <td><a>Test</a></td>
								<td><a style="font-weight: 600;margin-top: 4px;">milSugio2</a></td> 
                                <td style="font-weight: 600;font-size: 16px;">0</td>
							</tr>
														<tr>
								<td>2</td>
                                <td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
                                <td><a>Uno.</a></td>
								<td><a style="font-weight: 600;margin-top: 4px;">Genesis1</a></td> 
                                <td style="font-weight: 600;font-size: 16px;">0</td>
							</tr>
														<tr>
								<td>3</td>
                                <td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
                                <td><a>GUILD</a></td>
								<td><a style="font-weight: 600;margin-top: 4px;">Fighter</a></td> 
                                <td style="font-weight: 600;font-size: 16px;">4025</td>
							</tr>
													</tbody>
        """

        soup = BeautifulSoup(html, "html.parser")
        guild_ranks_tbody = soup.find("tbody")
        all_rows = guild_ranks_tbody.find_all("tr")

        for guild in guilds_data:
            guild_data = find_guild_position(all_rows, guild["name"], guild["is_fury"])
            side = "Fury" if guild["is_fury"] else "Light"

            message = f"@here {guild['name']} ranked " \
                      f"{guild_data.get('placement', 'unknown')}{guild_data.get('ordinal_placement', '')} among all {side} guilds " \
                      f"with {guild_data.get('points', 'unknown')} points at - {PLAYED_SERVER}!"
            send_message(message, guild["discord_webhook"])
    except Exception as e:
        print(e)


guilds_as_dict = guilds_data_as_dict(GUILDS_DATA)
send_discord_messages(guilds_as_dict)