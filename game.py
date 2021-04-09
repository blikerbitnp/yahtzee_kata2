from typing import Iterable, List, Dict

from main import ndice
import categories
import uuid

class Dices:
    def __init__(self):
        self.total_dice = 5
        self.dices = {i: {"value": 0, "freezed": False} for i in range(self.total_dice)}

    def dice_values(self):
        return [self.dices[i]["value"] for i in self.dices]

    def roll(self):
        nums = ndice(self.total_dice)
        for i in self.dices:
            if self.dices[i]["freezed"] == False:
                self.dices[i]["value"] = nums[i]
        return self.dice_values()

    def freeze_dices(self, dice_numbers: List[int]):
        for i in dice_numbers:
            self.freeze_dice(i)

    def freeze_dice(self, dice_number: int):
        self.dices[dice_number]["freezed"] = True

    def unfreeze_dice(self, dice_number: int):
        self.dices[dice_number]['freezed'] = False


from exceptions import *





class Score:
    def __init__(self, name:str="A"):
        self.name = name
        self.upper = ["aces", "two", "threes", "fours", "fives", "sixes"]
        self.lower = ["three of a kind", "four of a kind", "full house", "small straight", "large straight", "yahtzee",
                      "chance"]
        self.upper_score_bonus_point = 63
        self.upper_score_bonus = 35
        self.score_dict = {field: None for field in self.upper}
        self.score_dict.update({field: None for field in self.lower})
        self.allowed_keys = self.score_dict.keys()

    def cal_score(self) -> int:
        return sum(self.score_dict.values()) + self.cal_upper_bonus()

    def cal_upper_bonus(self) -> int:
        if sum([self.score_dict[i] for i in self.upper]) > self.upper_score_bonus_point:
            return 35
        else:
            return 0

    def get_eligble_fields(self) -> List[int]:
        return [i for i in self.score_dict if self.score_dict[i] is None]

    def get_score(self) -> int:
        return {i: 0 if j is None else j for i, j in self.score_dict.items()}

    def _override_score(self, key, value):
        self.score_dict[key] = value

    def __setitem__(self, key:str, value:Player):
        """

        :type value: Player
        """
        if key in self.allowed_keys:
            if self.score_dict[key] is not None:
                raise AlreadyUsedField(f"{key} value already set to {self.score_dict[key]}")
            self.score_dict[key] = value
        else:
            raise KeyNotAllowed(f" {key} : not allowed, choose one from {' ,'.join(self.allowed_keys)}")

    def __getitem__(self, item) -> Dict[str, int]:
        return self.score_dict[item]

    def get_possible_score(self, dices: int):
        possible_score = {
            "yahtzee": categories.yahtzee(dices),
            "three of a kind": categories.three_of_a_kind(dices),
            "four of a kind": categories.four_of_a_kind(dices),
            "large straight": categories.large_straight(dices),
            "small straight": categories.small_straight(dices),
            "chance": categories.chance(dices),
            "full house": categories.full_house(dices),
        }

        possible_score.update(
            {
                self.upper[i]: categories.n_of_kind(dices, i + 1)
                for i in range(len(self.upper))
            })
        return possible_score

    def __repr__(self):
        string = ""
        for i in self.score_dict:
            string += (
                f"{i} : {self.score_dict[i] if self.score_dict[i] is not None else 0}\n"
            )
        string += f"total score : {self.cal_score()}"
        return string


class Game:
    def __init__(self, players=None):
        if players is None:
            players = [1]
        self.dice = Dices()
        self.players: Dict[str,Player] = {}
        for name in players:
            player = Player(str(name))
            self.players.update( (player.uid, player ) )
        self.player_game = []
        self.final_score =None
        self.game_status = False

    def __getitem__(self, item):
        return self.players[item]

    def __setitem__(self, key, value):
        if isinstance(value,Player) and self.game_status==False:
            self.players[key] = value
    def start_game(self):
        self.game_status="started"

    def finish_game(self):
        if self.final_score is None:
            self.final_score ={}
            for player in self.players:
                this_player= self.players[player]
                self.final_score[this_player.uid] = this_player.get_score()

            self.game_status = "completed"


    def announce_winner(self):
        winner = max(self.final_score,key=self.final_score.get)
        return   f"winner is {self.players[winner].player_name} with score:  {self.players[winner].get_score()}"


class Player(Game):

    def __init__(self,name:str):
        self.player_name = name
        self.uid = str(uuid.uuid4())
        super(Player, self).__init__()
        self.round = [0, 0]
        self.score = Score()

    def finish_round(self, score_type):
        if self.round[0] > 12:
            raise AllRoundsCompleted(f"All rounds completed. Player score is {self.get_score()}")
        self.score[score_type] = self.score.get_possible_score()[score_type]
        self.round[0] += 1


    def roll_dice(self):
        if self.round[1] > 2:
            raise SequencesFinished(f"All rolls completed for this round. Choose a score category to finish the round")
        else:
            self.player_dice = self.dice.roll()

        return self.player_dice

    def get_score(self):
        return self.score.get_score()


