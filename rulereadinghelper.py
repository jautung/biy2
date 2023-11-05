import inspect
import itertools
from typing import Type

import rulehelper as RuleHelper
from nounmutation import NounMutation
from piecetype import *
from rule import Rule
from ruletype import RuleType


# Simplified rules remove all 'AND's and counts the parity of 'NOT's, and are thus of the form:
# (X | NOT X) (IS | HAS) (Y | NOT Y)
def simplify_rules(rules: set[Rule]) -> set[Rule]:
    simplified_rules: set[Rule] = set()
    for rule in rules:
        simplified_rules = simplified_rules.union(_simplify_rule(rule=rule))
    return simplified_rules


def _simplify_rule(rule: Rule) -> set[Rule]:
    if rule.rule_type == RuleType.NOUN_CLAUSE_IS_ATTRIBUTE_CLAUSE:
        return _simplify_noun_clause_is_attribute_clause_rule(rule)
    if rule.rule_type == RuleType.NOUN_CLAUSE_IS_NOUN:
        return _simplify_noun_clause_is_noun_rule(rule)
    if rule.rule_type == RuleType.NOUN_CLAUSE_HAS_NOUN:
        return _simplify_noun_clause_has_noun_rule(rule)
    assert False


def _simplify_noun_clause_is_attribute_clause_rule(rule: Rule) -> set[Rule]:
    assert rule.rule_type == RuleType.NOUN_CLAUSE_IS_ATTRIBUTE_CLAUSE
    index_of_is = RuleHelper.index_of_is_text_piece_type_in_list(
        text_piece_types=rule.text_piece_types
    )
    noun_clause_before_is = rule.text_piece_types[:index_of_is]
    attribute_clause_after_is = rule.text_piece_types[index_of_is + 1 :]
    simplified_noun_clauses_before_is = _simplify_clause(clause=noun_clause_before_is)
    simplified_attribute_clauses_after_is = _simplify_clause(
        clause=attribute_clause_after_is
    )
    return set(
        [
            Rule(
                rule_type=rule.rule_type,
                text_piece_types=simplified_noun_clause_before_is
                + [IsTextPieceType()]
                + simplified_attribute_clause_after_is,
            )
            for simplified_noun_clause_before_is in simplified_noun_clauses_before_is
            for simplified_attribute_clause_after_is in simplified_attribute_clauses_after_is
        ]
    )


def _simplify_noun_clause_is_noun_rule(rule: Rule) -> set[Rule]:
    assert rule.rule_type == RuleType.NOUN_CLAUSE_IS_NOUN
    index_of_is = RuleHelper.index_of_is_text_piece_type_in_list(
        text_piece_types=rule.text_piece_types
    )
    noun_clause_before_is = rule.text_piece_types[:index_of_is]
    noun_after_is = rule.text_piece_types[index_of_is + 1 :]
    simplified_noun_clauses_before_is = _simplify_clause(clause=noun_clause_before_is)
    return set(
        [
            Rule(
                rule_type=rule.rule_type,
                text_piece_types=simplified_noun_clause_before_is
                + [IsTextPieceType()]
                + noun_after_is,
            )
            for simplified_noun_clause_before_is in simplified_noun_clauses_before_is
        ]
    )


def _simplify_noun_clause_has_noun_rule(rule: Rule) -> set[Rule]:
    assert rule.rule_type == RuleType.NOUN_CLAUSE_HAS_NOUN
    index_of_has = RuleHelper.index_of_has_text_piece_type_in_list(
        text_piece_types=rule.text_piece_types
    )
    noun_clause_before_has = rule.text_piece_types[:index_of_has]
    noun_after_has = rule.text_piece_types[index_of_has + 1 :]
    simplified_noun_clauses_before_has = _simplify_clause(clause=noun_clause_before_has)
    return set(
        [
            Rule(
                rule_type=rule.rule_type,
                text_piece_types=simplified_noun_clause_before_has
                + [HasTextPieceType()]
                + noun_after_has,
            )
            for simplified_noun_clause_before_has in simplified_noun_clauses_before_has
        ]
    )


def _simplify_clause(
    clause: list[TextPieceType],
) -> list[list[TextPieceType]]:
    return [
        _simplify_nots_from_clause(clause=list(simplified_noun_clause))
        for key, simplified_noun_clause in itertools.groupby(
            clause, lambda piece_type: isinstance(piece_type, AndTextPieceType)
        )
        if not key
    ]


def _simplify_nots_from_clause(clause: list[TextPieceType]) -> list[TextPieceType]:
    if (
        len(clause) >= 2
        and isinstance(clause[0], NotTextPieceType)
        and isinstance(clause[1], NotTextPieceType)
    ):
        return _simplify_nots_from_clause(clause=clause[2:])
    return clause


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
    # TODO: Incorporate 'NOT' as a rule left-hand-side modifier
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
    # TODO: Incorporate 'NOT' as a rule left-hand-side modifier
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


def _get_simplified_noun_clause_from_simplified_rule(
    simplified_rule: Rule,
) -> list[TextPieceType]:
    if simplified_rule.rule_type == RuleType.NOUN_CLAUSE_IS_ATTRIBUTE_CLAUSE:
        index_of_is = RuleHelper.index_of_is_text_piece_type_in_list(
            text_piece_types=simplified_rule.text_piece_types
        )
        return simplified_rule.text_piece_types[:index_of_is]
    if simplified_rule.rule_type == RuleType.NOUN_CLAUSE_IS_NOUN:
        index_of_is = RuleHelper.index_of_is_text_piece_type_in_list(
            text_piece_types=simplified_rule.text_piece_types
        )
        return simplified_rule.text_piece_types[:index_of_is]
    if simplified_rule.rule_type == RuleType.NOUN_CLAUSE_HAS_NOUN:
        index_of_has = RuleHelper.index_of_has_text_piece_type_in_list(
            text_piece_types=simplified_rule.text_piece_types
        )
        return simplified_rule.text_piece_types[:index_of_has]
    assert False


def _get_all_object_piece_types() -> set[Type[ObjectPieceType]]:
    all_object_piece_types: set[Type[ObjectPieceType]] = set()

    def search_object_piece_type_subclasses(object_piece_type: Type[ObjectPieceType]):
        # We only care about concrete classes that can be instantiated with PieceType(),
        # and not the PieceType, ObjectPieceType, etc. super-classes
        if len(inspect.signature(object_piece_type.__init__).parameters) == 1:
            all_object_piece_types.add(object_piece_type)
        for subclass_piece_type in object_piece_type.__subclasses__():
            search_object_piece_type_subclasses(subclass_piece_type)

    search_object_piece_type_subclasses(ObjectPieceType)
    return all_object_piece_types
