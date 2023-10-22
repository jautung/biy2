from typing import Type

from piecetype import *
from rule import Rule


def generate_rules_for_row(row: list[TextPieceType]) -> list[Rule]:
    rules: list[Rule] = []
    for start_index in range(len(row)):
        length = _generate_longest_possible_rule_given_start(row[start_index:])
        if length is None:
            continue
        rules.append(Rule(text_piece_types=row[start_index : start_index + length]))
    return rules


def _generate_longest_possible_rule_given_start(row: list[TextPieceType]) -> int:
    # TODO: Incorporate 'NOT', 'AND', etc. etc.
    if not isinstance(row[0], NounTextPieceType):
        return None
    if len(row) <= 1 or not isinstance(row[1], IsTextPieceType):
        return None
    if len(row) <= 2 or not isinstance(row[2], AttributeTextPieceType):
        return None
    return 3


def get_object_piece_types_that_are_you(
    rules: list[Rule],
) -> list[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=YouTextPieceType
    )


def get_object_piece_types_that_are_win(
    rules: list[Rule],
) -> list[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=WinTextPieceType
    )


def get_object_piece_types_that_are_push(
    rules: list[Rule],
) -> list[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=PushTextPieceType
    )


def get_object_piece_types_that_are_stop(
    rules: list[Rule],
) -> list[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=StopTextPieceType
    )


def get_object_piece_types_that_are_defeat(
    rules: list[Rule],
) -> list[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=DefeatTextPieceType
    )


def _get_object_piece_types_that_have_attribute(
    rules: list[Rule], attribute_text_piece_type: Type[TextPieceType]
) -> list[Type[ObjectPieceType]]:
    object_piece_types_that_are_attribute: list[Type[ObjectPieceType]] = []
    for rule in rules:
        noun_text_piece_type_for_attribute = (
            rule.get_noun_text_piece_type_for_attribute(
                attribute_text_piece_type=attribute_text_piece_type
            )
        )
        if noun_text_piece_type_for_attribute:
            object_piece_types_that_are_attribute.append(
                noun_text_piece_type_for_attribute.associated_object_piece_type
            )
    return object_piece_types_that_are_attribute
