import json, time
from game import Game
from players import Player
from valclient import Client
from colorama import init, Fore, Style
import os

running = True
seen_matches = []
def clear_console():

    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

running = True
seen_matches = []

clear_console()
print(Fore.LIGHTRED_EX + 'VRYv2 Running'.center(120))

with open('settings.json', 'r') as f:
    data = json.load(f)
    ran_before = data['ran']
    region = data['region']
    state_interval = data['state_interval']

if not ran_before:
    prompt = 'Enter your region: '
    padding = (120 - len(prompt)) // 2
    region = input(' ' * padding + prompt).lower()

    if region == "europe":
        region = "eu"
    elif region == "northamerica":
        region = "na"

    client = Client(region=region)
    client.activate()

    with open('settings.json', 'w') as f:
        data['ran'] = True
        data['region'] = region
        json.dump(data, f, indent=4)
else:
    client = Client(region=region)
    client.activate()

print('Waiting for match to get detected...'.center(120) + Style.RESET_ALL)
while running:
    time.sleep(30)
    try:
        session_state = client.fetch_presence(client.puuid)['sessionLoopState']
        match_id = client.coregame_fetch_player()['MatchID']

        if session_state == 'INGAME' and match_id not in seen_matches:
            print('-'.center(120) * 40)
            print('Match has been found. Loading data.'.center(120))
            seen_matches.append(match_id)
            match_info = client.coregame_fetch_match(match_id)
            players = []

            for player in match_info['Players']:
                if client.puuid == player['Subject']:
                    local_player = Player(
                        client=client,
                        p_uuid=player['Subject'].lower(),
                        agent_id=player['CharacterID'].lower(),
                        incognito=player['PlayerIdentity']['Incognito'],
                        team=player['TeamID']
                    )
                else:
                    players.append(Player(
                        client=client,
                        p_uuid=player['Subject'].lower(),
                        agent_id=player['CharacterID'].lower(),
                        incognito=player['PlayerIdentity']['Incognito'],
                        team=player['TeamID']
                    ))
            current_game = Game(party=client.fetch_party(), match_id=match_id, players=players, local_player=local_player)
            print('Printing Users:')
            print('-' * 63)
            current_game.find_hidden_names(players)
    except Exception as e:
        if 'core' not in str(e) and "NoneType" not in str(e):
            print("An error occurred: ", e)
