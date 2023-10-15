from piecetype import PieceType, WordNounPieceType, WordIsPieceType, WordAttributePieceType


def is_word_piece_type(piece_type: PieceType) -> bool:
    return isinstance(piece_type, WordNounPieceType) or isinstance(piece_type, WordIsPieceType) or isinstance(piece_type, WordAttributePieceType)
