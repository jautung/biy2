from piecetype import PieceType, TextNounPieceType, TextIsPieceType, TextAttributePieceType


def is_word_piece_type(piece_type: PieceType) -> bool:
    return isinstance(piece_type, TextNounPieceType) or isinstance(piece_type, TextIsPieceType) or isinstance(piece_type, TextAttributePieceType)
