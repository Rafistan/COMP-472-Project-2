import numpy as np
from gbfs import GBFS
from aStar import AStar
from ucs import UCS
from game import Game

with open('input.txt') as f:
    lines = f.readlines()

puzzle_number = 2

for line in lines:
    board = np.empty((6, 6), dtype=str)
    unique_cars_in_game = []
    car_gas = {}
    car_orientation = {}
    car_size = {}

    line_content = line.split(' ')
    puzzle = line_content[0].replace('\n', '').strip()
    # Check if line is not a puzzle or not an uncommented puzzle
    if "#" in puzzle or line.isspace():
        continue
    else:
        # Populate the board
        for index, char in enumerate(puzzle):
            board[(int(index / 6) % 6), (index % 6)] = char

        unique_cars_in_game = set(puzzle)
        unique_cars_in_game.remove('.')

        # Take gas info per car if it exists and loop through it to give the car the gas value
        gas_indication_list = line_content[1:]
        for initial_car_gas in gas_indication_list:
            car = initial_car_gas[0]
            gas = int(initial_car_gas[1])
            car_gas[car] = gas

    # Assign gas value to the rest of the cars
    for car in unique_cars_in_game:
        if car not in car_gas.keys():
            car_gas[car] = 100

    # Assign orientations of the cars
    for car in unique_cars_in_game:
        # https://stackoverflow.com/questions/55870144/how-i-can-get-the-indexes-of-numpy-array-that-contain-ones
        indices_of_car_in_board = np.argwhere(board == car)
        car_size[car] = max(indices_of_car_in_board.shape)
        first_column = indices_of_car_in_board[0][1]
        second_column = indices_of_car_in_board[1][1]
        # By using argwhere, we can tell by the way that the columns match or
        # not whether they're aligned horizontally or vertically
        if first_column == second_column:
            car_orientation[car] = "v"
        else:
            car_orientation[car] = "h"

    # Execute UCS, GBFS & AStar with all 4 heuristics
    game: Game = Game(board, car_gas, car_orientation, car_size)
    print(f"Puzzle #{puzzle_number}")
    UCS(game, puzzle_number)
    GBFS(game, 1, puzzle_number)
    GBFS(game, 2, puzzle_number)
    GBFS(game, 3, puzzle_number)
    GBFS(game, 4, puzzle_number)
    AStar(game, 1, puzzle_number)
    AStar(game, 2, puzzle_number)
    AStar(game, 3, puzzle_number)
    AStar(game, 4, puzzle_number)

    puzzle_number += 1
