from typing import Type

from piecetype import *


def index_of_is_text_piece_type_in_list(text_piece_types: list[TextPieceType]) -> int:
    return _index_of_text_piece_type_in_list(
        text_piece_types=text_piece_types, target_text_piece_type=IsTextPieceType
    )


def index_of_and_text_piece_type_in_list(text_piece_types: list[TextPieceType]) -> int:
    return _index_of_text_piece_type_in_list(
        text_piece_types=text_piece_types, target_text_piece_type=AndTextPieceType
    )


def index_of_has_text_piece_type_in_list(text_piece_types: list[TextPieceType]) -> int:
    return _index_of_text_piece_type_in_list(
        text_piece_types=text_piece_types, target_text_piece_type=HasTextPieceType
    )


def _index_of_text_piece_type_in_list(
    text_piece_types: list[TextPieceType], target_text_piece_type: Type[TextPieceType]
) -> int:
    return next(
        index
        for index, piece_type in enumerate(text_piece_types)
        if isinstance(piece_type, target_text_piece_type)
    )
