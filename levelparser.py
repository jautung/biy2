from typing import Type
import inspect
import json
import os

from level import Level
from map import Map
from mappiece import MapPiece
from pieceposition import PiecePosition
from piecetype import *
from window import Window


def get_level_by_name(
    level_name: str, window: Window, levels_directory: str, assets_directory: str
) -> Level:
    name_to_piece_type_dict = _get_name_to_piece_type_dict()
    filename = os.path.join(levels_directory, f"{level_name}.json")
    with open(filename) as file:
        data = json.load(file)
        return Level(
            title=data["title"],
            window=window,
            map=Map(
                number_rows=data["rows"],
                number_columns=data["columns"],
                map_pieces=set(
                    [
                        MapPiece(
                            position=PiecePosition(
                                x=piece["x"],
                                y=piece["y"],
                            ),
                            piece_type=name_to_piece_type_dict[piece["type"]](),
                        )
                        for piece in data["pieces"]
                    ]
                ),
            ),
            assets_directory=assets_directory,
        )


def _get_name_to_piece_type_dict() -> dict[str, Type[PieceType]]:
    name_to_piece_type_dict: dict[str, Type[PieceType]] = {}

    def add_piece_type_subclasses_to_name_to_piece_type_dict(
        piece_type: Type[PieceType],
    ):
        # We only care about concrete classes that can be instantiated with PieceType(),
        # and not the PieceType, ObjectPieceType, etc. super-classes
        if len(inspect.signature(piece_type.__init__).parameters) == 1:
            name_to_piece_type_dict[piece_type().json_repr()] = piece_type
        for subclass_piece_type in piece_type.__subclasses__():
            add_piece_type_subclasses_to_name_to_piece_type_dict(subclass_piece_type)

    add_piece_type_subclasses_to_name_to_piece_type_dict(PieceType)
    return name_to_piece_type_dict
