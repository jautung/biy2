from mappiece import MapPiece
from movedirection import MoveDirection


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


    def generate_rules(self):
        # TODO
        return []


    def execute_move(self, direction: MoveDirection):
        # TODO: Only affect pieces that are you, based on rules
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
