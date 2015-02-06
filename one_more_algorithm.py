from Queue import Queue
from random import choice, sample
from addict import Dict
import itertools
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta

__author__ = 'lxz'

def gen_words(words_num, grid_num):
    words_list = []
    words_len = grid_num * grid_num
    random_word_len = lambda: choice(range(5, 14))
    for word in xrange(words_num):
        if words_len > 10:
            stub_word = str(word) * random_word_len()
            words_len -= len(stub_word)
            words_list.append(stub_word)
        else:
            stub_word = str(word) * words_len
            words_list.append(stub_word)
    return words_list


class STATIC():
    # WORDS6x6 = ['VILKA', 'FARS', 'NOS', 'DAMBA', 'KOLESO', 'OBNOVA', 'MOLOTOK']
    WORDS6x6 = ['00000', '1111', '222', '33333', '444444', '555555', '6666666']
    WORDS8x8 = ['000000000', '111111111', '222222222', '33333333333', '4444444444', '555555555', '6666666', '7777777', '8888888', '9999999']
    WORDS3x3 = ['DOG', 'CAT', 'REX']
    OUT_OF_GRID = 'OUT_OF_GRID'
    EMPTY_CELL_LETTER = {
        'value': 'X',
        'index': None,
        'cell_id': None
    }
    _EMPTY_CELL_LETTER = 'X'
    GAME_DIMENSIONS = 8


