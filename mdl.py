import urllib.request
import json

"""displays the top 10 on Deadman's MDL"""
mdl_url = "http://md-ladder.cloudapp.net/api/v1.0/players/?topk=10"

content = urllib.request.urlopen(mdl_url).read()

data = json.loads(content)
print("Deadman's Multi-Day Ladder Top 10")
print("=================================")
current_player = 1
for index, player in enumerate(data['players']):
    # once we have the players, start printing out each of the top 10
    print(str(current_player) + ") " + player['player_name'] + " " + str(player['displayed_rating']))
    current_player += 1

