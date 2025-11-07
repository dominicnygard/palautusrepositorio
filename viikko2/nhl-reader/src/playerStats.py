from playerReader import PlayerReader

class PlayerStats:
    def __init__(self, reader):
        self.players = reader.players

    def top_scorers_by_nationality(self, nationality):
        def nationality_filter(x):
            if x.nationality == nationality:
                return True
            else:
                return False
            
        return sorted(filter(nationality_filter, self.players), key=lambda player: player.points, reverse=True)
    
