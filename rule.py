from typing import Type
import copy

from piecetype import *


class Rule:
    def __init__(self, text_piece_types: list[TextPieceType]):
        self.rule = copy.deepcopy(text_piece_types)

    def __repr__(self) -> str:
        return " ".join(
            [text_piece_type.in_rule_repr() for text_piece_type in self.rule]
        )
