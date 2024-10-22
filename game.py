from colorama import init, Fore, Style
from agentmap import agentmap, agent_color_map

class Game:
    def __init__(self, party, matchID, players, localPlayer):
        self.matchID = matchID
        self.players = players
        self.localPlayer = localPlayer
        self.teamPlayers = self.find_team_players(self.localPlayer, self.players)
        self.partyPlayers = self.find_party_members(party)
    
    def find_hidden_names(self, players):
        self.found = False
        for player in players:
            agent_color = agent_color_map.get(player.agentID, Fore.WHITE)
            color = Fore.BLUE if player.team == "Defending" else Fore.RED
            if player.incognito:
                self.found = True
                print(f"{color}{player.full_name} | {player.team}{Style.RESET_ALL} | {agent_color}{player.agentID}{Style.RESET_ALL} | Hidden")
            else:
                print(f"{color}{player.full_name} | {player.team}{Style.RESET_ALL} | {agent_color}{player.agentID}{Style.RESET_ALL} | Not Hidden")
        if not self.found:
            print("No hidden names found")

    def find_team_players(self, localPlayer, players):
        team_players = []
        
        for player in players:
            if player.team == localPlayer.team:
                team_players.append(player)
        
        return team_players
    
    def find_party_members(self, party):
        members = []

        for member in party['Members']:
            members.append(member['Subject'].lower())

        return members