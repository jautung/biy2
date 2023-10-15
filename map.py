import copy

from mappiece import MapPiece
from movedirection import MoveDirection
from piecetype import PieceType, WordNounPieceType, WordIsPieceType, WordAttributePieceType, BabaObjectPieceType, FlagObjectPieceType, BabaWordPieceType, FlagWordPieceType, WinWordPieceType, YouWordPieceType


class Map:
    def __init__(self, number_rows, number_columns, pieces: list[MapPiece]):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self._init_grid(pieces)


    def _init_grid(self, pieces: list[MapPiece]):
        self.grid = [[None for _ in range(self.number_columns)] for _ in range(self.number_rows)]
        for piece in pieces:
            assert(piece.x >= 0 and piece.x < self.number_columns)
            assert(piece.y >= 0 and piece.y < self.number_rows)
            self.grid[piece.y][piece.x] = piece.piece_type


    def get_pieces(self) -> list[MapPiece]:
        pieces = []
        for column_index, row in enumerate(self.grid):
            for row_index, piece_type in enumerate(row):
                if piece_type is not None:
                    pieces.append(
                        MapPiece(
                            x=row_index,
                            y=column_index,
                            piece_type=piece_type
                        )
                    )
        return pieces


    def _generate_rules_for_grid(self):
        row_rules = [self._generate_rules_for_row(row) for row in self.grid]
        column_rules = [self._generate_rules_for_row([self.grid[row_index][column_index] for row_index in range(self.number_rows)]) for column_index in range(self.number_columns)]
        print(row_rules + column_rules)
        return row_rules + column_rules


    def _generate_rules_for_row(self, row: list[PieceType]):
        rules = []
        for start_index in range(len(row)):
            length = self._generate_logest_possible_rule_given_start(row[start_index:])
            if length is None:
                continue
            rules.append(copy.deepcopy(row[start_index:start_index+length]))
        return rules


    def _generate_logest_possible_rule_given_start(self, row: list[PieceType]):
        # TODO: Incorporate 'NOT', 'AND', etc. etc.
        if row[0] is not WordNounPieceType:
            return None
        if len(row) <= 1 or row[1] is not WordIsPieceType:
            return None
        if len(row) <= 2 or row[2] is not WordAttributePieceType:
            return None
        return 3


    def execute_move(self, direction: MoveDirection):
        # TODO: Only affect pieces that are you, based on rules
        rules = self._generate_rules_for_grid()
        for piece in self.get_pieces():
            if direction == MoveDirection.UP:
                piece.y += 1
            elif direction == MoveDirection.DOWN:
                piece.y -= 1
            elif direction == MoveDirection.LEFT:
                piece.x -= 1
            elif direction == MoveDirection.RIGHT:
                piece.x += 1
            elif direction == MoveDirection.WAIT:
                pass
