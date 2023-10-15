import piecetypehelper as PieceTypeHelper
import rulehelper as RuleHelper
from mappiece import MapPiece
from movedirection import MoveDirection
from piecetype import PieceType


class Map:
    def __init__(self, number_rows, number_columns, map_pieces: list[MapPiece]):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.map_pieces = map_pieces


    def _get_piece_types_at(self, x, y) -> set[PieceType]:
        piece_types = []
        for map_piece in self.map_pieces:
            if map_piece.x == x and map_piece.y == y:
                piece_types.append(map_piece.piece_type)
        return piece_types


    def _get_word_piece_type_at(self, x, y) -> PieceType:
        piece_types = self._get_piece_types_at(x=x, y=y)
        word_piece_types = list(filter(lambda piece_type: PieceTypeHelper.is_word_piece_type(piece_type), piece_types))
        assert(len(word_piece_types) <= 1)
        if len(word_piece_types) == 0:
            return None
        return word_piece_types[0]


    def _generate_rules(self) -> list[list[PieceType]]:
        rules = []
        for row_index in range(self.number_rows):
            rules += RuleHelper.generate_rules_for_row([self._get_word_piece_type_at(x=column_index, y=row_index) for column_index in range(self.number_columns)])
        for column_index in range(self.number_columns):
            rules += RuleHelper.generate_rules_for_row([self._get_word_piece_type_at(x=column_index, y=row_index) for row_index in range(self.number_rows)])
        return rules


    def execute_move(self, direction: MoveDirection):
        rules = self._generate_rules() # statically freeze rules for entire timestep, even if things move
        self._execute_player_move(direction=direction, rules=rules)
        # TODO execute checks for 'MOVE', 'SINK', 'DEFEAT', each other interaction
        # TODO think about how to handle push


    def _execute_player_move(self, direction: MoveDirection, rules: list[list[PieceType]]):
        piece_types_that_are_you = RuleHelper.get_piece_types_that_are_you(rules)
        for map_piece in self.map_pieces:
            if any([isinstance(map_piece.piece_type, piece_type_that_is_you) for piece_type_that_is_you in piece_types_that_are_you]):
                self._execute_object_move(map_piece=map_piece, direction=direction, rules=rules)


    def _execute_object_move(self, map_piece: MapPiece, direction: MoveDirection, rules: list[list[PieceType]]):
            if direction == MoveDirection.UP and map_piece.y < self.number_rows - 1:
                map_piece.y += 1
            elif direction == MoveDirection.DOWN and map_piece.y > 0:
                map_piece.y -= 1
            elif direction == MoveDirection.LEFT and map_piece.x > 0:
                map_piece.x -= 1
            elif direction == MoveDirection.RIGHT and map_piece.x < self.number_columns - 1:
                map_piece.x += 1
            elif direction == MoveDirection.WAIT:
                pass
            piece_types_in_new_spot = self._get_piece_types_at(x=map_piece.x, y=map_piece.y)
            RuleHelper.get_piece_types_that_are_push(rules=rules)
            # TODO: Do some propagated pushing


    def check_for_win(self) -> bool:
        rules = self._generate_rules()
        piece_types_that_are_you = RuleHelper.get_piece_types_that_are_you(rules)
        piece_types_that_are_win = RuleHelper.get_piece_types_that_are_win(rules)
        for row_index in range(self.number_rows):
            for column_index in range(self.number_columns):
                piece_types = self._get_piece_types_at(x=column_index, y=row_index)
                piece_types_contains_you = any([any([isinstance(piece_type, piece_type_that_is_you) for piece_type_that_is_you in piece_types_that_are_you]) for piece_type in piece_types])
                piece_types_contains_win = any([any([isinstance(piece_type, piece_type_that_is_win) for piece_type_that_is_win in piece_types_that_are_win]) for piece_type in piece_types])
                if piece_types_contains_you and piece_types_contains_win:
                    return True
        return False
