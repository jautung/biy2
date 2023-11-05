import copy

from piecetype import *
from ruletype import RuleType


class Rule:
    def __init__(self, rule_type: RuleType, text_piece_types: list[TextPieceType]):
        self.rule_type = rule_type
        self.text_piece_types = copy.deepcopy(text_piece_types)

    def __repr__(self) -> str:
        return " ".join(
            [
                text_piece_type.in_rule_repr()
                for text_piece_type in self.text_piece_types
            ]
        )

    def get_length(self) -> int:
        return len(self.text_piece_types)
