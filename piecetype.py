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
        super().__init__(BasicType.OBJECT, asset_name)
    def __repr__(self):
        return "ObjectPieceType"


class WordNounPieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(BasicType.WORD_NOUN, asset_name)
    def __repr__(self):
        return "WordNounPieceType"


class WordIsPieceType(PieceType):
    def __init__(self):
        super().__init__(BasicType.WORD_IS, "word_is.png")
    def __repr__(self):
        return "WordIsPieceType"


class WordAttributePieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(BasicType.WORD_ATTRIBUTE, asset_name)
    def __repr__(self):
        return "WordAttributePieceType"


class BabaObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__("object_baba.png")
    def __repr__(self):
        return "BabaObjectPieceType"


class FlagObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__("object_flag.png")
    def __repr__(self):
        return "FlagObjectPieceType"


class BabaWordPieceType(WordNounPieceType):
    def __init__(self):
        super().__init__("word_baba.png")
    def __repr__(self):
        return "BabaWordPieceType"


class FlagWordPieceType(WordNounPieceType):
    def __init__(self):
        super().__init__("word_flag.png")
    def __repr__(self):
        return "FlagWordPieceType"


class WinWordPieceType(WordAttributePieceType):
    def __init__(self):
        super().__init__("word_win.png")
    def __repr__(self):
        return "WinWordPieceType"


class YouWordPieceType(WordAttributePieceType):
    def __init__(self):
        super().__init__("word_you.png")
    def __repr__(self):
        return "YouWordPieceType"
