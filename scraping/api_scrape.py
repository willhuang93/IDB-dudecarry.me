#!/usr/bin/env python3

import requests, json
from time import sleep

player_data = {}
team_data = {}
f = open('output.txt', 'w')

def main():

	global f
	
	players = initial_scrape()

	scrape(players)

	additions = clean()

	while len(additions) != 0:
		scrape(additions)
		additions = clean()

	# print_player()
	# print_team()

	f.write("\n\n\n*********************final data*****************************\n\n\n")
	f.write(player_data + "\n")
	f.write(team_data+"\n")

	f.close()

def initial_scrape():
	global f
	sleep(1.5)
	r = requests.get('https://na.api.pvp.net/api/lol/na/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key=a5b55989-0be8-452f-bc45-2c5265ce99c3')
	data = r.json()
	players = {v["playerOrTeamName"]: v["playerOrTeamId"] for v in data["entries"]}

	return players

def clean(): 
	additions = []
	global player_data
	global team_data

	# 36109721
	for team in team_data:
		for member in team_data[team]["team_roster"]:
			
			url_clean_start = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/"
			url_clean_end = "?api_key=a5b55989-0be8-452f-bc45-2c5265ce99c3"

			url_clean = url_clean_start + str(member) + url_clean_end
			clean_r = request(url_clean)

			clean_data = json.loads(clean_r.text)

			sleep(1.5)
			if clean_data[member]["name"] not in player_data and len(team_data[team]["team_roster"]) > 3:
				team_data[team]["team_roster"].remove(member)
			else:
				additions.append({clean_data[member]["name"] : int(member)})

	return additions


def scrape(players):

	global f

	url_rank_start = "https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/"
	url_rank_end = "/entry?api_key=a5b55989-0be8-452f-bc45-2c5265ce99c3"

	url_score_start = "https://na.api.pvp.net/championmastery/location/NA1/player/"
	url_score_end = "/score?api_key=a5b55989-0be8-452f-bc45-2c5265ce99c3"

	url_topchamp_start = "https://na.api.pvp.net/championmastery/location/NA1/player/"
	url_topchamp_end = "/champions?api_key=a5b55989-0be8-452f-bc45-2c5265ce99c3"

	# https://na.api.pvp.net/api/lol/na/v2.4/team/by-summoner/36109721?api_key=a5b55989-0be8-452f-bc45-2c5265ce99c3
	url_teams_start = "https://na.api.pvp.net/api/lol/na/v2.4/team/by-summoner/"
	url_teams_end = "?api_key=a5b55989-0be8-452f-bc45-2c5265ce99c3"

	global player_data
	global team_data
        	
	for i in players:
		
		p_id = str(players[i])

		url_rank = url_rank_start + p_id + url_rank_end
		url_score = url_score_start + p_id + url_score_end
		url_topchamp = url_topchamp_start + p_id + url_topchamp_end
		url_teams = url_teams_start + p_id + url_teams_end

		rank_r = requests.get(url_rank)
		sleep(1.5)
		score_r = requests.get(url_score)
		sleep(1.5)
		topchamp_r = requests.get(url_topchamp)
		sleep(1.5)
		teams_r = requests.get(url_teams)
		sleep(1.5)

		rank_data = json.loads(rank_r.text.encode('utf-8', 'replace').decode('utf-8', 'replace'))
		score_data = str(score_r.text)
		topchamp_data = json.loads(str(topchamp_r.text))

		###

		rtext = teams_r.text.encode('utf-8', 'replace').decode('utf-8', 'replace)')
		teams_data = json.loads(rtext)

		###

		# rank data
		league = str(rank_data[p_id][0]["name"])
		tier = str(rank_data[p_id][0]["tier"])
		league_pts = int(rank_data[p_id][0]["entries"][0]["leaguePoints"])
		division = str(rank_data[p_id][0]["entries"][0]["division"])
		losses = int(rank_data[p_id][0]["entries"][0]["losses"])
		wins = int(rank_data[p_id][0]["entries"][0]["wins"])
		total_games = losses + wins

		if total_games == 0:
			win_perc = None
		else:
			win_perc = float(float(wins) / float(total_games))


		# champion data
		p_champs = []

		for champ in topchamp_data:
			p_champs.append({"champID" : champ["championId"] , "mastery_score" : champ["championPoints"]})

		p_teams = []

		# team data
		if p_id in teams_data.keys():

			for team in teams_data[p_id]:
				team_wins = int(team["teamStatDetails"][0]["wins"]) + int(team["teamStatDetails"][1]["wins"])
				team_losses = int(team["teamStatDetails"][0]["losses"]) + int(team["teamStatDetails"][1]["losses"])
				team_total_games = team_wins + team_losses

				if team_total_games == 0:
					team_win_perc = None
				else:
					team_win_perc = float(float(team_wins) / float(team_total_games))

				team_roster = []
				team_roster.append(team["roster"]["ownerId"])
				

				for member in team["roster"]["memberList"]:
					team_roster.append(member["playerId"])

				team_dict = { 
					"team_name" : team["name"],
					"fullTeamId" : team["fullId"],
					"team_status" : team["status"],
					"team_tag" : team["tag"],
					"team_lastJoinDate" : team["lastJoinDate"],
					"team_wins" : team_wins,
					"team_losses" : team_losses,
					"team_total_games" : team_total_games,
					"team_win_perc" : team_win_perc,
					"team_roster" : team_roster,
					# "team_match_history" : team["matchHistory"]
				}

				team_data[team_dict["team_name"]] = team_dict.copy()

				p_teams.append(team_dict.copy())

		player_data[i] = {
			"player_id" : p_id,
			"rank" : {"tier" : tier, "division" : division, "league_points" : league_pts},
			"league" : league,
			"wins" : wins,
			"losses" : losses,
			"total_games" : total_games,
			"win_perc" : win_perc,
			"total_mastery_score" : int(score_data),
			"champ_mastery" : p_champs,
			"teams" : p_teams
		}

		f.write(json.dumps(player_data))
		f.write("\n\n" + json.dumps(team_data) + "\n\n\n\n\n\n\n")


