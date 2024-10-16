import requests

agentmap = [] 
def get_agents_from_api():
    apiurl = "https://valorant-api.com/v1/agents"
    response = requests.get(apiurl)
    
    if response.status_code == 200:
        agents = response.json()["data"]
        for agent in agents:
            agentmap.append({
                "uuid": agent["uuid"],
                "displayName": agent["displayName"]
            })
    else:
        print("Failed to retrieve agents")

    return agentmap

agents_list = get_agents_from_api()
print(agents_list)