import csv

def to_int(value):
    if value == "" or value is None:
        return 0
    return int(value.replace(",", ""))

def to_float(value):
    if value == "" or value is None:
        return 0.0
    return float(value)

def read_csv(file_name):
    players = []
    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            player = {
                "Player": row[1],
                "GP": to_int(row[2]),
                "MIN": to_int(row[3]),
                "PTS": to_int(row[4]),
                "FGM": to_int(row[5]),
                "FGA": to_int(row[6]),
                "FG%": to_float(row[7]),
                "3PM": to_int(row[8]),
                "3PA": to_int(row[9]),
                "3P%": to_float(row[10]),
                "FTM": to_int(row[11]),
                "FTA": to_int(row[12]),
                "FT%": to_float(row[13]),
                "OREB": to_int(row[14]),
                "DREB": to_int(row[15]),
                "REB": to_int(row[16]),
                "AST": to_int(row[17]),
                "STL": to_int(row[18]),
                "BLK": to_int(row[19]),
                "TOV": to_int(row[20]),
                "eFG%": to_float(row[21]),
                "TS%": to_float(row[22]),
            }
            players.append(player)
    return players

def calculate_per_game(player):
    if player["GP"] == 0:
        player["PTS_per_game"] = 0
        player["REB_per_game"] = 0
        player["AST_per_game"] = 0
        player["STL_per_game"] = 0
        player["BLK_per_game"] = 0
        player["TOV_per_game"] = 0
    else:
        player["PTS_per_game"] = player["PTS"] / player["GP"]
        player["REB_per_game"] = player["REB"] / player["GP"]
        player["AST_per_game"] = player["AST"] / player["GP"]
        player["STL_per_game"] = player["STL"] / player["GP"]
        player["BLK_per_game"] = player["BLK"] / player["GP"]
        player["TOV_per_game"] = player["TOV"] / player["GP"]

def points_score(player):
    return player["PTS_per_game"]

def reb_ast_score(player):
    return player["REB_per_game"] + player["AST_per_game"]

def defense_score(player):
    return player["STL_per_game"] + player["BLK_per_game"]

def overall_goat_score(player):
    return (
        player["PTS_per_game"] * 0.4 +
        player["REB_per_game"] * 0.3 +
        player["AST_per_game"] * 0.3 +
        player["STL_per_game"] * 1.5 +
        player["BLK_per_game"] * 1.5 -
        player["TOV_per_game"] * 0.5
    )

def sort_players(players, score_function):
    n = len(players)
    for player in players:
        player["Score"] = score_function(player)
    for i in range(n):
        for j in range(0, n-i-1):
            if players[j]["Score"] < players[j+1]["Score"]:
                players[j], players[j+1] = players[j+1], players[j]

def display_top(players, top_n=10):
    print(f"\nTop {top_n} Players:")
    print("Rank | Player | Score")
    for i in range(top_n):
        player = players[i]
        print(f"{i+1}. {player['Player']} - {round(player['Score'], 2)}")

def write_ranking_csv(players, file_name="nba_ranking.csv"):
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Rank", "Player", "GP", "PTS", "PTS_per_game",
            "REB", "REB_per_game", "AST", "AST_per_game",
            "STL", "STL_per_game", "BLK", "BLK_per_game",
            "TOV", "TOV_per_game", "Score"
        ])
        for i, player in enumerate(players):
            writer.writerow([
                i+1,
                player["Player"],
                player["GP"],
                player["PTS"],
                round(player["PTS_per_game"], 2),
                player["REB"],
                round(player["REB_per_game"], 2),
                player["AST"],
                round(player["AST_per_game"], 2),
                player["STL"],
                round(player["STL_per_game"], 2),
                player["BLK"],
                round(player["BLK_per_game"], 2),
                player["TOV"],
                round(player["TOV_per_game"], 2),
                round(player["Score"], 2)
            ])

def extra_analysis(players):
    high_scorers = sum(1 for p in players if p["PTS_per_game"] >= 25)
    top_rebounders = sum(1 for p in players if p["REB_per_game"] >= 10)
    top_assisters = sum(1 for p in players if p["AST_per_game"] >= 5)
    print(f"\nPlayers averaging 25+ PPG: {high_scorers}")
    print(f"Players averaging 10+ RPG: {top_rebounders}")
    print(f"Players averaging 5+ AST per game: {top_assisters}")

def main():
    csv_file = "alltimeleaders.csv"
    players = read_csv(csv_file)
    for player in players:
        calculate_per_game(player)

    print("Welcome to the NBA Stats Analyzer!")
    print("Choose ranking method:")
    print("1. Points per game")
    print("2. Rebounds + Assists per game")
    print("3. Defense (Steals + Blocks per game)")
    print("4. Overall GOAT score")

    choice = input("Enter 1,2,3 or 4: ")
    if choice == "1":
        sort_players(players, points_score)
    elif choice == "2":
        sort_players(players, reb_ast_score)
    elif choice == "3":
        sort_players(players, defense_score)
    else:
        sort_players(players, overall_goat_score)

    display_top(players, 10)
    extra_analysis(players)
    write_ranking_csv(players)
    print("\nFull ranking saved to nba_ranking.csv")

if __name__ == "__main__":
    main()
