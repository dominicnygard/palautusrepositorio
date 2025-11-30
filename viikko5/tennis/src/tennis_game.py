class TennisGame:
    MINIMUM_SCORE_TO_WIN = 4
    SCORE_DIFFERENCE_FOR_WIN = 2
    SCORE_DIFFERENCE_FOR_ADVANTAGE = 1

    SCORE_NAMES = {
        0: "Love",
        1: "Fifteen",
        2: "Thirty",
        3: "Forty"
    }

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1

    def get_score(self):
        if self._is_scores_equal():
            return self._get_equal_score()
        elif self._is_deuce_or_advantage():
            return self._get_deuce_or_advantage_score()
        else:
            return self._get_regular_score()

    def _is_scores_equal(self):
        return self.player1_score == self.player2_score

    def _is_deuce_or_advantage(self):
        return self.player1_score >= self.MINIMUM_SCORE_TO_WIN or self.player2_score >= self.MINIMUM_SCORE_TO_WIN

    def _get_equal_score(self):
        if self.player1_score < 3:
            return f"{self.SCORE_NAMES[self.player1_score]}-All"
        else:
            return "Deuce"

    def _get_deuce_or_advantage_score(self):
        score_difference = self.player1_score - self.player2_score

        if score_difference == self.SCORE_DIFFERENCE_FOR_ADVANTAGE:
            return "Advantage player1"
        elif score_difference == -self.SCORE_DIFFERENCE_FOR_ADVANTAGE:
            return "Advantage player2"
        elif score_difference >= self.SCORE_DIFFERENCE_FOR_WIN:
            return "Win for player1"
        elif score_difference <= -self.SCORE_DIFFERENCE_FOR_WIN:
            return "Win for player2"

    def _get_regular_score(self):
        player1_score_name = self._convert_score_to_name(self.player1_score)
        player2_score_name = self._convert_score_to_name(self.player2_score)
        return f"{player1_score_name}-{player2_score_name}"

    def _convert_score_to_name(self, score):
        return self.SCORE_NAMES.get(score, "Forty")
