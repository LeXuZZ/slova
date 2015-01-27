from algorithms import check_grid_for_ability_to_enter_3letter_words, smart_cell, create_smart_grid
import random

#rewrite test with static grid to use assert function
grid = create_smart_grid()
for i in grid:
    for letter in grid[i]:
        letter.letter = random.choice((1, 1, 1, '0'))

for rec in grid:
    print(grid[rec][0].letter, grid[rec][1].letter, grid[rec][2].letter, grid[rec][3].letter, grid[rec][4].letter)

print(check_grid_for_ability_to_enter_3letter_words(grid))