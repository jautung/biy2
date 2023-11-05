from typing import Type

from nounmutation import NounMutation
from piecetype import *
from rule import Rule
from ruletype import RuleType


# Simplified rules remove all 'AND's, and are thus of the form:
# (X | NOT X) (IS | HAS) (Y | NOT Y)
def simplify_rules(rules: set[Rule]) -> set[Rule]:
    # TODO: Implement this
    return rules


def get_object_piece_types_that_are_you(
    simplified_rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        simplified_rules=simplified_rules, attribute_text_piece_type=YouTextPieceType
    )


def get_object_piece_types_that_are_win(
    simplified_rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        simplified_rules=simplified_rules, attribute_text_piece_type=WinTextPieceType
    )


def get_object_piece_types_that_are_push(
    simplified_rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        simplified_rules=simplified_rules, attribute_text_piece_type=PushTextPieceType
    )


def get_object_piece_types_that_are_stop(
    simplified_rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        simplified_rules=simplified_rules, attribute_text_piece_type=StopTextPieceType
    )


def get_object_piece_types_that_are_defeat(
    simplified_rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        simplified_rules=simplified_rules, attribute_text_piece_type=DefeatTextPieceType
    )


def get_object_piece_types_that_are_sink(
    simplified_rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        simplified_rules=simplified_rules, attribute_text_piece_type=SinkTextPieceType
    )


def get_object_piece_types_that_are_move(
    simplified_rules: set[Rule],
) -> set[Type[ObjectPieceType]]:
    return _get_object_piece_types_that_have_attribute(
        simplified_rules=simplified_rules, attribute_text_piece_type=MoveTextPieceType
    )


def _get_object_piece_types_that_have_attribute(
    simplified_rules: set[Rule], attribute_text_piece_type: Type[TextPieceType]
) -> set[Type[ObjectPieceType]]:
    object_piece_types_that_are_attribute: set[Type[ObjectPieceType]] = set()
    for simplified_rule in simplified_rules:
        noun_text_piece_type_for_attribute = _get_noun_text_piece_type_for_attribute(
            simplified_rule=simplified_rule,
            attribute_text_piece_type=attribute_text_piece_type,
        )
        if noun_text_piece_type_for_attribute:
            object_piece_types_that_are_attribute.add(
                noun_text_piece_type_for_attribute.associated_object_piece_type
            )
    return object_piece_types_that_are_attribute


def _get_noun_text_piece_type_for_attribute(
    simplified_rule: Rule, attribute_text_piece_type: Type[TextPieceType]
) -> NounTextPieceType:
    # TODO: Incorporate 'NOT', 'AND', etc. etc.
    if (
        simplified_rule.rule_type == RuleType.NOUN_CLAUSE_IS_ATTRIBUTE_CLAUSE
        and len(simplified_rule.text_piece_types) == 3
        and isinstance(simplified_rule.text_piece_types[0], NounTextPieceType)
        and isinstance(simplified_rule.text_piece_types[1], IsTextPieceType)
        and isinstance(simplified_rule.text_piece_types[2], attribute_text_piece_type)
    ):
        return simplified_rule.text_piece_types[0]
    return None


def get_noun_mutations(simplified_rules: set[Rule]) -> set[NounMutation]:
    # TODO: Incorporate 'NOT', 'AND', etc. etc.
    return set(
        [
            NounMutation(
                from_object_piece_type=simplified_rule.text_piece_types[
                    0
                ].associated_object_piece_type,
                to_object_piece_type=simplified_rule.text_piece_types[
                    2
                ].associated_object_piece_type,
            )
            for simplified_rule in simplified_rules
            if simplified_rule.rule_type == RuleType.NOUN_CLAUSE_IS_NOUN
            and len(simplified_rule.text_piece_types) == 3
            and isinstance(simplified_rule.text_piece_types[0], NounTextPieceType)
            and isinstance(simplified_rule.text_piece_types[1], IsTextPieceType)
            and isinstance(simplified_rule.text_piece_types[2], NounTextPieceType)
        ]
    )
