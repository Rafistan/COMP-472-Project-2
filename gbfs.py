import numpy as np
import copy
import time

import car as car_object
from game import Game
from heuristics import h1, h2, h3, h4


def GBFS(game, heuristic_number, puzzle_number):
    # start_time time
    start_time = time.time()
    # Initialize variables
    list_of_open_games = []
    list_of_closed_games = []
    present_game_board = game.board
    present_car_gas = game.car_gas
    present_game = game
    list_of_closed_games.append(game)
    # Setup paths for solutions
    solutions_path = f".\solutions\GBFS-h{heuristic_number}-sol-{puzzle_number}.txt"
    search_path = f".\search\GBFS-h{heuristic_number}-search-{puzzle_number}.txt"
    print(f"GBFS h{heuristic_number} puzzle #{puzzle_number}")
    # write solution for GBFS for the board and the gas, per heuristic, respectively
    with open(solutions_path, "w+") as solution_file:
        solution_file.write(f"{game.board}\n\n")
        solution_file.write(f"Car fuel available: {str(game.car_gas)}\n")

    # Enter game and iterate until the game is over
    while not game.is_game_over(present_game_board):
        possible_moves = car_object.possible_moves(present_game_board, present_car_gas, game.car_orientation)

        for possible_move in possible_moves:
            car_being_moved = possible_move[0]
            new_cost = present_game.cost

            new_car_gas = copy.deepcopy(present_car_gas)
            car_gas_entry_to_be_updated = {car_being_moved: new_car_gas.get(car_being_moved) - 1}
            new_car_gas.update(car_gas_entry_to_be_updated)

            new_board = car_object.move_car(present_game_board, possible_move)

            # simply add a new cost if the new direction is different from the previous direction
            # append f(n), g(n) and h(n) and the board to the file
            if not possible_move == present_game.last_move:
                if heuristic_number == 1:
                    new_cost = h1(new_board)
                    with open(search_path, "a+") as solution:
                        solution.write(
                            f"\n{new_cost}\t0\t{new_cost}\t{present_game_board[0][0:6]}{present_game_board[1][0:6]}{present_game_board[2][0:6]}{present_game_board[3][0:6]}{present_game_board[4][0:6]}{present_game_board[5][0:6]}")
                elif heuristic_number == 2:
                    new_cost = h2(new_board)
                    with open(search_path, "a+") as solution:
                        solution.write(
                            f"\n{new_cost}\t0\t{new_cost}\t{present_game_board[0][0:6]}{present_game_board[1][0:6]}{present_game_board[2][0:6]}{present_game_board[3][0:6]}{present_game_board[4][0:6]}{present_game_board[5][0:6]}")
                elif heuristic_number == 3:
                    new_cost = h3(new_board)
                    with open(search_path, "a+") as solution:
                        solution.write(
                            f"\n{new_cost}\t0\t{new_cost}\t{present_game_board[0][0:6]}{present_game_board[1][0:6]}{present_game_board[2][0:6]}{present_game_board[3][0:6]}{present_game_board[4][0:6]}{present_game_board[5][0:6]}")
                elif heuristic_number == 4:
                    new_cost = h4(new_board)
                    with open(search_path, "a+") as solution:
                        solution.write(
                            f"\n{new_cost}\t0\t{new_cost}\t{present_game_board[0][0:6]}{present_game_board[1][0:6]}{present_game_board[2][0:6]}{present_game_board[3][0:6]}{present_game_board[4][0:6]}{present_game_board[5][0:6]}")

            # We want to remove any other car other than the ambulance if its blocking the way
            if car_object.can_valet(new_board) and new_board[2][5] != 'A':
                new_board = car_object.remove_valet(new_board)

            new_game = Game(new_board, new_car_gas, game.car_orientation, game.car_size)
            new_game.cost = new_cost
            new_game.last_board = present_game_board
            new_game.last_move = possible_move

            # Check if the game is closed
            is_game_closed = False
            for closed_game in list_of_closed_games:
                if np.array_equal(closed_game.board, new_game.board):
                    is_game_closed = True

            # Check which cost is lower and use that one
            is_game_open = False
            for open_game in list_of_open_games:
                if np.array_equal(open_game.board, new_game.board):
                    if open_game.cost > new_game.cost:
                        open_game.cost = new_game.cost
                    is_game_open = True

            if not is_game_open and not is_game_closed:
                list_of_open_games.append(new_game)

        # If already_in_closed_list ends up being True, it will mean that there is no solution because the same
        # occurrence has is repeating
        already_in_closed_list = False
        for value in range(len(list_of_closed_games)):
            if np.array_equal(present_game, list_of_closed_games[value]):
                already_in_closed_list = True

        # Let the user know that no solution was found if there are no more moves left, gas left, or same board happening again
        if len(list_of_open_games) == 0 and (len(car_object.possible_moves(list_of_closed_games[len(list_of_closed_games) - 1].board, list_of_closed_games[
            len(list_of_closed_games) - 1].car_gas, game.car_orientation)) == 0 or already_in_closed_list):
            print("No Solution")
            with open(solutions_path, "w+") as solution_file:
                solution_file.write("No Solution")
            break
        lowest_cost = list_of_open_games[0].cost

        # Iterate through the list_of_open_games to find the lowest cost.
        for open_puzzle in list_of_open_games:
            if open_puzzle.cost < lowest_cost:
                lowest_cost = open_puzzle.cost

        # Create new board with the lowest cost
        puzzle_array = []
        for open_puzzle in list_of_open_games:
            if lowest_cost == open_puzzle.cost:
                puzzle_array.append(open_puzzle)

        # Add lowest cost to the list_of_closed_games and remove from the list_of_open_games
        list_of_closed_games.append(puzzle_array[0])
        list_of_open_games.remove(puzzle_array[0])
        present_game = puzzle_array[0]
        present_game_board = puzzle_array[0].board
        present_car_gas = puzzle_array[0].car_gas

    # Get last game from the list_of_closed_games
    last_game = list_of_closed_games[len(list_of_closed_games) - 1]
    moves_list = []
    search_length = len(list_of_closed_games)
    end_time = time.time()
    with open(solutions_path, "a") as solution_file:
        solution_file.write(f"\nRuntime: {end_time - start_time} seconds")
    last_board = last_game.board
    reversed_array = []
    # append to reversed_array while the shape of the last_board is still a 6x6
    while np.shape(last_game.last_board) == (6, 6):
        for i in range(len(list_of_closed_games)):
            if np.array_equal(list_of_closed_games[i].board, last_game.last_board):
                last_game = list_of_closed_games[i]
                moves_list.append(list_of_closed_games[i].last_move)
                reversed_array.append(last_game)

    # append the move to the text file with the board
    reversed_array.pop()
    solution_path_length = 0
    moves_list.remove('')
    solution_path = []
    last_move = []
    for move_list_index in range(len(moves_list)):
        if not np.array_equal(moves_list[move_list_index], last_move):
            solution_path_length = solution_path_length + 1
            solution_path.append(moves_list[move_list_index])
        else:
            solution_path[len(solution_path) - 1][2] += 1

        last_move = moves_list[move_list_index]
    with open(solutions_path, "a") as solution_file:
        solution_file.write(f"\nSearch path length: {search_length}")
        solution_file.write(f"\nSolution path length: {solution_path_length}")
        solution_file.write(f"\nSolution path: {solution_path}\n")
        for game in reversed(reversed_array):
            solution_file.write(
                f"\n{game.last_move}\t{game.board[0][0:6]}{game.board[1][0:6]}{game.board[2][0:6]}{game.board[3][0:6]}{game.board[4][0:6]}{game.board[5][0:6]}")

        solution_file.write(f"\n\n{last_board}")

    with open(f".\\analysis.txt", "a") as analysis_file:
        analysis_file.write(f"\n{puzzle_number}\t GBFS\t{heuristic_number}\t{solution_path_length}\t{search_length} \t{end_time - start_time} ")
