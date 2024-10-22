import json, time
from game import Game
from players import Player
from valclient import Client
from colorama import init, Fore, Style
import os

running = True
seenMatches = []
def clear_console():

    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

running = True
seenMatches = []

clear_console()
print(Fore.RED + 'VRYv2 Running'.center(120))

with open('settings.json', 'r') as f:
    data = json.load(f)
    ranbefore = data['ran']
    region = data['region']
    stateinterval = data['stateInterval']

if not ranbefore:
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

print('Waiting for match to get detected....'.center(120) + Style.RESET_ALL)
while running:
    time.sleep(30)
    try:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        matchID = client.coregame_fetch_player()['MatchID']

        if sessionState == 'INGAME' and matchID not in seenMatches:
            print('-' * 40)
            print('Match has been found. Loading data.')
            seenMatches.append(matchID)
            matchInfo = client.coregame_fetch_match(matchID)
            players = []

            for player in matchInfo['Players']:
                if client.puuid == player['Subject']:
                    localPlayer = Player(
                        client=client,
                        puuid=player['Subject'].lower(),
                        agentID=player['CharacterID'].lower(),
                        incognito=player['PlayerIdentity']['Incognito'],
                        team=player['TeamID']
                    )
                else:
                    players.append(Player(
                        client=client,
                        puuid=player['Subject'].lower(),
                        agentID=player['CharacterID'].lower(),
                        incognito=player['PlayerIdentity']['Incognito'],
                        team=player['TeamID']
                    ))
            currentgame = Game(party=client.fetch_party(), matchID=matchID, players=players, localPlayer=localPlayer)
            print('Printing Users:')
            print('-' *20)
            currentgame.find_hidden_names(players)
    except Exception as e:
        if 'core' not in str(e) and "NoneType" not in str(e):
            print("An error occurred: ", e)