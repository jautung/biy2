from movedirection import MoveDirection


def reverse_direction(direction: MoveDirection) -> MoveDirection:
    if direction == MoveDirection.UP:
        return MoveDirection.DOWN
    elif direction == MoveDirection.DOWN:
        return MoveDirection.UP
    elif direction == MoveDirection.LEFT:
        return MoveDirection.RIGHT
    elif direction == MoveDirection.RIGHT:
        return MoveDirection.LEFT
    assert False
