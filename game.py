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
                print(f"{player.full_name} - {player.team} {player.agent} - {player.teamID}")
        if not self.found:
            print("No hidden names found")