class PieceType:
    def __init__(self, asset_name: str):
        self.asset_name = asset_name
    def __repr__(self):
        return "PieceType"


class ObjectPieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(asset_name=asset_name)
    def __repr__(self):
        return "ObjectPieceType"


class TextPieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(asset_name=asset_name)
    def __repr__(self):
        return "TextPieceType"


class NounTextPieceType(TextPieceType):
    def __init__(self, asset_name: str, associated_object_piece_types):
        super().__init__(asset_name=asset_name)
        # The object(s) that this noun text should be controlling on the board
        self.associated_object_piece_types = associated_object_piece_types
    def __repr__(self):
        return "NounTextPieceType"


class IsTextPieceType(TextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_is.png")
    def __repr__(self):
        return "IsTextPieceType"


class AttributeTextPieceType(TextPieceType):
    def __init__(self, asset_name: str):
        super().__init__(asset_name=asset_name)
    def __repr__(self):
        return "AttributeTextPieceType"


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


class BabaTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_baba.png", associated_object_piece_types=[BabaObjectPieceType])
    def __repr__(self):
        return "BabaTextPieceType"


class FlagTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_flag.png", associated_object_piece_types=[FlagObjectPieceType])
    def __repr__(self):
        return "FlagTextPieceType"


class TextTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_text.png", associated_object_piece_types=[TextPieceType])
    def __repr__(self):
        return "TextTextPieceType"


class WinTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_win.png")
    def __repr__(self):
        return "WinTextPieceType"


class YouTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_you.png")
    def __repr__(self):
        return "YouTextPieceType"


class PushTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_push.png")
    def __repr__(self):
        return "PushTextPieceType"
