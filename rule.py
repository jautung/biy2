from typing import Type
import copy

from piecetype import *


# TODO: Somehow implement rule overriding logic
class Rule:
    def __init__(self, text_piece_types: list[TextPieceType]):
        # TODO: Incorporate 'NOT', 'AND', etc. etc.
        assert len(text_piece_types) == 3
        self.rule = copy.deepcopy(text_piece_types)

    def __repr__(self) -> str:
        return " ".join(
            [text_piece_type.in_rule_repr() for text_piece_type in self.rule]
        )

    def get_noun_text_piece_type_for_attribute(
        self, attribute_text_piece_type: Type[TextPieceType]
    ) -> NounTextPieceType:
        # TODO: Incorporate 'NOT', 'AND', etc. etc.
        if (
            len(self.rule) == 3
            and isinstance(self.rule[0], NounTextPieceType)
            and isinstance(self.rule[1], IsTextPieceType)
            and isinstance(self.rule[2], attribute_text_piece_type)
        ):
            return self.rule[0]
        return None
