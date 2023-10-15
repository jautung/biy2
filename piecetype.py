from enum import Enum, auto


class BasicType(Enum):
    OBJECT = auto()
    WORD_NOUN = auto()
    WORD_IS = auto()
    WORD_ATTRIBUTE = auto()


class PieceType:
    def __init__(self, type: BasicType, asset_name: str):
        self.type = type
        self.asset_name = asset_name
    def __repr__(self):
        return "PieceType"


class ObjectPieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(type=BasicType.OBJECT, asset_name=asset_name)
    def __repr__(self):
        return "ObjectPieceType"


class WordNounPieceType(PieceType):
    def __init__(self, asset_name: str, associated_object_piece_type):
        super().__init__(type=BasicType.WORD_NOUN, asset_name=asset_name)
        self.associated_object_piece_type = associated_object_piece_type
    def __repr__(self):
        return "WordNounPieceType"


class WordIsPieceType(PieceType):
    def __init__(self):
        super().__init__(type=BasicType.WORD_IS, asset_name="word_is.png")
    def __repr__(self):
        return "WordIsPieceType"


class WordAttributePieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(type=BasicType.WORD_ATTRIBUTE, asset_name=asset_name)
    def __repr__(self):
        return "WordAttributePieceType"


class BabaObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(asset_name="object_baba.png")
    def __repr__(self):
        return "BabaObjectPieceType"


class FlagObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(asset_name="object_flag.png")
    def __repr__(self):
        return "FlagObjectPieceType"


class BabaWordPieceType(WordNounPieceType):
    def __init__(self):
        super().__init__(asset_name="word_baba.png", associated_object_piece_type=BabaObjectPieceType)
    def __repr__(self):
        return "BabaWordPieceType"


class FlagWordPieceType(WordNounPieceType):
    def __init__(self):
        super().__init__(asset_name="word_flag.png", associated_object_piece_type=FlagObjectPieceType)
    def __repr__(self):
        return "FlagWordPieceType"


class WinWordPieceType(WordAttributePieceType):
    def __init__(self):
        super().__init__(asset_name="word_win.png")
    def __repr__(self):
        return "WinWordPieceType"


class YouWordPieceType(WordAttributePieceType):
    def __init__(self):
        super().__init__(asset_name="word_you.png")
    def __repr__(self):
        return "YouWordPieceType"
