from typing import Type
import inspect
import os

from level import Level
from map import Map
from mappiece import MapPiece
from pieceposition import PiecePosition
from piecetype import *
from window import Window


LEVEL_FILENAME_EXTENSION = "txt"
TITLE_PREFIX = "Title: "
ROWS_PREFIX = "Rows: "
COLUMNS_PREFIX = "Columns: "


def get_level_by_name(
    level_name: str, window: Window, levels_directory: str, assets_directory: str
) -> Level:
    name_to_piece_type_dict = _get_name_to_piece_type_dict()
    filename = os.path.join(
        levels_directory, f"{level_name}.{LEVEL_FILENAME_EXTENSION}"
    )
    with open(filename) as file:
        lines = [line.strip("\n") for line in file.readlines()]
        assert len(lines) >= 3
        title = _get_data_from_prefixed_line(line=lines[0], prefix=TITLE_PREFIX)
        number_rows = int(
            _get_data_from_prefixed_line(line=lines[1], prefix=ROWS_PREFIX)
        )
        number_columns = int(
            _get_data_from_prefixed_line(line=lines[2], prefix=COLUMNS_PREFIX)
        )
        return Level(
            title=title,
            window=window,
            map=Map(
                number_rows=number_rows,
                number_columns=number_columns,
                map_pieces=_get_map_pieces(
                    lines=lines[3:], name_to_piece_type_dict=name_to_piece_type_dict
                ),
            ),
            assets_directory=assets_directory,
        )


def _get_data_from_prefixed_line(line: str, prefix: str) -> str:
    assert line.startswith(prefix)
    return line[len(prefix) :]


def _get_map_pieces(
    lines: list[str], name_to_piece_type_dict: dict[str, Type[PieceType]]
) -> set[MapPiece]:
    map_pieces = set()
    current_piece_type: Type[PieceType] = None
    for line in lines:
        if line == "":
            continue
        line_split = line.split()
        if len(line_split) == 1:
            piece_name = line_split[0]
            current_piece_type = name_to_piece_type_dict[piece_name]
        else:
            piece_attributes = line_split
            x = int(piece_attributes[0])
            y = int(piece_attributes[1])
            map_pieces.add(
                MapPiece(
                    position=PiecePosition(x=x, y=y), piece_type=current_piece_type()
                )
            )
    return map_pieces


def _get_name_to_piece_type_dict() -> dict[str, Type[PieceType]]:
    name_to_piece_type_dict: dict[str, Type[PieceType]] = {}

    def add_piece_type_subclasses_to_name_to_piece_type_dict(
        piece_type: Type[PieceType],
    ):
        # We only care about concrete classes that can be instantiated with PieceType(),
        # and not the PieceType, ObjectPieceType, etc. super-classes
        if len(inspect.signature(piece_type.__init__).parameters) == 1:
            name_to_piece_type_dict[piece_type().stored_levels_repr()] = piece_type
        for subclass_piece_type in piece_type.__subclasses__():
            add_piece_type_subclasses_to_name_to_piece_type_dict(subclass_piece_type)

    add_piece_type_subclasses_to_name_to_piece_type_dict(PieceType)
    return name_to_piece_type_dict
