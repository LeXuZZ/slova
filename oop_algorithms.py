from random import choice, sample
from addict import Dict

__author__ = 'lxz'


class STATIC():
    WORDS = ['DOG', 'CAT', 'REX']
    OUT_OF_GRID = 'OUT_OF_GRID'
    EMPTY_CELL_LETTER = {
        'value': '0',
        'index': None,
        'cell_id': None
    }
    _EMPTY_CELL_LETTER = '0'
    GAME_DIMENSIONS = 3



def create_smart_grid(game_dimensions=STATIC.GAME_DIMENSIONS):
    smart_grid = Dict()
    for row in xrange(game_dimensions):
        for cell in xrange(game_dimensions):
            smart_grid[row][cell] = {
                'id': (row, cell),
                'letter': STATIC.EMPTY_CELL_LETTER,
                'flag': None,
                'up': (row - 1, cell) if row != 0 else None,
                'down': (row + 1, cell) if row != game_dimensions - 1 else None,
                'left': (row, cell - 1) if cell != 0 else None,
                'right': (row, cell + 1) if cell != game_dimensions - 1 else None

            }
    return smart_grid


def delete_move_ability_to(cell):
    if cell.up is not None:
        get_cell(cell.up).down = None
    if cell.down is not None:
        get_cell(cell.down).up = None
    if cell.left is not None:
        get_cell(cell.left).right = None
    if cell.right is not None:
        get_cell(cell.right).left = None


def get_cell(cell_id):
    return grid[cell_id[0]][cell_id[1]]


def get_neighbours(cell):
    return cell.up, cell.down, cell.left, cell.right


def fill_word_to_grid(word):
    random_cell_id = (choice(xrange(STATIC.GAME_DIMENSIONS)), choice(xrange(STATIC.GAME_DIMENSIONS)))
    print 'start cell is {0}'.format(random_cell_id)
    word_letters = list(word)
    print 'word is {0}'.format(word)

    prev_cell = get_cell(random_cell_id)
    prev_cell.letter = word_letters[0]
    for letter in word_letters[1:]:
        moves_list = get_neighbours(prev_cell)
        if len(set(moves_list)) <= 1:
            print 'no moves!'
        move_to_cell_id = None
        for _move in moves_list:
            if _move is not None:
                if get_cell(_move).letter == STATIC.EMPTY_CELL_LETTER:
                    move_to_cell_id = _move
                    print 'moves to {0}'.format(_move)
                    delete_move_ability_to(prev_cell)
                    break
        move_to_cell = get_cell(move_to_cell_id)
        move_to_cell.letter = letter
        prev_cell = move_to_cell
        print_grid_to_console()


def print_grid_to_console():
    for row in grid:
        for cell in grid[row]:
            _cell = get_cell((row, cell))
            print str(_cell.letter.value) + ' ',
        print '\r\n'
    print '============='

def _print_grid_to_console():
    for row in grid:
        for cell in grid[row]:
            print str(get_cell((row, cell)).letter) + ' ',
        print '\r\n'
    print '============='


def get_start_cell_ids(num=3):
    num_of_polygons = num
    start_cells = []
    while True:
        start_cell_id = (choice(xrange(STATIC.GAME_DIMENSIONS)), choice(xrange(STATIC.GAME_DIMENSIONS)))
        if start_cell_id not in start_cells:
            start_cells.append(start_cell_id)
        if len(start_cells) == num_of_polygons:
            break
    return start_cells


def create_words_dict():
    words_dict = Dict()
    for word_num in xrange(len(STATIC.WORDS)):
        for i, letter in enumerate(STATIC.WORDS[word_num]):
            words_dict[word_num][i] = {
                'value': letter,
                'index': i,
                'cell_id': None
            }
        words_dict[word_num].full_word = STATIC.WORDS[word_num]
    return words_dict


def get_available_cell_to_move(cell):
    moves_list = get_neighbours(cell)
    if len(set(moves_list)) <= 1:
        print 'no moves!'
    move_to_cell_id = None
    for _move in moves_list:
        if _move is not None:
            if get_cell(_move).letter == STATIC.EMPTY_CELL_LETTER:
                move_to_cell_id = _move
                print 'moves to {0}'.format(_move)
                delete_move_ability_to(cell)
                break
    move_to_cell = get_cell(move_to_cell_id)
    return move_to_cell

def create_polygons(start_cell_ids):
    for i, word in enumerate(words_dict.values()):
        start_cell_id = choice(start_cell_ids)
        cell = get_cell(start_cell_id)
        cell.letter = word[0]
        word[0].cell_id = start_cell_id
        delete_move_ability_to(cell)
        words_dict[i].prev_cell_id = start_cell_id
        start_cell_ids.remove(start_cell_id)
    for w, word in enumerate(words_dict.values()):
        for l, letter in enumerate(word.full_word[1:]):
            cell = get_cell(word.prev_cell_id)
            cell_to_move = get_available_cell_to_move(cell)
            print words_dict.values()[l][w+1].value
            cell_to_move.value = words_dict.values()[l][w+1].value
            print_grid_to_console()



if __name__ == "__main__":
    grid = create_smart_grid()
    words_dict = create_words_dict()
    start_cell_ids = get_start_cell_ids()
    create_polygons(start_cell_ids)
    print_grid_to_console()
    pass