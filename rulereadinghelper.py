from typing import Type

from nounmutation import NounMutation
from piecetype import *
from rule import Rule
from ruletype import RuleType


def get_object_piece_types_that_are_you(
    rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=YouTextPieceType
    )


def get_object_piece_types_that_are_win(
    rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=WinTextPieceType
    )


def get_object_piece_types_that_are_push(
    rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=PushTextPieceType
    )


def get_object_piece_types_that_are_stop(
    rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=StopTextPieceType
    )


def get_object_piece_types_that_are_defeat(
    rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=DefeatTextPieceType
    )


def get_object_piece_types_that_are_sink(
    rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=SinkTextPieceType
    )


def get_object_piece_types_that_are_move(
    rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        rules=rules, attribute_text_piece_type=MoveTextPieceType
    )


def _get_object_piece_types_that_have_attribute(
    rules: set[Rule], attribute_text_piece_type: Type[TextPieceType]
) -> set[Type[ObjectPieceType]]:
    object_piece_types_that_are_attribute: set[Type[ObjectPieceType]] = set()
    for rule in rules:
        noun_text_piece_type_for_attribute = _get_noun_text_piece_type_for_attribute(
            rule=rule, attribute_text_piece_type=attribute_text_piece_type
        )
        if noun_text_piece_type_for_attribute:
            object_piece_types_that_are_attribute.add(
                noun_text_piece_type_for_attribute.associated_object_piece_type
            )
    return object_piece_types_that_are_attribute


def _get_noun_text_piece_type_for_attribute(
    rule: Rule, attribute_text_piece_type: Type[TextPieceType]
) -> NounTextPieceType:
    # TODO: Incorporate 'NOT', 'AND', etc. etc.
    if (
        rule.rule_type == RuleType.NOUN_IS_ATTRIBUTE
        and len(rule.text_piece_types) == 3
        and isinstance(rule.text_piece_types[0], NounTextPieceType)
        and isinstance(rule.text_piece_types[1], IsTextPieceType)
        and isinstance(rule.text_piece_types[2], attribute_text_piece_type)
    ):
        return rule.text_piece_types[0]
    return None


def get_noun_mutations(rules: set[Rule]) -> set[NounMutation]:
    # TODO: Incorporate 'NOT', 'AND', etc. etc.
    return set(
        [
            NounMutation(
                from_object_piece_type=rule.text_piece_types[
                    0
                ].associated_object_piece_type,
                to_object_piece_type=rule.text_piece_types[
                    2
                ].associated_object_piece_type,
            )
            for rule in rules
            if rule.rule_type == RuleType.NOUN_IS_NOUN
            and len(rule.text_piece_types) == 3
            and isinstance(rule.text_piece_types[0], NounTextPieceType)
            and isinstance(rule.text_piece_types[1], IsTextPieceType)
            and isinstance(rule.text_piece_types[2], NounTextPieceType)
        ]
    )
