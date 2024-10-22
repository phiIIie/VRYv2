from colorama import init, Fore, Style
from agentmap import agent_map, agent_color_map

class Game:
    def __init__(self, party, match_id, players, local_player):
        self.match_id = match_id
        self.players = players
        self.local_player = local_player
        self.team_players = self.find_team_players(self.local_player, self.players)
        self.party_players = self.find_party_members(party)
    
    def find_hidden_names(self, players):
        self.found = False
        for player in players:
            agent_color = agent_color_map.get(player.agent_id, Fore.WHITE)
            color = Fore.BLUE if player.team == "Defending" else Fore.RED
            if player.incognito:
                self.found = True
                print(f"{color}{player.full_name} | {player.team}{Style.RESET_ALL} | {agent_color}{player.agent_id}{Style.RESET_ALL} | Hidden")
            else:
                print(f"{color}{player.full_name} | {player.team}{Style.RESET_ALL} | {agent_color}{player.agent_id}{Style.RESET_ALL} | Not Hidden")
        if not self.found:
            print("No hidden names found")

    def find_team_players(self, local_player, players):
        team_players = []
        
        for player in players:
            if player.team == local_player.team:
                team_players.append(player)
        
        return team_players
    
    def find_party_members(self, party):
        members = []

        for member in party['Members']:
            members.append(member['Subject'].lower())

        return members
