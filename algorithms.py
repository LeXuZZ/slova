# coding=utf-8
from random import choice, shuffle, sample
from addict import Dict
__author__ = 'lxz'

class STATIC():
    WORDS = ['HELLO', 'BUNNY', 'ADDICT']
    OUT_OF_GRID = 'OUT_OF_GRID'
    EMPTY_CELL_LETTER = '0'
    GAME_DIMENSIONS = 5


def check_grid_for_ability_to_enter_3letter_words(grid):
    all_empty_cells = []
    for row in grid:
        for cell in grid[row]:
            if cell.letter == STATIC.EMPTY_CELL_LETTER:
                if cell.up is None and cell.down is None and cell.left is None and cell.right is None:
                    print 'cell with no move is {0}'.format(cell.id)
                    return False
                else:
                    all_empty_cells.append(cell)

    print [cell.id + ': {0}, {1}, {2}, {3}'.format(cell.up, cell.down, cell.left, cell.right) for cell in all_empty_cells]


def add_word_to_grid():
    pass


class smart_cell():
    def __init__(self, row, cell, game_dimensions=STATIC.GAME_DIMENSIONS):
        self.id = '{0}-{1}'.format(row, cell)
        self.letter = STATIC.EMPTY_CELL_LETTER
        self.flag = None
        self.up = '{0}-{1}'.format(row - 1, cell) if row != 0 else None
        self.down = '{0}-{1}'.format(row + 1, cell) if row != game_dimensions - 1 else None
        self.left = '{0}-{1}'.format(row, cell - 1) if cell != 0 else None
        self.right = '{0}-{1}'.format(row, cell + 1) if cell != game_dimensions - 1 else None
        pass


def create_smart_grid(game_dimensions=STATIC.GAME_DIMENSIONS):
    smart_grid = Dict()
    for dimension in xrange(game_dimensions):
        smart_grid[dimension] = []
    for row in smart_grid:
        smart_grid[row] = [smart_cell(row, cell) for cell in xrange(game_dimensions)]
    return smart_grid


def search_cell_in_grid(cell_id, grid):
    for row in grid:
        for cell in grid[row]:
            if cell.id == cell_id:
                return cell
    return STATIC.OUT_OF_GRID

def delete_move_ability(cell, move_to_cell_id):
    if cell.up == move_to_cell_id:
        print 'cell {1} move to {0} deleted'.format(cell.id, cell.up)
        cell.up = None
    if cell.down == move_to_cell_id:
        print 'cell {1} move to {0} deleted'.format(cell.id, cell.down)
        cell.down = None
    if cell.left == move_to_cell_id:
        print 'cell {1} move to {0} deleted'.format(cell.id, cell.left)
        cell.left = None
    if cell.right == move_to_cell_id:
        print 'cell {1} move to {0} deleted'.format(cell.id, cell.right)
        cell.right = None


def _delete_move_ability_to(cell):
    if cell.up is not None:
        search_cell_in_grid(cell.up, grid).down = None
    if cell.down is not None:
        search_cell_in_grid(cell.down, grid).up = None
    if cell.left is not None:
        search_cell_in_grid(cell.left, grid).right = None
    if cell.right is not None:
        search_cell_in_grid(cell.right, grid).left = None

def fill_a_word_to_grid(word, start_cell_id, grid):
    splitted_word = list(word)
    start_cell = search_cell_in_grid(start_cell_id, grid)
    start_cell.letter = splitted_word[0]
    previous_cell = start_cell
    for letter in splitted_word[1:]:
        print previous_cell.id
        moves_list = [previous_cell.up, previous_cell.down, previous_cell.left, previous_cell.right]
        if len(set(moves_list)) <= 1:
            print 'NO WAY!!1'
            break
        moves_list = sample(moves_list, len(moves_list))
        move_to_cell_id = None
        for _move in moves_list:
            if _move is not None:
                if search_cell_in_grid(_move, grid) != STATIC.OUT_OF_GRID:
                    if search_cell_in_grid(_move, grid).letter is STATIC.EMPTY_CELL_LETTER:
                        move_to_cell_id = _move
                        print 'moves to ' + str(move_to_cell_id)
                        # delete_move_ability(search_cell_in_grid(move_to_cell_id, grid), previous_cell.id)
                        _delete_move_ability_to(search_cell_in_grid(previous_cell.id, grid))
                        break
        print_grid_to_console(grid)
        move_to_cell = search_cell_in_grid(move_to_cell_id, grid)
        move_to_cell.letter = letter
        previous_cell = move_to_cell
    _delete_move_ability_to(previous_cell)
    return grid


def print_grid_to_console(grid):
    for row in grid:
        for cell in grid[row]:
            print str(cell.letter) + ' ',
        print '\r\n'
    print '============='


def run_algo():
    pass


if __name__ == "__main__":
    grid = create_smart_grid()
    needed_cell = search_cell_in_grid('0-4', grid)
    new_grid = fill_a_word_to_grid(STATIC.WORDS[0], '2-1', grid)
    print_grid_to_console(new_grid)
    print check_grid_for_ability_to_enter_3letter_words(new_grid)
    pass