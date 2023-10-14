from map import Map
from window import Window


MINIMUM_WINDOW_PADDING_SIZE = 50


def calculate_cell_size(window: Window, map: Map):
    max_cell_size_horizontal = (window.width - 2 * MINIMUM_WINDOW_PADDING_SIZE) / map.number_columns
    max_cell_size_vertical = (window.height - 2 * MINIMUM_WINDOW_PADDING_SIZE) / map.number_rows
    return min(max_cell_size_horizontal, max_cell_size_vertical)


def calculate_window_paddings(window: Window, map: Map, cell_size: int):
    horizontal_padding = (window.width - map.number_columns * cell_size) / 2
    vertical_padding = (window.height - map.number_rows * cell_size) / 2
    assert(horizontal_padding >= 0)
    assert(vertical_padding >= 0)
    return (horizontal_padding, vertical_padding)
