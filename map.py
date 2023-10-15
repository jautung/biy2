import rulehelper as RuleHelper
from mappiece import MapPiece
from movedirection import MoveDirection
from piecetype import PieceType


class Map:
    def __init__(self, number_rows, number_columns, map_pieces: list[MapPiece]):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.map_pieces = map_pieces


    def _get_piece_type_at(self, x, y):
        for map_piece in self.map_pieces:
            if map_piece.x == x and map_piece.y == y:
                return map_piece.piece_type
        return None


    def _generate_rules(self):
        rules = []
        for row_index in range(self.number_rows):
            rules += RuleHelper.generate_rules_for_row([self._get_piece_type_at(x=column_index, y=row_index) for column_index in range(self.number_columns)])
        for column_index in range(self.number_columns):
            rules += RuleHelper.generate_rules_for_row([self._get_piece_type_at(x=column_index, y=row_index) for row_index in range(self.number_rows)])
        return rules


    def execute_move(self, direction: MoveDirection):
        rules = self._generate_rules() # statically freeze rules for entire timestep, even if things move
        self._execute_player_move(direction=direction, rules=rules)
        # TODO execute checks for 'MOVE', 'SINK', 'DEFEAT', each other interaction
        # TODO think about how to handle push


    def _execute_player_move(self, direction: MoveDirection, rules: list[list[PieceType]]):
        piece_types_that_are_you = RuleHelper.get_piece_types_that_are_you(rules)
        for map_piece in self.map_pieces:
            if not any([isinstance(map_piece.piece_type, piece_type_that_is_you) for piece_type_that_is_you in piece_types_that_are_you]):
                continue
            if direction == MoveDirection.UP:
                map_piece.y += 1
            elif direction == MoveDirection.DOWN:
                map_piece.y -= 1
            elif direction == MoveDirection.LEFT:
                map_piece.x -= 1
            elif direction == MoveDirection.RIGHT:
                map_piece.x += 1
            elif direction == MoveDirection.WAIT:
                pass


    def check_for_win(self) -> bool:
        rules = self._generate_rules()
        piece_types_that_are_you = RuleHelper.get_piece_types_that_are_you(rules)
        piece_types_that_are_win = RuleHelper.get_piece_types_that_are_win(rules)
        for row_index in range(self.number_rows):
            for column_index in range(self.number_columns):
                self._get_piece_type_at(x=column_index, y=row_index)
        return False