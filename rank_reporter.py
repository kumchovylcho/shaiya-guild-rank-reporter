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


def create_sorted_sides_data(tbody_rows, faction_css_class: str):
    result = []
    for row in tbody_rows:
        row_data = row.find_all("td")

        faction_div = row_data[1].find("div")
        faction_div_classes = faction_div.attrs.get("class")

        if faction_css_class in faction_div_classes:
            result.append({
                "guild_name": row_data[2].get_text(),
                "points": int(row_data[4].get_text())
            })

    result = sorted(result, key=lambda x: -x["points"])

    return result


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


def find_guild_position(side_guilds: list[dict], look_for_guild_name: str):
    result = {}
    for i in range(len(side_guilds)):
        guild = side_guilds[i]
        if guild["guild_name"] != look_for_guild_name:
            continue

        result["placement"] = i + 1
        result["ordinal_placement"] = position_as_ordinal_number(i + 1)
        result["points"] = guild["points"]
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
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Hate</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Munchy</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>2</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>TO4ILKATAAAAA</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Moderet[681]</a></td>
<td style="font-weight: 600;font-size: 16px;">33475</td>
</tr>
<tr>
<td>3</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>NDs</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Chobans</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>4</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Demolition</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Junjee</a></td>
<td style="font-weight: 600;font-size: 16px;">30011</td>
</tr>
<tr>
<td>5</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>God</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">[GS]Mephisto[$]</a></td>
<td style="font-weight: 600;font-size: 16px;">32629</td>
</tr>
<tr>
<td>6</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>c y a</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">harry</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>7</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>phip</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">ghip</a></td>
<td style="font-weight: 600;font-size: 16px;">26329</td>
</tr>
<tr>
<td>8</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Annihilation</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Popki</a></td>
<td style="font-weight: 600;font-size: 16px;">20305</td>
</tr>
<tr>
<td>9</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>I AM LEGEND IN SHAIYA</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">uBeenLuredBro</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>10</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>rapido</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">kittyslayuwu</a></td>
<td style="font-weight: 600;font-size: 16px;">25409</td>
</tr>
<tr>
<td>11</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Dark Syndicate</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">[DSy]Miracle-</a></td>
<td style="font-weight: 600;font-size: 16px;">34263</td>
</tr>
<tr>
<td>12</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Criminals</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Kubas</a></td>
<td style="font-weight: 600;font-size: 16px;">337</td>
</tr>
<tr>
<td>13</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Famous</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Adel</a></td>
<td style="font-weight: 600;font-size: 16px;">20870</td>
</tr>
<tr>
<td>14</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Halloween Town</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Jack.</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>15</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>22cm</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Lia</a></td>
<td style="font-weight: 600;font-size: 16px;">33261</td>
</tr>
<tr>
<td>16</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Priscus</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Genocide</a></td>
<td style="font-weight: 600;font-size: 16px;">33803</td>
</tr>
<tr>
<td>17</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>BlackHole</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Fz25</a></td>
<td style="font-weight: 600;font-size: 16px;">27992</td>
</tr>
<tr>
<td>18</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Hellezzkie</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Recrent</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>19</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Public Enemy</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">[IGB]Prado</a></td>
<td style="font-weight: 600;font-size: 16px;">22258</td>
</tr>
<tr>
<td>20</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Immortality</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Trynda</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>21</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>esophagus esophagus</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">[GS]Bomby</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>22</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Infinity</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">CarloSantana</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>23</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>hehe</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Tashi</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>24</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Angry Pussy</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">nStinct</a></td>
<td style="font-weight: 600;font-size: 16px;">20058</td>
</tr>
<tr>
<td>25</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>show must go on</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Kin</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>26</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Dont Drama</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Sophie</a></td>
<td style="font-weight: 600;font-size: 16px;">25911</td>
</tr>
<tr>
<td>27</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>VietSub</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">HOT</a></td>
<td style="font-weight: 600;font-size: 16px;">76</td>
</tr>
<tr>
<td>28</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Odyssey Staff</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">[GM]Nyx</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>29</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>9Lives</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Leia</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>30</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>unmatched</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">cocosul</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>31</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>erase una vez</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Jovia-</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>32</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>CMarseilleBB</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">DaddyChocolat</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>33</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>NLB</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Yoogi</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>34</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>.</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">ivy</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>35</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Sanctuary Empire</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">[WHOS]IMoan</a></td>
<td style="font-weight: 600;font-size: 16px;">23203</td>
</tr>
<tr>
<td>36</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>2Ms</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">cHEMs</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>37</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>HomeLess</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">[no]food</a></td>
<td style="font-weight: 600;font-size: 16px;">565</td>
</tr>
<tr>
<td>38</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Dontmesswithme</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">MorningCoffee</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>39</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>ROTASIZLAR</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">BABAYAGA</a></td>
<td style="font-weight: 600;font-size: 16px;">23112</td>
</tr>
<tr>
<td>40</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>SexyShadow</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">ChoA</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>41</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Kudos</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Bip</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>42</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Chromium</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">raysush</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>43</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>D0MINATION</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Larz</a></td>
<td style="font-weight: 600;font-size: 16px;">20839</td>
</tr>
<tr>
<td>44</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Turkish Army</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">KafamRahat</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>45</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Lights Syndicate</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Viscooo.</a></td>
<td style="font-weight: 600;font-size: 16px;">3194</td>
</tr>
<tr>
<td>46</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Phantom Troupe</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Chrollo</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>47</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Acoustic</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">spades</a></td>
<td style="font-weight: 600;font-size: 16px;">1112</td>
</tr>
<tr>
<td>48</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>EL CHAPO</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">TruePA-</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>49</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>khhhhhhh</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Pui</a></td>
<td style="font-weight: 600;font-size: 16px;">2831</td>
</tr>
<tr>
<td>50</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Cheers</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Dansoo</a></td>
<td style="font-weight: 600;font-size: 16px;">4512</td>
</tr>
<tr>
<td>51</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>KK3</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Buu</a></td>
<td style="font-weight: 600;font-size: 16px;">97</td>
</tr>
<tr>
<td>52</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>pridurka</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">4urka</a></td>
<td style="font-weight: 600;font-size: 16px;">20438</td>
</tr>
<tr>
<td>53</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>brings back memories</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">yel</a></td>
<td style="font-weight: 600;font-size: 16px;">241</td>
</tr>
<tr>
<td>54</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>InvictuZ</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Xena-</a></td>
<td style="font-weight: 600;font-size: 16px;">22483</td>
</tr>
<tr>
<td>55</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Furylicious</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">meshti</a></td>
<td style="font-weight: 600;font-size: 16px;">23119</td>
</tr>
<tr>
<td>56</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>JebZ..</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">JonS</a></td>
<td style="font-weight: 600;font-size: 16px;">2738</td>
</tr>
<tr>
<td>57</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>vanquisher</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">[ADV]Boji</a></td>
<td style="font-weight: 600;font-size: 16px;">523</td>
</tr>
<tr>
<td>58</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Tits</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Sexy</a></td>
<td style="font-weight: 600;font-size: 16px;">24333</td>
</tr>
<tr>
<td>59</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Frahndes</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">DNT</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>60</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Nosleep</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">STK</a></td>
<td style="font-weight: 600;font-size: 16px;">1304</td>
</tr>
<tr>
<td>61</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>HALANGA OY</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Em</a></td>
<td style="font-weight: 600;font-size: 16px;">21821</td>
</tr>
<tr>
<td>62</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Tressemme</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">GET</a></td>
<td style="font-weight: 600;font-size: 16px;">73</td>
</tr>
<tr>
<td>63</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Krahos</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">SKL</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>64</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>DJ House</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">HKTJSN</a></td>
<td style="font-weight: 600;font-size: 16px;">671</td>
</tr>
<tr>
<td>65</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Rhyder</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">VNV</a></td>
<td style="font-weight: 600;font-size: 16px;">0</td>
</tr>
<tr>
<td>66</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_dark" title="Union of Fury"></div></td>
<td><a>Jook</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">Zz4</a></td>
<td style="font-weight: 600;font-size: 16px;">20373</td>
</tr>
<tr>
<td>67</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>Vengeance</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">BuckxNaked</a></td>
<td style="font-weight: 600;font-size: 16px;">572</td>
</tr>
<tr>
<td>68</td>
<td><div style="margin-left: 14px;" class="faction_icon faction_light" title="Alliance of Light"></div></td>
<td><a>GermanBobs</a></td>
<td><a style="font-weight: 600;margin-top: 4px;">RangerGirl</a></td>
<td style="font-weight: 600;font-size: 16px;">932</td>
</tr>
</tbody>
        """

        soup = BeautifulSoup(html, "html.parser")
        guild_ranks_tbody = soup.find("tbody")
        all_rows = guild_ranks_tbody.find_all("tr")

        all_light_guilds = create_sorted_sides_data(all_rows, "faction_light")
        all_fury_guilds = create_sorted_sides_data(all_rows, "faction_dark")

        for guild in guilds_data:
            which_side = all_fury_guilds if guild["is_fury"] else all_light_guilds

            guild_data = find_guild_position(which_side, guild["name"])
            side = "Fury" if guild["is_fury"] else "Light"

            message = f"@here {guild['name']} ranked " \
                      f"{guild_data.get('placement', 'unknown')}{guild_data.get('ordinal_placement', '')} among all {side} guilds " \
                      f"with {guild_data.get('points', 'unknown')} points at - {PLAYED_SERVER}!"

            send_message(message, guild["discord_webhook"])
    except Exception as e:
        print(e)


guilds_as_dict = guilds_data_as_dict(GUILDS_DATA)
send_discord_messages(guilds_as_dict)