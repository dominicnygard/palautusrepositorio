from playerReader import PlayerReader
from playerStats import PlayerStats
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

def main():
    console = Console()

    season = Prompt.ask(choices=["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"], default="2024-25")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    print("q to quit")
    nationality = ""
    while True:
        nationality = Prompt.ask(choices=["USA", "FIN", "CAN", "SWE", "CZE", "RUS", "SLO", "FRA", "GBR", "SVK", "DEN", "NED", "AUT", "BLR", "GER", "SUI", "NOR", "UZB", "LAT", "AUS", "q"])
        if nationality == "q":
            break
        players = stats.top_scorers_by_nationality(nationality=nationality)


        table = Table(title=f"Season {season} players from {nationality}")
        table.add_column("Name", style="cyan")
        table.add_column("Teams", style="magenta")
        table.add_column("Goals", style="green")
        table.add_column("Assists", style="green")
        table.add_column("Points", style="green")
        for player in players:
            table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.points))

        
        console.print(table)

if __name__ == "__main__":
    main()
