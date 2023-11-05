from piecetype import *
from rule import Rule


def generate_rules_for_row(row: list[TextPieceType]) -> set[Rule]:
    rules: set[Rule] = set()
    for start_index in range(len(row)):
        length = _generate_longest_possible_rule_given_start(row[start_index:])
        if length is None:
            continue
        rules.add(Rule(text_piece_types=row[start_index : start_index + length]))
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
