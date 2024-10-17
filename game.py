class Game:
    def __init__(self, party, matchID, players, localPlayer):
        self.matchID = matchID
        self.players = players
        self.localPlayer = localPlayer
        self.teamPlayers = self.find_team_players(self.localPlayer, self.players)
        self.partyPlayers = self.find_party_members(party)
    
    def find_hidden_names(self, players):
        self.found = True
        for player in players:
            if (player.incognito):
                self.found = True
                print(f"{player.full_name} - {player.team} {player.agentID}" + "Name is hidden")
            else:
                print(f"{player.full_name} - {player.team} {player.agentID}" + "Name is not hidden")
        if not self.found:
            print("No hidden names found")

    def find_team_players(self, localPlayer, players):
        team_players = []
        
        for player in players:
            if (player.team == localPlayer.team):
                team_players.append(player)
        
        return team_players
    
    def find_party_members(self, party):
        members = []

        for member in party['Members']:
            members.append(member['Subject'].lower())

        return members