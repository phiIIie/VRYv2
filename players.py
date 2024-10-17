from agentmap import agentmap

class Player: 
    def __init__(self, client, puuid, agentID, incognito, team):
        self.client = client
        self.puuid = puuid
        self.agentID = self.get_agent_name(agentID)
        self.incognito = incognito
        self.team = self.teamside(team)
        self.name = self.set_name(puuid).split('#')[0]
        self.full_name = self.set_name(puuid)
        self.tag = self.set_name(puuid).split('#')[1]

    def get_agent_name(self, agentID):
        if agentID in agentmap:
            return agentmap[agentID]
        else:
            print(f"Agent ID {agentID} not found in agentmap.")
            return "Unknown Agent"

    def teamside(self, color):
        if color == "Blue":
            return "Defending"
        else:
            return "Attacking"
    
    def set_name(self, puuid):
        playerData = self.client.put(
            endpoint="/name-service/v2/players", 
            endpoint_type="pd", 
            json_data=[puuid]
        )[0]
        return f"{playerData['GameName']}#{playerData['TagLine']}"