from movedirection import MoveDirection


class AssetSet:
    def __init__(
        self,
        up_asset_name: str,
        down_asset_name: str,
        left_asset_name: str,
        right_asset_name: str,
    ):
        self.asset_map: dict[MoveDirection, str] = {
            MoveDirection.UP: up_asset_name,
            MoveDirection.DOWN: down_asset_name,
            MoveDirection.LEFT: left_asset_name,
            MoveDirection.RIGHT: right_asset_name,
        }

    def get_asset_name(self, move_direction: MoveDirection) -> str:
        return self.asset_map[move_direction]

    @classmethod
    def from_directional_assets(
        cls,
        up_asset_name: str,
        down_asset_name: str,
        left_asset_name: str,
        right_asset_name: str,
    ):
        return cls(
            up_asset_name=up_asset_name,
            down_asset_name=down_asset_name,
            left_asset_name=left_asset_name,
            right_asset_name=right_asset_name,
        )

    @classmethod
    def from_single_default_asset(cls, default_asset_name: str):
        return cls(
            up_asset_name=default_asset_name,
            down_asset_name=default_asset_name,
            left_asset_name=default_asset_name,
            right_asset_name=default_asset_name,
        )
