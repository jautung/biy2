from typing import Type
import copy

from piecetype import *


def generate_rules_for_row(row: list[PieceType]) -> list[list[TextPieceType]]:
    rules = []
    for start_index in range(len(row)):
        length = _generate_longest_possible_rule_given_start(row[start_index:])
        if length is None:
            continue
        rules.append(copy.deepcopy(row[start_index : start_index + length]))
    return rules


def _generate_longest_possible_rule_given_start(row: list[PieceType]) -> int:
    # TODO: Incorporate 'NOT', 'AND', etc. etc.
    if not isinstance(row[0], NounTextPieceType):
        return None
    if len(row) <= 1 or not isinstance(row[1], IsTextPieceType):
        return None
    if len(row) <= 2 or not isinstance(row[2], AttributeTextPieceType):
        return None
    return 3


def get_object_piece_types_that_are_you(
    rules: list[list[TextPieceType]],
) -> list[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=YouTextPieceType
    )


def get_object_piece_types_that_are_win(
    rules: list[list[TextPieceType]],
) -> list[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=WinTextPieceType
    )


def get_object_piece_types_that_are_push(
    rules: list[list[TextPieceType]],
) -> list[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=PushTextPieceType
    )


def _get_object_piece_types_that_have_attribute(
    rules: list[list[TextPieceType]], attribute_text_piece_type: Type[TextPieceType]
) -> list[Type[ObjectPieceType]]:
    # TODO: Incorporate 'NOT', 'AND', etc. etc.
    object_piece_types_that_are_attribute: list[Type[ObjectPieceType]] = []
    for rule in rules:
        if (
            len(rule) == 3
            and isinstance(rule[0], NounTextPieceType)
            and isinstance(rule[1], IsTextPieceType)
            and isinstance(rule[2], attribute_text_piece_type)
        ):
            object_piece_types_that_are_attribute += rule[
                0
            ].associated_object_piece_types
    return object_piece_types_that_are_attribute