# def print_player():
# 	global player_data

# 	for x in player_data:
# 		print("Player Name: " + x)
# 		print("Player ID: " + data[x]["player_id"])
# 		print("Rank: ")
# 		print("\tTier: " + data[x]["rank"]["tier"] + "\tDivision: " + data[x]["rank"]["division"] + "\tLeague Points: " + str(data[x]["rank"]["league_points"]))
# 		print("League Name: " + data[x]["league"])
# 		print("# of Wins: " + str(data[x]["wins"]))
# 		print("# of Losses: " + str(data[x]["losses"]))
# 		print("Total Games: " + str(data[x]["total_games"]))
# 		print("Win Percentage: " + str(data[x]["win_perc"]))
# 		print("Mastery Score: " + str(data[x]["total_mastery_score"]))
# 		print("Champion Masteries: " + str(data[x]["champ_mastery"]))
# 		print("\n")
# 		print("Team Names: " + str(data[x]["teams"]))
# 		print("\n\n\n\n")

# def print_team():
# 	global team_data

# 	for x in team_data:
# 		print("Team Name: " + x)
# 		print("Team ID: " + data[x]["fullTeamId"])
# 		print("Team Status: " + data[x]["team_status"])
# 		print("Team Tag: " + data[x]["team_tag"])
# 		print("Most Recent Member Join Date: " + str(data[x]["team_lastJoinDate"]))
# 		pri7nt("# of Wins: " + str(data[x]["team_wins"]))
# 		print("# of Losses: " + str(data[x]["team_losses"]))
# 		print("Total Games: " + str(data[x]["team_total_games"]))
# 		print("Win Percentage: " + str(data[x]["team_win_perc"]))
# 		print("Roster [Player ID]: ")

# 		for member in data[x]["team_roster"]:
# 			print("\t" + str(member))

# 		print("\n\n\n")

# def json_loads_byteified(json_text):
#     return _byteify(
#         json.loads(json_text, object_hook=_byteify),
#         ignore_dicts=True
#     )


# def _byteify(data, ignore_dicts = False):
#     # if this is a unicode string, return its string representation
#     if isinstance(data, unicode):
#         return data.encode('utf-8')
#     # if this is a list of values, return list of byteified values
#     if isinstance(data, list):
#         return [ _byteify(item, ignore_dicts=True) for item in data ]
#     # if this is a dictionary, return dictionary of byteified keys and values
#     # but only if we haven't already byteified it
#     if isinstance(data, dict) and not ignore_dicts:
#         return {
#             _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
#             for key, value in data.iteritems()
#         }
#     # if it's anything else, return it in its original form
#     return data

if __name__ == "__main__":
    main()
