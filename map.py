from collections.abc import Callable
from typing import Type, TypeVar

T = TypeVar("T")

import movedirectionhelper as MoveDirectionHelper
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
        # There can never be more than 1 text piece at a given position
        assert len(text_piece_types) <= 1
        if len(text_piece_types) == 0:
            return None
        return text_piece_types[0]

    def _generate_rules(self) -> set[Rule]:
        on_map_rules = self._generate_results_for_all_rows_and_columns(
            generate_from_row=RuleGenerationHelper.generate_rules_for_row
        )
        return RuleGenerationHelper.get_final_rules_from_all_on_map_rules(
            on_map_rules=on_map_rules
        )

    def print_rules(self):
        rules = self._generate_rules()
        print("Rules:")
        for rule in rules:
            print(f"* {rule}")
        print()

    def _generate_simplified_rules(self) -> set[Rule]:
        return RuleReadingHelper.simplify_rules(rules=self._generate_rules())

    def print_simplified_rules(self):
        simplified_rules = self._generate_simplified_rules()
        print("Simplified Rules:")
        for simplified_rule in simplified_rules:
            print(f"* {simplified_rule}")
        print()

    def execute_move(self, direction: MoveDirection):
        if self.execute_move_locked:
            print("Excuse me, please stop mashing the keyboard!!!")
            return
        self.execute_move_locked = True
        # Statically freeze rules for entire timestep, even if things move
        # TODO: Check if this is actually true in the game!
        simplified_rules = self._generate_simplified_rules()
        # TODO: Figure out real in-game order of operations when player and npc moves to the same square
        self._execute_player_move(
            direction=direction, simplified_rules=simplified_rules
        )
        self._execute_npc_move(simplified_rules=simplified_rules)
        self._execute_shifts(simplified_rules=simplified_rules)
        # TODO: Figure out what the actual order of operations of these are in-game
        # I'm 80% sure that we freeze new rules to calculate these after movement, but I could be mistaken
        simplified_rules = self._generate_simplified_rules()
        self._apply_defeat_interactions(simplified_rules=simplified_rules)
        self._apply_sink_interactions(simplified_rules=simplified_rules)
        self._apply_hot_melt_interactions(simplified_rules=simplified_rules)
        self._apply_open_close_interactions(simplified_rules=simplified_rules)
        self._apply_noun_mutations(simplified_rules=simplified_rules)
        self.execute_move_locked = False

    def _execute_player_move(
        self, direction: MoveDirection, simplified_rules: set[Rule]
    ):
        object_piece_types_that_are_you = (
            RuleReadingHelper.get_object_piece_types_that_are_you(
                simplified_rules=simplified_rules
            )
        )
        for map_piece in self.map_pieces:
            if self._is_piece_type_within_object_piece_types(
                piece_type=map_piece.piece_type,
                object_piece_types=object_piece_types_that_are_you,
            ):
                self._execute_object_move(
                    map_piece=map_piece,
                    direction=direction,
                    simplified_rules=simplified_rules,
                )

    def _execute_npc_move(self, simplified_rules: set[Rule]):
        object_piece_types_that_are_move = (
            RuleReadingHelper.get_object_piece_types_that_are_move(
                simplified_rules=simplified_rules
            )
        )
        for map_piece in self.map_pieces:
            if self._is_piece_type_within_object_piece_types(
                piece_type=map_piece.piece_type,
                object_piece_types=object_piece_types_that_are_move,
            ):
                assert map_piece.direction != MoveDirection.WAIT
                if not self._can_object_move(
                    map_piece=map_piece,
                    direction=map_piece.direction,
                    simplified_rules=simplified_rules,
                ):
                    map_piece.direction = MoveDirectionHelper.reverse_direction(
                        map_piece.direction
                    )
                self._execute_object_move(
                    map_piece=map_piece,
                    direction=map_piece.direction,
                    simplified_rules=simplified_rules,
                )

    def _execute_shifts(self, simplified_rules: set[Rule]):
        # TODO: Implement shift
        pass

    def _execute_object_move(
        self,
        map_piece: MapPiece,
        direction: MoveDirection,
        simplified_rules: set[Rule],
    ):
        if direction == MoveDirection.WAIT:
            return
        if not self._can_object_move(
            map_piece=map_piece, direction=direction, simplified_rules=simplified_rules
        ):
            return
        new_position = PiecePositionHelper.get_position_after_move(
            position=map_piece.position, direction=direction
        )
        for pushable_map_piece in self._get_map_pieces_in_position_that_are_push(
            position=new_position, simplified_rules=simplified_rules
        ):
            self._execute_object_move(
                map_piece=pushable_map_piece,
                direction=direction,
                simplified_rules=simplified_rules,
            )
        map_piece.position = new_position
        map_piece.direction = direction

    def _can_object_move(
        self,
        map_piece: MapPiece,
        direction: MoveDirection,
        simplified_rules: set[Rule],
    ) -> bool:
        if self._is_piece_type_within_object_piece_types(
            piece_type=map_piece.piece_type,
            object_piece_types=RuleReadingHelper.get_object_piece_types_that_are_stop(
                simplified_rules=simplified_rules
            ),
        ):
            return False
        new_position = PiecePositionHelper.get_position_after_move(
            position=map_piece.position, direction=direction
        )
        if not self._can_object_enter_position(
            position=new_position, simplified_rules=simplified_rules
        ):
            return False
        map_pieces_in_new_position_that_are_push = (
            self._get_map_pieces_in_position_that_are_push(
                position=new_position, simplified_rules=simplified_rules
            )
        )
        return all(
            [
                self._can_object_move(
                    map_piece=map_piece,
                    direction=direction,
                    simplified_rules=simplified_rules,
                )
                for map_piece in map_pieces_in_new_position_that_are_push
            ]
        )

    def _get_map_pieces_in_position_that_are_push(
        self, position: PiecePosition, simplified_rules: set[Rule]
    ) -> set[MapPiece]:
        map_pieces_in_new_position = self._get_map_pieces_at(position=position)
        object_piece_types_that_are_push = (
            RuleReadingHelper.get_object_piece_types_that_are_push(
                simplified_rules=simplified_rules
            )
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
        self, position: PiecePosition, simplified_rules: set[Rule]
    ) -> bool:
        if position.x < 0:
            return False
        if position.y < 0:
            return False
        if position.x >= self.number_columns:
            return False
        if position.y >= self.number_rows:
            return False
        if self._has_map_piece_in_position_that_is_stop(
            position=position, simplified_rules=simplified_rules
        ):
            return False
        return True

    def _has_map_piece_in_position_that_is_stop(
        self, position: PiecePosition, simplified_rules: set[Rule]
    ) -> bool:
        object_piece_types_that_are_stop = (
            RuleReadingHelper.get_object_piece_types_that_are_stop(
                simplified_rules=simplified_rules
            )
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

    def _apply_defeat_interactions(self, simplified_rules: set[Rule]):
        overlapping_map_pieces = self._get_all_overlapping_map_pieces_between_object_piece_types(
            object_piece_types_1=RuleReadingHelper.get_object_piece_types_that_are_you(
                simplified_rules=simplified_rules
            ),
            object_piece_types_2=RuleReadingHelper.get_object_piece_types_that_are_defeat(
                simplified_rules=simplified_rules
            ),
        )
        for overlapping_map_pieces_that_are_you, _ in overlapping_map_pieces:
            for map_piece in overlapping_map_pieces_that_are_you:
                self._remove_map_piece(map_piece=map_piece)

    def _apply_sink_interactions(self, simplified_rules: set[Rule]):
        # TODO: Handle negation here so that floating objects do not sink
        overlapping_map_pieces = self._get_all_overlapping_map_pieces_between_object_piece_types(
            object_piece_types_1=RuleReadingHelper.get_object_piece_types_that_are_sink(
                simplified_rules=simplified_rules
            ),
            object_piece_types_2=[ObjectPieceType],
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

    def _apply_hot_melt_interactions(self, simplified_rules: set[Rule]):
        # TODO: Implement hot melt
        pass

    def _apply_open_close_interactions(self, simplified_rules: set[Rule]):
        # TODO: Implement open close
        pass

    def _remove_map_piece(self, map_piece: MapPiece):
        if map_piece in self.map_pieces:
            self.map_pieces.remove(map_piece)

    def _apply_noun_mutations(self, simplified_rules: set[Rule]):
        noun_mutations = RuleReadingHelper.get_noun_mutations(
            simplified_rules=simplified_rules
        )
        for noun_mutation in noun_mutations:
            for map_piece in self.map_pieces:
                if isinstance(
                    map_piece.piece_type, noun_mutation.from_object_piece_type
                ):
                    map_piece.piece_type = noun_mutation.to_object_piece_type()

    def is_in_win_state(self) -> bool:
        simplified_rules = self._generate_simplified_rules()
        overlapping_map_pieces = self._get_all_overlapping_map_pieces_between_object_piece_types(
            object_piece_types_1=RuleReadingHelper.get_object_piece_types_that_are_you(
                simplified_rules=simplified_rules
            ),
            object_piece_types_2=RuleReadingHelper.get_object_piece_types_that_are_win(
                simplified_rules=simplified_rules
            ),
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
