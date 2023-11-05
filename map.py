from collections.abc import Callable
from typing import Type, TypeVar

T = TypeVar("T")

import movedirectionhelper as MoveDirectionHelper
import nounmutationhelper as NounMutationHelper
import piecepositionhelper as PiecePositionHelper
import rulegenerationhelper as RuleGenerationHelper
import rulereadinghelper as RuleReadingHelper
from mappiece import MapPiece
from movedirection import MoveDirection
from piecetype import *
from pieceposition import PiecePosition
from rule import Rule


# Note that (0, 0) is the bottom left corner
class Map:
    def __init__(self, number_rows, number_columns, map_pieces: set[MapPiece]):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.map_pieces = map_pieces
        # Prevent responding to repeated keystrokes before the current computation is finished
        self.execute_move_locked = False

    def _get_map_pieces_at(self, position: PiecePosition) -> set[MapPiece]:
        map_pieces = []
        for map_piece in self.map_pieces:
            if map_piece.position == position:
                map_pieces.append(map_piece)
        return map_pieces

    def _get_piece_types_at(self, position: PiecePosition) -> set[PieceType]:
        return set(
            [
                map_piece.piece_type
                for map_piece in self._get_map_pieces_at(position=position)
            ]
        )

    def _get_text_piece_type_at(self, position: PiecePosition) -> TextPieceType:
        piece_types = self._get_piece_types_at(position=position)
        text_piece_types = list(
            filter(
                lambda piece_type: isinstance(piece_type, TextPieceType), piece_types
            )
        )
        assert (
            len(text_piece_types) <= 1
        )  # There can never be more than 1 text piece at a given position
        if len(text_piece_types) == 0:
            return None
        return text_piece_types[0]

    def _generate_rules(self) -> set[Rule]:
        rules = self._generate_results_for_all_rows_and_columns(
            generate_from_row=RuleGenerationHelper.generate_rules_for_row
        )
        # By default, "TEXT IS PUSH" is always a rule
        rules.add(
            Rule(
                text_piece_types=[
                    TextTextPieceType(),
                    IsTextPieceType(),
                    PushTextPieceType(),
                ]
            )
        )
        return rules

    def print_rules(self):
        rules = self._generate_rules()
        print("Rules:")
        for rule in rules:
            print(f"* {rule}")
        print()

    def execute_move(self, direction: MoveDirection):
        if self.execute_move_locked:
            print("Excuse me, please stop mashing the keyboard!!!")
            return
        self.execute_move_locked = True
        # Statically freeze rules for entire timestep, even if things move
        rules = self._generate_rules()
        self._execute_player_move(direction=direction, rules=rules)
        self._execute_npc_move(rules=rules)
        self._execute_shifts(rules=rules)
        # TODO Figure out what the actual order of operations of these are in-game
        # I'm 80% sure that we freeze new rules to calculate these after movement, but I could be mistaken
        rules = self._generate_rules()
        self._apply_defeat_interactions(rules=rules)
        self._apply_sink_interactions(rules=rules)
        self._apply_melt_interactions(rules=rules)
        self._apply_open_close_interactions(rules=rules)
        self._apply_noun_mutations()
        self.execute_move_locked = False

    def _execute_player_move(self, direction: MoveDirection, rules: set[Rule]):
        object_piece_types_that_are_you = (
            RuleReadingHelper.get_object_piece_types_that_are_you(rules=rules)
        )
        for map_piece in self.map_pieces:
            if self._is_piece_type_within_object_piece_types(
                piece_type=map_piece.piece_type,
                object_piece_types=object_piece_types_that_are_you,
            ):
                self._execute_object_move(
                    map_piece=map_piece, direction=direction, rules=rules
                )

    def _execute_npc_move(self, rules: set[Rule]):
        object_piece_types_that_are_move = (
            RuleReadingHelper.get_object_piece_types_that_are_move(rules=rules)
        )
        for map_piece in self.map_pieces:
            if self._is_piece_type_within_object_piece_types(
                piece_type=map_piece.piece_type,
                object_piece_types=object_piece_types_that_are_move,
            ):
                assert map_piece.direction != MoveDirection.WAIT
                if not self._can_object_move(
                    map_piece=map_piece, direction=map_piece.direction, rules=rules
                ):
                    map_piece.direction = MoveDirectionHelper.reverse_direction(
                        map_piece.direction
                    )
                self._execute_object_move(
                    map_piece=map_piece, direction=map_piece.direction, rules=rules
                )

    def _execute_shifts(self, rules: set[Rule]):
        # TODO for shift
        pass

    def _execute_object_move(
        self,
        map_piece: MapPiece,
        direction: MoveDirection,
        rules: set[Rule],
    ):
        if direction == MoveDirection.WAIT:
            return
        if not self._can_object_move(
            map_piece=map_piece, direction=direction, rules=rules
        ):
            return
        new_position = PiecePositionHelper.get_position_after_move(
            position=map_piece.position, direction=direction
        )
        for pushable_map_piece in self._get_map_pieces_in_position_that_are_push(
            position=new_position, rules=rules
        ):
            self._execute_object_move(
                map_piece=pushable_map_piece, direction=direction, rules=rules
            )
        map_piece.position = new_position
        map_piece.direction = direction

    def _can_object_move(
        self,
        map_piece: MapPiece,
        direction: MoveDirection,
        rules: set[Rule],
    ) -> bool:
        if self._is_piece_type_within_object_piece_types(
            piece_type=map_piece.piece_type,
            object_piece_types=RuleReadingHelper.get_object_piece_types_that_are_stop(
                rules=rules
            ),
        ):
            return False
        new_position = PiecePositionHelper.get_position_after_move(
            position=map_piece.position, direction=direction
        )
        if not self._can_object_enter_position(position=new_position, rules=rules):
            return False
        map_pieces_in_new_position_that_are_push = (
            self._get_map_pieces_in_position_that_are_push(
                position=new_position, rules=rules
            )
        )
        return all(
            [
                self._can_object_move(
                    map_piece=map_piece, direction=direction, rules=rules
                )
                for map_piece in map_pieces_in_new_position_that_are_push
            ]
        )

    def _get_map_pieces_in_position_that_are_push(
        self, position: PiecePosition, rules: set[Rule]
    ) -> set[MapPiece]:
        map_pieces_in_new_position = self._get_map_pieces_at(position=position)
        object_piece_types_that_are_push = (
            RuleReadingHelper.get_object_piece_types_that_are_push(rules=rules)
        )
        return set(
            list(
                filter(
                    lambda map_piece: self._is_piece_type_within_object_piece_types(
                        piece_type=map_piece.piece_type,
                        object_piece_types=object_piece_types_that_are_push,
                    ),
                    map_pieces_in_new_position,
                )
            )
        )

    def _can_object_enter_position(
        self, position: PiecePosition, rules: set[Rule]
    ) -> bool:
        if position.x < 0:
            return False
        if position.y < 0:
            return False
        if position.x >= self.number_columns:
            return False
        if position.y >= self.number_rows:
            return False
        if self._has_map_piece_in_position_that_is_stop(position=position, rules=rules):
            return False
        return True

    def _has_map_piece_in_position_that_is_stop(
        self, position: PiecePosition, rules: set[Rule]
    ) -> bool:
        object_piece_types_that_are_stop = (
            RuleReadingHelper.get_object_piece_types_that_are_stop(rules=rules)
        )
        return any(
            [
                self._is_piece_type_within_object_piece_types(
                    piece_type=map_piece.piece_type,
                    object_piece_types=object_piece_types_that_are_stop,
                )
                for map_piece in self._get_map_pieces_at(position=position)
            ]
        )

    def _apply_defeat_interactions(self, rules: set[Rule]):
        overlapping_map_pieces = (
            self._get_all_overlapping_map_pieces_between_object_piece_types(
                object_piece_types_1=RuleReadingHelper.get_object_piece_types_that_are_you(
                    rules
                ),
                object_piece_types_2=RuleReadingHelper.get_object_piece_types_that_are_defeat(
                    rules
                ),
            )
        )
        for overlapping_map_pieces_that_are_you, _ in overlapping_map_pieces:
            for map_piece in overlapping_map_pieces_that_are_you:
                self._remove_map_piece(map_piece=map_piece)

    def _apply_sink_interactions(self, rules: set[Rule]):
        # TODO: Handle negation here so that floating objects do not sink
        overlapping_map_pieces = (
            self._get_all_overlapping_map_pieces_between_object_piece_types(
                object_piece_types_1=RuleReadingHelper.get_object_piece_types_that_are_sink(
                    rules
                ),
                object_piece_types_2=[ObjectPieceType],
            )
        )
        for (
            overlapping_map_pieces_that_are_sink,
            overlapping_map_pieces_to_be_sunk,
        ) in overlapping_map_pieces:
            # TODO: Figure out the real in-game logic for multiple pieces sinking simultaneously; for now, sinking everything
            # Only sink if there are map pieces to be sunk that are not themselves sink
            should_apply_sink = (
                len(
                    overlapping_map_pieces_to_be_sunk.difference(
                        overlapping_map_pieces_that_are_sink
                    )
                )
                > 0
            )
            if not should_apply_sink:
                continue
            for map_piece in overlapping_map_pieces_that_are_sink:
                self._remove_map_piece(map_piece=map_piece)
            for map_piece in overlapping_map_pieces_to_be_sunk:
                self._remove_map_piece(map_piece=map_piece)

    def _apply_melt_interactions(self, rules: set[Rule]):
        # TODO for melt
        pass

    def _apply_open_close_interactions(self, rules: set[Rule]):
        # TODO for open close
        pass

    def _remove_map_piece(self, map_piece: MapPiece):
        if map_piece in self.map_pieces:
            self.map_pieces.remove(map_piece)

    def _apply_noun_mutations(self):
        noun_mutations = self._generate_results_for_all_rows_and_columns(
            generate_from_row=NounMutationHelper.generate_noun_mutations_for_row
        )
        for noun_mutation in noun_mutations:
            for map_piece in self.map_pieces:
                if isinstance(
                    map_piece.piece_type, noun_mutation.from_object_piece_type
                ):
                    map_piece.piece_type = noun_mutation.to_object_piece_type()

    def is_in_win_state(self) -> bool:
        rules = self._generate_rules()
        overlapping_map_pieces = (
            self._get_all_overlapping_map_pieces_between_object_piece_types(
                object_piece_types_1=RuleReadingHelper.get_object_piece_types_that_are_you(
                    rules
                ),
                object_piece_types_2=RuleReadingHelper.get_object_piece_types_that_are_win(
                    rules
                ),
            )
        )
        return len(overlapping_map_pieces) > 0

    def _get_all_overlapping_map_pieces_between_object_piece_types(
        self,
        object_piece_types_1: set[Type[ObjectPieceType]],
        object_piece_types_2: set[Type[ObjectPieceType]],
    ) -> set[tuple[frozenset[MapPiece], frozenset[MapPiece]]]:
        overlaps: set[tuple[frozenset[MapPiece], frozenset[MapPiece]]] = set()
        for row_index in range(self.number_rows):
            for column_index in range(self.number_columns):
                map_pieces = self._get_map_pieces_at(
                    position=PiecePosition(x=column_index, y=row_index)
                )
                map_pieces_matching_1 = frozenset(
                    [
                        map_piece
                        for map_piece in map_pieces
                        if self._is_piece_type_within_object_piece_types(
                            piece_type=map_piece.piece_type,
                            object_piece_types=object_piece_types_1,
                        )
                    ]
                )
                map_pieces_matching_2 = frozenset(
                    [
                        map_piece
                        for map_piece in map_pieces
                        if self._is_piece_type_within_object_piece_types(
                            piece_type=map_piece.piece_type,
                            object_piece_types=object_piece_types_2,
                        )
                    ]
                )
                if len(map_pieces_matching_1) > 0 and len(map_pieces_matching_2) > 0:
                    overlaps.add((map_pieces_matching_1, map_pieces_matching_2))
        return overlaps

    def _generate_results_for_all_rows_and_columns(
        self, generate_from_row: Callable[[list[PieceType]], set[T]]
    ) -> set[T]:
        results: set[T] = set()
        for row_index in range(self.number_rows):
            results.update(
                generate_from_row(
                    row=[
                        self._get_text_piece_type_at(
                            position=PiecePosition(x=column_index, y=row_index)
                        )
                        for column_index in range(self.number_columns)
                    ]
                )
            )
        for column_index in range(self.number_columns):
            results.update(
                generate_from_row(
                    row=[
                        self._get_text_piece_type_at(
                            position=PiecePosition(x=column_index, y=row_index)
                        )
                        # Reversed because (0, 0) is the bottom left corner
                        for row_index in reversed(range(self.number_rows))
                    ]
                )
            )
        return results

    def _is_piece_type_within_object_piece_types(
        self, piece_type: PieceType, object_piece_types: set[Type[ObjectPieceType]]
    ) -> bool:
        return any(
            [
                isinstance(piece_type, object_piece_type)
                for object_piece_type in object_piece_types
            ]
        )
