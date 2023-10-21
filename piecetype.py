from typing import Type


class PieceType:
    def __init__(self, asset_name: str):
        self.asset_name = asset_name
    def __repr__(self) -> str:
        return "PieceType"


class ObjectPieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(asset_name=asset_name)
    def __repr__(self) -> str:
        return "ObjectPieceType"


class TextPieceType(ObjectPieceType): # Technically text pieces are themselves objects!
    def __init__(self, asset_name: str):
        super().__init__(asset_name=asset_name)
    def __repr__(self) -> str:
        return "TextPieceType"
    def _debug_repr(self) -> str:
        return self.__repr__()[:-len("TextPieceType")]


class NounTextPieceType(TextPieceType):
    def __init__(self, asset_name: str, associated_object_piece_types: list[Type[ObjectPieceType]]):
        super().__init__(asset_name=asset_name)
        # The object(s) that this noun text should be controlling on the board
        self.associated_object_piece_types = associated_object_piece_types
    def __repr__(self) -> str:
        return "NounTextPieceType"


class IsTextPieceType(TextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_is.png")
    def __repr__(self) -> str:
        return "IsTextPieceType"


class AttributeTextPieceType(TextPieceType):
    def __init__(self, asset_name: str):
        super().__init__(asset_name=asset_name)
    def __repr__(self) -> str:
        return "AttributeTextPieceType"


class BabaObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(asset_name="object_baba.png")
    def __repr__(self) -> str:
        return "BabaObjectPieceType"


class FlagObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(asset_name="object_flag.png")
    def __repr__(self) -> str:
        return "FlagObjectPieceType"


class RockObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(asset_name="object_rock.png")
    def __repr__(self) -> str:
        return "RockObjectPieceType"


class WallObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(asset_name="object_wall.png")
    def __repr__(self) -> str:
        return "WallObjectPieceType"


class BabaTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_baba.png", associated_object_piece_types=[BabaObjectPieceType])
    def __repr__(self) -> str:
        return "BabaTextPieceType"


class FlagTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_flag.png", associated_object_piece_types=[FlagObjectPieceType])
    def __repr__(self) -> str:
        return "FlagTextPieceType"


class TextTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_text.png", associated_object_piece_types=[TextPieceType])
    def __repr__(self) -> str:
        return "TextTextPieceType"


class RockTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_rock.png", associated_object_piece_types=[RockObjectPieceType])
    def __repr__(self) -> str:
        return "RockTextPieceType"


class WallTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_wall.png", associated_object_piece_types=[WallObjectPieceType])
    def __repr__(self) -> str:
        return "WallTextPieceType"


class WinTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_win.png")
    def __repr__(self) -> str:
        return "WinTextPieceType"


class YouTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_you.png")
    def __repr__(self) -> str:
        return "YouTextPieceType"


class PushTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_push.png")
    def __repr__(self) -> str:
        return "PushTextPieceType"


class StopTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_stop.png")
    def __repr__(self) -> str:
        return "StopTextPieceType"
