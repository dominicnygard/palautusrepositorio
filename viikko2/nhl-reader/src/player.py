class Player:
    def __init__(self, player):
        self.nationality = player['nationality']
        self.name = player['name']
        self.team = player['team']
        self.goals = player['goals']
        self.assists = player['assists']
        self.points = self.goals + self.assists



    def __str__(self):
        return f"{self.name:20} team {self.team:20} {self.goals} + {self.assists} = {self.points}"
