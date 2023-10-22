from typing import Type


# Images at https://docs.google.com/presentation/d/1frkfoDgriNW8fC-DpAeI8oB3nAnU9JQ5UQh_VQ3LjvQ/edit


class PieceType:
    def __init__(self, asset_name: str):
        self.asset_name = asset_name

    def __repr__(self) -> str:
        return "PieceType"

    def json_repr(self) -> str:
        return self.__repr__()[: -len("PieceType")]


class ObjectPieceType(PieceType):
    def __init__(self, asset_name: str):
        super().__init__(asset_name=asset_name)

    def __repr__(self) -> str:
        return "ObjectPieceType"


class TextPieceType(ObjectPieceType):  # Technically text pieces are themselves objects!
    def __init__(self, asset_name: str):
        super().__init__(asset_name=asset_name)

    def __repr__(self) -> str:
        return "TextPieceType"

    def in_rule_repr(self) -> str:
        return self.__repr__()[: -len("TextPieceType")]


class NounTextPieceType(TextPieceType):
    def __init__(
        self,
        asset_name: str,
        associated_object_piece_type: Type[ObjectPieceType],
    ):
        super().__init__(asset_name=asset_name)
        # The object that this noun text should be controlling on the board
        # Also the object that other nouns will mutate into for NOUN IS NOUN
        self.associated_object_piece_type = associated_object_piece_type

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


class SkullObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(asset_name="object_skull.png")

    def __repr__(self) -> str:
        return "SkullObjectPieceType"


class BabaTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_name="text_baba.png",
            associated_object_piece_type=BabaObjectPieceType,
        )

    def __repr__(self) -> str:
        return "BabaTextPieceType"


class FlagTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_name="text_flag.png",
            associated_object_piece_type=FlagObjectPieceType,
        )

    def __repr__(self) -> str:
        return "FlagTextPieceType"


class TextTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_name="text_text.png", associated_object_piece_type=TextPieceType
        )

    def __repr__(self) -> str:
        return "TextTextPieceType"


class RockTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_name="text_rock.png",
            associated_object_piece_type=RockObjectPieceType,
        )

    def __repr__(self) -> str:
        return "RockTextPieceType"


class WallTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_name="text_wall.png",
            associated_object_piece_type=WallObjectPieceType,
        )

    def __repr__(self) -> str:
        return "WallTextPieceType"


class SkullTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_name="text_skull.png",
            associated_object_piece_type=SkullObjectPieceType,
        )

    def __repr__(self) -> str:
        return "SkullTextPieceType"


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


class DefeatTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(asset_name="text_defeat.png")

    def __repr__(self) -> str:
        return "DefeatTextPieceType"
