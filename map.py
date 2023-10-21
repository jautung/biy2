from typing import Type

import piecepositionhelper as PiecePositionHelper
import rulehelper as RuleHelper
from mappiece import MapPiece
from movedirection import MoveDirection
from piecetype import *
from pieceposition import PiecePosition


# Note that (0, 0) is the bottom left corner
class Map:
    def __init__(self, number_rows, number_columns, map_pieces: list[MapPiece]):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.map_pieces = map_pieces


    def _get_map_pieces_at(self, position: PiecePosition) -> set[MapPiece]:
        map_pieces = []
        for map_piece in self.map_pieces:
            if map_piece.position == position:
                map_pieces.append(map_piece)
        return map_pieces


    def _get_piece_types_at(self, position: PiecePosition) -> set[PieceType]:
        return [map_piece.piece_type for map_piece in self._get_map_pieces_at(position=position)]


    def _get_text_piece_type_at(self, position: PiecePosition) -> TextPieceType:
        piece_types = self._get_piece_types_at(position=position)
        text_piece_types = list(filter(lambda piece_type: isinstance(piece_type, TextPieceType), piece_types))
        assert(len(text_piece_types) <= 1) # There can never be more than 1 text piece at a given position
        if len(text_piece_types) == 0:
            return None
        return text_piece_types[0]


    def _generate_rules(self) -> list[list[TextPieceType]]:
        rules: list[list[TextPieceType]] = []
        # By default, without any overrides, "TEXT IS PUSH" is always a rule
        rules.append([TextTextPieceType(), IsTextPieceType(), PushTextPieceType()])
        for row_index in range(self.number_rows):
            rules += RuleHelper.generate_rules_for_row([self._get_text_piece_type_at(PiecePosition(x=column_index, y=row_index)) for column_index in range(self.number_columns)])
        for column_index in range(self.number_columns):
            rules += RuleHelper.generate_rules_for_row([self._get_text_piece_type_at(PiecePosition(x=column_index, y=row_index)) for row_index in reversed(range(self.number_rows))]) # Reversed because (0, 0) is the bottom left corner
        return rules


    def execute_move(self, direction: MoveDirection):
        rules = self._generate_rules() # statically freeze rules for entire timestep, even if things move
        self._execute_player_move(direction=direction, rules=rules)
        # TODO execute mutations of e.g. NOUN IS NOUN
        # TODO execute checks for 'MOVE', 'SINK', 'DEFEAT', each other interaction


    def _execute_player_move(self, direction: MoveDirection, rules: list[list[TextPieceType]]):
        object_piece_types_that_are_you = RuleHelper.get_object_piece_types_that_are_you(rules)
        for map_piece in self.map_pieces:
            if self._is_piece_type_within_object_piece_types(
                piece_type=map_piece.piece_type,
                object_piece_types=object_piece_types_that_are_you
            ):
                self._execute_object_move(map_piece=map_piece, direction=direction, rules=rules)


    def _execute_object_move(self, map_piece: MapPiece, direction: MoveDirection, rules: list[list[TextPieceType]]):
        if not self._can_object_move(map_piece=map_piece, direction=direction, rules=rules):
            return
        new_position = PiecePositionHelper.get_position_after_move(position=map_piece.position, direction=direction)
        map_piece.position = new_position
        map_pieces_in_new_position_that_are_push = self._get_map_pieces_in_position_that_are_push(position=new_position, rules=rules)
        for map_piece in map_pieces_in_new_position_that_are_push:
            self._execute_object_move(map_piece=map_piece, direction=direction, rules=rules)


    def _can_object_move(self, map_piece: MapPiece, direction: MoveDirection, rules: list[list[TextPieceType]]) -> bool:
        # TODO: Check is map_piece is 'STOP' and if so, return False
        new_position = PiecePositionHelper.get_position_after_move(position=map_piece.position, direction=direction)
        if not self._can_object_enter_position(position=new_position, rules=rules):
            return False
        map_pieces_in_new_position_that_are_push = self._get_map_pieces_in_position_that_are_push(position=new_position, rules=rules)
        return all(
            [self._can_object_move(map_piece=map_piece, direction=direction, rules=rules) for map_piece in map_pieces_in_new_position_that_are_push]
        )


    def _get_map_pieces_in_position_that_are_push(self, position: PiecePosition, rules: list[list[TextPieceType]]) -> list[MapPiece]:
        map_pieces_in_new_position = self._get_map_pieces_at(position=position)
        object_piece_types_that_are_push = RuleHelper.get_object_piece_types_that_are_push(rules=rules)
        return list(filter(
            lambda map_piece: self._is_piece_type_within_object_piece_types(
                piece_type=map_piece.piece_type,
                object_piece_types=object_piece_types_that_are_push
            ), map_pieces_in_new_position
        ))


    def _can_object_enter_position(self, position: PiecePosition, rules: list[list[TextPieceType]]) -> bool:
        if position.x < 0:
            return False
        if position.y < 0:
            return False
        if position.x >= self.number_columns:
            return False
        if position.y >= self.number_rows:
            return False
        # TODO: Check for 'STOP' pieces in position and if so, return False
        return True


    def check_for_win(self) -> bool:
        rules = self._generate_rules()
        object_piece_types_that_are_you = RuleHelper.get_object_piece_types_that_are_you(rules)
        object_piece_types_that_are_win = RuleHelper.get_object_piece_types_that_are_win(rules)
        for row_index in range(self.number_rows):
            for column_index in range(self.number_columns):
                piece_types = self._get_piece_types_at(PiecePosition(x=column_index, y=row_index))
                piece_types_contains_you = any([self._is_piece_type_within_object_piece_types(piece_type=piece_type, object_piece_types=object_piece_types_that_are_you) for piece_type in piece_types])
                piece_types_contains_win = any([self._is_piece_type_within_object_piece_types(piece_type=piece_type, object_piece_types=object_piece_types_that_are_win) for piece_type in piece_types])
                if piece_types_contains_you and piece_types_contains_win:
                    return True
        return False


    def _is_piece_type_within_object_piece_types(self, piece_type: PieceType, object_piece_types: list[Type[ObjectPieceType]]) -> bool:
        return any([isinstance(piece_type, object_piece_type) for object_piece_type in object_piece_types])
