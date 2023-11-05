import copy
from typing import Type

from piecetype import *
from rule import Rule
from ruletype import RuleType


DEFAULT_TEXT_IS_PUSH_RULE = Rule(
    rule_type=RuleType.NOUN_CLAUSE_IS_ATTRIBUTE_CLAUSE,
    text_piece_types=[
        TextTextPieceType(),
        IsTextPieceType(),
        PushTextPieceType(),
    ],
)


def generate_rules_for_row(row: list[TextPieceType]) -> set[Rule]:
    rules: set[Rule] = set()
    start_index = 0
    while start_index < len(row):
        rule = _generate_longest_possible_rule_given_start(row[start_index:])
        if rule is None:
            start_index += 1
            continue
        rules.add(rule)
        start_index += rule.get_length()
    return rules


def get_final_rules_from_all_on_map_rules(on_map_rules: set[Rule]) -> set[Rule]:
    rules = copy.deepcopy(on_map_rules)
    # By default, "TEXT IS PUSH" is always a rule, even if it is not on the map
    rules.add(DEFAULT_TEXT_IS_PUSH_RULE)
    # TODO: Somehow implement rule overriding logic
    return rules


def _generate_longest_possible_rule_given_start(row: list[TextPieceType]) -> Rule:
    for end_index in range(len(row), 1, -1):
        maybe_rule = row[:end_index]
        maybe_rule_type = _get_maybe_rule_type(maybe_rule=maybe_rule)
        if maybe_rule_type is not None:
            return Rule(rule_type=maybe_rule_type, text_piece_types=maybe_rule)
    return None


def _get_maybe_rule_type(maybe_rule: list[TextPieceType]) -> bool:
    if not all([isinstance(piece_type, TextPieceType) for piece_type in maybe_rule]):
        return None
    number_of_is = len(
        list(
            filter(
                lambda piece_type: isinstance(piece_type, IsTextPieceType), maybe_rule
            )
        )
    )
    number_of_has = len(
        list(
            filter(
                lambda piece_type: isinstance(piece_type, HasTextPieceType), maybe_rule
            )
        )
    )
    if number_of_is == 1 and number_of_has == 0:
        index_of_is = next(
            index
            for index, piece_type in enumerate(maybe_rule)
            if isinstance(piece_type, IsTextPieceType)
        )
        clause_before_is = maybe_rule[:index_of_is]
        clause_after_is = maybe_rule[index_of_is + 1 :]
        if _is_noun_clause(maybe_noun_clause=clause_before_is) and _is_attribute_clause(
            maybe_attribute_clause=clause_after_is
        ):
            return RuleType.NOUN_CLAUSE_IS_ATTRIBUTE_CLAUSE
        if _is_noun_clause(maybe_noun_clause=clause_before_is) and _is_noun(
            maybe_noun=clause_after_is
        ):
            return RuleType.NOUN_CLAUSE_IS_NOUN
    if number_of_is == 0 and number_of_has == 1:
        index_of_has = next(
            index
            for index, piece_type in enumerate(maybe_rule)
            if isinstance(piece_type, HasTextPieceType)
        )
        clause_before_has = maybe_rule[:index_of_has]
        clause_after_has = maybe_rule[index_of_has + 1 :]
        if _is_noun_clause(maybe_noun_clause=clause_before_has) and _is_noun(
            maybe_noun=clause_after_has
        ):
            return RuleType.NOUN_CLAUSE_HAS_NOUN
    return None


def _is_noun(maybe_noun: list[TextPieceType]) -> bool:
    return len(maybe_noun) == 1 and isinstance(maybe_noun[0], NounTextPieceType)


def _is_noun_clause(maybe_noun_clause: list[TextPieceType]) -> bool:
    return _is_type_of_clause_with_conjugation(
        maybe_type_of_clause=maybe_noun_clause, base_case_piece_type=NounTextPieceType
    )


def _is_attribute_clause(maybe_attribute_clause: list[TextPieceType]) -> bool:
    return _is_type_of_clause_with_conjugation(
        maybe_type_of_clause=maybe_attribute_clause,
        base_case_piece_type=AttributeTextPieceType,
    )


def _is_type_of_clause_with_conjugation(
    maybe_type_of_clause: list[TextPieceType],
    base_case_piece_type: Type[PieceType],
) -> bool:
    if len(maybe_type_of_clause) == 0:
        return False
    if len(maybe_type_of_clause) == 1:
        return isinstance(maybe_type_of_clause[0], base_case_piece_type)
    if isinstance(maybe_type_of_clause[0], NotTextPieceType):
        return _is_type_of_clause_with_conjugation(
            maybe_type_of_clause=maybe_type_of_clause[1:],
            base_case_piece_type=base_case_piece_type,
        )
    if any(
        [
            isinstance(piece_type, AndTextPieceType)
            for piece_type in maybe_type_of_clause
        ]
    ):
        index_of_and = next(
            index
            for index, piece_type in enumerate(maybe_type_of_clause)
            if isinstance(piece_type, AndTextPieceType)
        )
        clause_before_and = maybe_type_of_clause[:index_of_and]
        clause_after_and = maybe_type_of_clause[index_of_and + 1 :]
        return _is_type_of_clause_with_conjugation(
            maybe_type_of_clause=clause_before_and,
            base_case_piece_type=base_case_piece_type,
        ) and _is_type_of_clause_with_conjugation(
            maybe_type_of_clause=clause_after_and,
            base_case_piece_type=base_case_piece_type,
        )
    return False
