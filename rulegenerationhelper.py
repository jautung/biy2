from piecetype import *
from rule import Rule
from ruletype import RuleType


DEFAULT_TEXT_IS_PUSH_RULE = Rule(
    rule_type=RuleType.NOUN_IS_ATTRIBUTE,
    text_piece_types=[
        TextTextPieceType(),
        IsTextPieceType(),
        PushTextPieceType(),
    ],
)


def generate_rules_for_row(row: list[TextPieceType]) -> set[Rule]:
    rules: set[Rule] = set()
    for start_index in range(len(row)):
        rule = _generate_longest_possible_rule_given_start(row[start_index:])
        if rule is None:
            continue
        rules.add(rule)
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
            return RuleType.NOUN_IS_ATTRIBUTE
        if _is_noun_clause(maybe_noun_clause=clause_before_is) and _is_noun_clause(
            maybe_noun_clause=clause_after_is
        ):
            return RuleType.NOUN_IS_NOUN
    if number_of_is == 0 and number_of_has == 1:
        index_of_has = next(
            index
            for index, piece_type in enumerate(maybe_rule)
            if isinstance(piece_type, HasTextPieceType)
        )
        clause_before_has = maybe_rule[:index_of_has]
        clause_after_has = maybe_rule[index_of_has + 1 :]
        if _is_noun_clause(maybe_noun_clause=clause_before_has) and _is_noun_clause(
            maybe_noun_clause=clause_after_has
        ):
            return RuleType.NOUN_HAS_NOUN
    return None


def _is_noun_clause(maybe_noun_clause: list[TextPieceType]) -> bool:
    # TODO: Properly implement this
    return len(maybe_noun_clause) == 1 and isinstance(
        maybe_noun_clause[0], NounTextPieceType
    )


def _is_attribute_clause(maybe_attribute_clause: list[TextPieceType]) -> bool:
    # TODO: Properly implement this
    return len(maybe_attribute_clause) == 1 and isinstance(
        maybe_attribute_clause[0], AttributeTextPieceType
    )
