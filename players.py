from agentmap import agent_map

class Player: 
    def __init__(self, client, p_uuid, agent_id, incognito, team):
        self.client = client
        self.p_uuid = p_uuid
        self.agent_id = self.get_agent_name(agent_id)
        self.incognito = incognito
        self.team = self.teamside(team)
        self.name = self.set_name(p_uuid).split('#')[0]
        self.full_name = self.set_name(p_uuid)
        self.tag = self.set_name(p_uuid).split('#')[1]

    def get_agent_name(self, agent_id):
        if agent_id in agent_map:
            return agent_map[agent_id]
        else:
            print(f"Agent ID {agent_id} not found in agentmap.")
            return "Unknown Agent"

    def teamside(self, color):
        if color == "Blue":
            return "Defending"
        else:
            return "Attacking"
    
    def set_name(self, p_uuid):
        player_data = self.client.put(
            endpoint="/name-service/v2/players", 
            endpoint_type="pd", 
            json_data=[p_uuid]
        )[0]
        return f"{player_data['GameName']}#{player_data['TagLine']}"
