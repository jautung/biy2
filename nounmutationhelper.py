from nounmutation import NounMutation
from piecetype import *


# Despite being similar, intentionally distinct from rules;
# rules define how things interact with each other,
# while noun mutations are just one-time mutations
def generate_noun_mutations_for_row(row: list[PieceType]) -> list[NounMutation]:
    noun_mutations: list[NounMutation] = []
    for start_index in range(len(row) - 2):
        piece_1 = row[start_index]
        piece_2 = row[start_index + 1]
        piece_3 = row[start_index + 2]
        if not isinstance(piece_1, NounTextPieceType):
            continue
        if not isinstance(piece_2, IsTextPieceType):
            continue
        if not isinstance(piece_3, NounTextPieceType):
            continue
        noun_mutations.append(
            NounMutation(
                from_object_piece_type=piece_1.associated_object_piece_type,
                to_object_piece_type=piece_3.associated_object_piece_type,
            )
        )
    return noun_mutations
