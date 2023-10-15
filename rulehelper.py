import copy

from piecetype import PieceType, WordNounPieceType, WordIsPieceType, WordAttributePieceType, BabaObjectPieceType, FlagObjectPieceType, BabaWordPieceType, FlagWordPieceType, WinWordPieceType, YouWordPieceType


def generate_rules_for_row(row: list[PieceType]):
    rules = []
    for start_index in range(len(row)):
        length = _generate_longest_possible_rule_given_start(row[start_index:])
        if length is None:
            continue
        rules.append(copy.deepcopy(row[start_index:start_index+length]))
    return rules


def _generate_longest_possible_rule_given_start(row: list[PieceType]):
    # TODO: Incorporate 'NOT', 'AND', etc. etc.
    if not isinstance(row[0], WordNounPieceType):
        return None
    if len(row) <= 1 or not isinstance(row[1], WordIsPieceType):
        return None
    if len(row) <= 2 or not isinstance(row[2], WordAttributePieceType):
        return None
    return 3
