from assetset import AssetSet
from typing import Type


# Images at https://docs.google.com/presentation/d/1frkfoDgriNW8fC-DpAeI8oB3nAnU9JQ5UQh_VQ3LjvQ/edit


class PieceType:
    def __init__(self, asset_set: AssetSet):
        self.asset_set = asset_set

    def __repr__(self) -> str:
        return "PieceType"

    def stored_levels_repr(self) -> str:
        return self.__repr__()[: -len("PieceType")]


class ObjectPieceType(PieceType):
    def __init__(self, asset_set: AssetSet):
        super().__init__(asset_set=asset_set)

    def __repr__(self) -> str:
        return "ObjectPieceType"


class TextPieceType(ObjectPieceType):  # Technically text pieces are themselves objects!
    def __init__(self, asset_set: AssetSet):
        super().__init__(asset_set=asset_set)

    def __repr__(self) -> str:
        return "TextPieceType"

    def in_rule_repr(self) -> str:
        return self.__repr__()[: -len("TextPieceType")]


class NounTextPieceType(TextPieceType):
    def __init__(
        self,
        asset_set: AssetSet,
        associated_object_piece_type: Type[ObjectPieceType],
    ):
        super().__init__(asset_set=asset_set)
        # The object that this noun text should be controlling on the board
        # Also the object that other nouns will mutate into for NOUN IS NOUN
        self.associated_object_piece_type = associated_object_piece_type

    def __repr__(self) -> str:
        return "NounTextPieceType"


class IsTextPieceType(TextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_is.png"
            )
        )

    def __repr__(self) -> str:
        return "IsTextPieceType"


class AndTextPieceType(TextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_and.png"
            )
        )

    def __repr__(self) -> str:
        return "AndTextPieceType"


class NotTextPieceType(TextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_not.png"
            )
        )

    def __repr__(self) -> str:
        return "NotTextPieceType"


class HasTextPieceType(TextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_has.png"
            )
        )

    def __repr__(self) -> str:
        return "HasTextPieceType"


class AttributeTextPieceType(TextPieceType):
    def __init__(self, asset_set: AssetSet):
        super().__init__(asset_set=asset_set)

    def __repr__(self) -> str:
        return "AttributeTextPieceType"


class BabaObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_directional_assets(
                up_asset_name="object_baba_up.png",
                down_asset_name="object_baba_down.png",
                left_asset_name="object_baba_left.png",
                right_asset_name="object_baba_right.png",
            )
        )

    def __repr__(self) -> str:
        return "BabaObjectPieceType"


class FlagObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="object_flag.png"
            )
        )

    def __repr__(self) -> str:
        return "FlagObjectPieceType"


class RockObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="object_rock.png"
            )
        )

    def __repr__(self) -> str:
        return "RockObjectPieceType"


class WallObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="object_wall.png"
            )
        )

    def __repr__(self) -> str:
        return "WallObjectPieceType"


class SkullObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="object_skull.png"
            )
        )

    def __repr__(self) -> str:
        return "SkullObjectPieceType"


class WaterObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="object_water.png"
            )
        )

    def __repr__(self) -> str:
        return "WaterObjectPieceType"


class CrabObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="object_crab.png"
            )
        )

    def __repr__(self) -> str:
        return "CrabObjectPieceType"


class JellyObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="object_jelly.png"
            )
        )

    def __repr__(self) -> str:
        return "JellyObjectPieceType"


class BeltObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_directional_assets(
                up_asset_name="object_belt_up.png",
                down_asset_name="object_belt_down.png",
                left_asset_name="object_belt_left.png",
                right_asset_name="object_belt_right.png",
            )
        )

    def __repr__(self) -> str:
        return "BeltObjectPieceType"


class DoorObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="object_door.png"
            )
        )

    def __repr__(self) -> str:
        return "DoorObjectPieceType"


class KeyObjectPieceType(ObjectPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="object_key.png"
            )
        )

    def __repr__(self) -> str:
        return "KeyObjectPieceType"


class BabaTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_baba.png"
            ),
            associated_object_piece_type=BabaObjectPieceType,
        )

    def __repr__(self) -> str:
        return "BabaTextPieceType"


class FlagTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_flag.png"
            ),
            associated_object_piece_type=FlagObjectPieceType,
        )

    def __repr__(self) -> str:
        return "FlagTextPieceType"


class TextTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_text.png"
            ),
            associated_object_piece_type=TextPieceType,
        )

    def __repr__(self) -> str:
        return "TextTextPieceType"


class RockTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_rock.png"
            ),
            associated_object_piece_type=RockObjectPieceType,
        )

    def __repr__(self) -> str:
        return "RockTextPieceType"


class WallTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_wall.png"
            ),
            associated_object_piece_type=WallObjectPieceType,
        )

    def __repr__(self) -> str:
        return "WallTextPieceType"


class SkullTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_skull.png"
            ),
            associated_object_piece_type=SkullObjectPieceType,
        )

    def __repr__(self) -> str:
        return "SkullTextPieceType"


class WaterTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_water.png"
            ),
            associated_object_piece_type=WaterObjectPieceType,
        )

    def __repr__(self) -> str:
        return "WaterTextPieceType"


class CrabTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_crab.png"
            ),
            associated_object_piece_type=CrabObjectPieceType,
        )

    def __repr__(self) -> str:
        return "CrabTextPieceType"


class JellyTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_jelly.png"
            ),
            associated_object_piece_type=JellyObjectPieceType,
        )

    def __repr__(self) -> str:
        return "JellyTextPieceType"


class BeltTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_belt.png"
            ),
            associated_object_piece_type=BeltObjectPieceType,
        )

    def __repr__(self) -> str:
        return "BeltTextPieceType"


class DoorTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_door.png"
            ),
            associated_object_piece_type=DoorObjectPieceType,
        )

    def __repr__(self) -> str:
        return "DoorTextPieceType"


class KeyTextPieceType(NounTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_key.png"
            ),
            associated_object_piece_type=KeyObjectPieceType,
        )

    def __repr__(self) -> str:
        return "KeyTextPieceType"


class WinTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_win.png"
            )
        )

    def __repr__(self) -> str:
        return "WinTextPieceType"


class YouTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_you.png"
            )
        )

    def __repr__(self) -> str:
        return "YouTextPieceType"


class PushTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_push.png"
            )
        )

    def __repr__(self) -> str:
        return "PushTextPieceType"


class StopTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_stop.png"
            )
        )

    def __repr__(self) -> str:
        return "StopTextPieceType"


class DefeatTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_defeat.png"
            )
        )

    def __repr__(self) -> str:
        return "DefeatTextPieceType"


class SinkTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_sink.png"
            )
        )

    def __repr__(self) -> str:
        return "SinkTextPieceType"


class MoveTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_move.png"
            )
        )

    def __repr__(self) -> str:
        return "MoveTextPieceType"


class HotTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_hot.png"
            )
        )

    def __repr__(self) -> str:
        return "HotTextPieceType"


class MeltTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_melt.png"
            )
        )

    def __repr__(self) -> str:
        return "MeltTextPieceType"


class OpenTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_open.png"
            )
        )

    def __repr__(self) -> str:
        return "OpenTextPieceType"


class CloseTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_close.png"
            )
        )

    def __repr__(self) -> str:
        return "CloseTextPieceType"


class ShiftTextPieceType(AttributeTextPieceType):
    def __init__(self):
        super().__init__(
            asset_set=AssetSet.from_single_default_asset(
                default_asset_name="text_shift.png"
            )
        )

    def __repr__(self) -> str:
        return "ShiftTextPieceType"