class OMA():
    def __init__(self):
        self.grid = self.create_smart_grid()


    def create_smart_grid(self, game_dimensions=STATIC.GAME_DIMENSIONS):
        smart_grid = Dict()
        for row in xrange(game_dimensions):
            for cell in xrange(game_dimensions):
                smart_grid[row][cell] = {
                    'id': (row, cell),
                    'letter': STATIC.EMPTY_CELL_LETTER,
                    'flag': None,
                    'up': {'move_id': (row - 1, cell) if row != 0 else None, 'can_move': True},
                    'down': {'move_id': (row + 1, cell) if row != game_dimensions - 1 else None, 'can_move': True},
                    'left': {'move_id': (row, cell - 1) if cell != 0 else None, 'can_move': True},
                    'right': {'move_id': (row, cell + 1) if cell != game_dimensions - 1 else None, 'can_move': True}
                }
        return smart_grid


    def get_cell(self, cell_id):
        return self.grid[cell_id[0]][cell_id[1]]


    def print_grid_to_console(self):
        for row in self.grid:
            for cell in self.grid[row]:
                _cell = self.get_cell((row, cell))
                print str(_cell.letter.value) + ' ',
            print '\r\n'
        print '===' * STATIC.GAME_DIMENSIONS


    def get_neighbours(self, cell):
        return cell.up, cell.down, cell.left, cell.right


    def is_cell_empty(self, cell):
        if cell is not None:
            if cell.letter.value == STATIC._EMPTY_CELL_LETTER:
                return True
            else:
                return False
        else:
            return False


    #
    # def fill_random_word(start_cell, word):
    # counter = 0
    # queue = Queue()
    # start_cell.letter.value = word[counter]
    # counter += 1
    #     queue.put([start_cell])
    #
    #     while not queue.empty():
    #
    #         path = queue.get()
    #         cell = path[-1]
    #
    #         if len(word) == counter+1:
    #             return path
    #
    #         for neighbour_cell in get_neighbours(cell):
    #             if neighbour_cell is None:
    #                 continue
    #             else:
    #                 neighbour_cell = get_cell(neighbour_cell)
    #             if is_cell_empty(neighbour_cell):
    #                 neighbour_cell.letter.value = word[counter]
    #                 counter += 1
    #                 new_path = list(path)
    #                 new_path.append(neighbour_cell)
    #                 queue.put(new_path)
    #                 print_grid_to_console()


    def create_start_cell(self):
        while True:
            start_cell_id = (choice(xrange(STATIC.GAME_DIMENSIONS)), choice(xrange(STATIC.GAME_DIMENSIONS)))
            start_cell = self.get_cell(start_cell_id)
            if start_cell.letter.value == STATIC._EMPTY_CELL_LETTER:
                return start_cell_id


    def delete_move_ability_to(self, cell):
        # print 'deleting cell {} neighbours'.format(cell.id)
        if cell.up is not None:
            _tmp_cell = self.get_cell(cell.up)
            _tmp_cell.down = None
            # print 'cell {} down move to {} deleted'.format(_tmp_cell.id, cell.id)
        if cell.down is not None:
            _tmp_cell = self.get_cell(cell.down)
            _tmp_cell.up = None
            # print 'cell {} up move to {} deleted'.format(_tmp_cell.id, cell.id)
        if cell.left is not None:
            _tmp_cell = self.get_cell(cell.left)
            _tmp_cell.right = None
            # print 'cell {} right move to {} deleted'.format(_tmp_cell.id, cell.id)
        if cell.right is not None:
            _tmp_cell = self.get_cell(cell.right)
            _tmp_cell.left = None
            # print 'cell {} left move to {} deleted'.format(_tmp_cell.id, cell.id)


    def _delete_move_ability_to(self, cell):
        # print 'deleting neighbours moves to cell {}'.format(cell.id)
        if cell.up.move_id is not None:
            self.get_cell(cell.up.move_id).down.can_move = False
        if cell.down.move_id is not None:
            self.get_cell(cell.down.move_id).up.can_move = False
        if cell.left.move_id is not None:
            self.get_cell(cell.left.move_id).right.can_move = False
        if cell.right.move_id is not None:
            self.get_cell(cell.right.move_id).left.can_move = False


    def _add_move_ability_to(self, cell):
        if cell.up.move_id is not None:
            self.get_cell(cell.up.move_id).down.can_move = True
        if cell.down.move_id is not None:
            self.get_cell(cell.down.move_id).up.can_move = True
        if cell.left.move_id is not None:
            self.get_cell(cell.left.move_id).right.can_move = True
        if cell.right.move_id is not None:
            self.get_cell(cell.right.move_id).left.can_move = True

    def set_letter_to_cell(self, letter, cell_id):
        cell = self.get_cell(cell_id)
        cell.letter.value = letter
        self._delete_move_ability_to(cell)


    def set_letter_to_random_neighbour_cell(self, letter, cell_id):
        has_moves = self.cell_has_moves(cell_id)
        if has_moves:
            self.set_letter_to_cell(letter, has_moves)
        return has_moves


    def cell_has_moves(self, cell_id):
        neighbours = self.get_neighbours(self.get_cell(cell_id))
        neighbours = filter(lambda neighbour: neighbour.can_move is True and neighbour.move_id is not None, neighbours)
        if len(neighbours) == 0:
            return False
        else:
            move_to_cell_id = choice(neighbours).move_id
            return move_to_cell_id


    def get_cell_id_with_moves(self, list_of_cell_ids):
        list_of_cell_ids = sample(list_of_cell_ids, len(list_of_cell_ids))
        for cell_id in list_of_cell_ids:
            if self.cell_has_moves(cell_id):
                return cell_id
            else:
                pass
        return False


    def is_empty_cells_in_grid(self):
        for row in self.grid:
            for cell in self.grid[row]:
                _cell = self.get_cell((row, cell))
                if _cell.letter.value == STATIC._EMPTY_CELL_LETTER:
                    return True
        return False


    def count_polygons(self):
        polygons = {}
        for row in self.grid:
            for cell in self.grid[row]:
                _cell = self.get_cell((row, cell))
                if _cell.letter.value in polygons:
                    polygons[_cell.letter.value] += 1
                else:
                    polygons[_cell.letter.value] = 1
        print 'result of generating polygons'
        for polygon in polygons.keys():
            print 'polygon {} has {} letters'.format(polygon, polygons[polygon])
        return polygons

    def generate_field(self, num_of_polygons):
        polygons_list = [[] for polygon in xrange(num_of_polygons)]
        for i, polygon in enumerate(polygons_list):
            start_cell = self.create_start_cell()
            self.set_letter_to_cell(str(i), start_cell)
            polygons_list[i].append(start_cell)
        # print_grid_to_console()
        for i, polygon in itertools.cycle(enumerate(polygons_list)):
            cell_id = self.get_cell_id_with_moves(polygon)
            if cell_id:
                new_cell = self.set_letter_to_random_neighbour_cell(str(i), cell_id)
                polygons_list[i].append(new_cell)
            else:
                if self.is_empty_cells_in_grid():
                    continue
                else:
                    break
            pass

    def fill_word(self, word):
        word_indexes = []
        for letter in word:
            if len(word_indexes) == 0:
                cell_id = self.create_start_cell()
                self.set_letter_to_cell(letter, cell_id)
                word_indexes.append(cell_id)
            else:
                if word_indexes[-1] is False:
                    return word_indexes
                cell_id = self.set_letter_to_random_neighbour_cell(letter, word_indexes[-1])
                word_indexes.append(cell_id)
        return word_indexes

    def check_not_separated(self, cell_id, checked_cells=None):
        # print 'checking {}'.format(cell_id)
        if not checked_cells:
            checked_cells = []
        neighbours = self.get_neighbours(self.get_cell(cell_id))
        neighbours = filter(lambda
                                neighbour: neighbour.can_move is True and neighbour.move_id is not None and neighbour.move_id not in checked_cells,
                            neighbours)
        if len(neighbours) != 0:
            for neighbour in neighbours:
                checked_cells.append(neighbour.move_id)
                self.check_not_separated(neighbour.move_id, checked_cells)
        return checked_cells

    def get_all_empty_cells(self):
        empty_cells = []
        for row in self.grid:
            for cell in self.grid[row]:
                _cell = self.get_cell((row, cell))
                if _cell.letter.value == STATIC._EMPTY_CELL_LETTER:
                    empty_cells.append(_cell.id)
        return empty_cells

    def has_grid_united(self):
        res1 = self.check_not_separated(self.create_start_cell())
        res2 = self.get_all_empty_cells()
        if set(res1) == set(res2):
            return True
        else:
            return False

    def has_grid_cells_with_cell_with_one_neighbour(self):
        cells_with_one_neighbour = []
        for row in self.grid:
            for cell in self.grid[row]:
                _cell = self.get_cell((row, cell))
                if _cell.letter.value == STATIC._EMPTY_CELL_LETTER:
                    neighbours = self.get_neighbours(_cell)
                    neighbours = filter(lambda neighbour: neighbour.can_move is True and neighbour.move_id is not None,
                                        neighbours)
                    if len(neighbours) == 1:
                        cells_with_one_neighbour.append(_cell.id)
        if len(cells_with_one_neighbour) > 1:
            return False
        return True


    def revert_word(self, word_indexes):
        for index in word_indexes:
            cell = self.get_cell(index)
            cell.letter.value = STATIC._EMPTY_CELL_LETTER
            self._add_move_ability_to(cell)

    def reset_grid(self):
        self.grid = self.create_smart_grid()


    def ggenerate_field(self, words=STATIC.WORDS8x8):
        words_indexes = []
        words = sorted(words, key=len, reverse=True)
        words = [{'word': word, 'added': False} for word in words]
        # for word in words:
        counter = 0
        while len(self.get_all_empty_cells()) != 0:
            counter += 1
            if self.has_grid_united():
                    # and self.has_grid_cells_with_cell_with_one_neighbour():
                # self.print_grid_to_console()
                word = next(word for word in words if word['added'] is False)
                _tmp_indexes = self.fill_word(word['word'])
                if _tmp_indexes[-1] is not False:
                    words_indexes.append(_tmp_indexes)
                    word['added'] = True
                else:
                    del _tmp_indexes[-1]
                    self.revert_word(_tmp_indexes)
                    word['added'] = False
                    # print 'NO WAY'
                    # self.print_grid_to_console()
            else:
                self.revert_word(words_indexes[-1])
                words_indexes.remove(words_indexes[-1])
                word = next(word for word in reversed(words) if word['added'] is True)
                word['added'] = False
                # self.print_grid_to_console()
            if counter > 250:
                self.reset_grid()
                self.ggenerate_field()
        print counter
        # self.print_grid_to_console()
        print


if __name__ == "__main__":
    # print(gen_words(10, 8))
    all_startTime = datetime.now()
    all_times = []
    for x in xrange(1000):
        oma = OMA()
        startTime = datetime.now()
        oma.ggenerate_field()
        _time = datetime.now() - startTime
        all_times.append(_time)
        print _time
    print datetime.now() - all_startTime
    all_times = sorted(all_times)
    print 'average time: ' + str(sum(all_times, timedelta()) / len(all_times))
    print 'shortest time: ' + str(all_times[0])
    print 'longest time: ' + str(all_times[-1])