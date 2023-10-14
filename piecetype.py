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


class ObjectPieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(BasicType.OBJECT, asset_name)


class WordNounPieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(BasicType.WORD_NOUN, asset_name)


class WordIsPieceType(PieceType):
    def __init__(self):
        super().__init__(BasicType.WORD_IS, "word_is.png")


class WordAttributePieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(BasicType.WORD_ATTRIBUTE, asset_name)


class BabaObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__("object_baba.png")


class FlagObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__("object_flag.png")


class BabaWordPieceType(WordNounPieceType):
    def __init__(self):
        super().__init__("word_baba.png")


class FlagWordPieceType(WordNounPieceType):
    def __init__(self):
        super().__init__("word_flag.png")


class WinWordPieceType(WordAttributePieceType):
    def __init__(self):
        super().__init__("word_win.png")


class YouWordPieceType(WordAttributePieceType):
    def __init__(self):
        super().__init__("word_you.png")

