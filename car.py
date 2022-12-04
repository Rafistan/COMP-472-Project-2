import numpy as np
import copy


def can_valet(board):
    return board[2][5] == board[2][4] and board[2][5] != '.'


def remove_valet(board):
    for position in range(0, 6):
        if board[2][position] == board[2][5]:
            board[2][position] = '.'


def possible_moves(board, car_gas, car_orientation):
    # This function returns all the possible moves (of length one) possible at a state. We first look at all the
    # empty spots in the game.
    empty_positions = np.argwhere(board == ".")
    possible_moves_list = []
    # Iterate through every empty spot.
    for position in empty_positions:
        column = board[:, position[1]]

        # Check that we aren't at the top most row
        if position[0] > 0:
            position_above = column[position[0] - 1]
            # If there is a vertical car above with gas, it can move down once.
            if position_above != "." and car_orientation[position_above] == "v" and car_gas[position_above] >= 1:
                possible_moves_list.append(([position_above, "D", 1]))

        # Check that we aren't at the bottom most row.
        if position[0] < 5:
            position_below = column[position[0] + 1]
            # If there is a vertical car below with gas, it can move up once.
            if position_below != "." and car_orientation[position_below] == "v" and car_gas[
                position_below] >= 1:
                possible_moves_list.append(([position_below, "U", 1]))
        row = board[position[0]]

        # Check the position to the right as long as we aren't at the right most column.
        if position[1] < 5:
            position_to_the_right = row[position[1] + 1]
            # Check the value to the right, if it's a car that moves horizontally and has gas, it can move to
            # the left 1 position.
            if position_to_the_right != "." and car_orientation[position_to_the_right] == "h" and car_gas[
                position_to_the_right] >= 1:
                possible_moves_list.append([position_to_the_right, "L", 1])

        # Check the position to the left as long as we aren't at the left most column.
        if position[1] > 0:
            position_to_the_left = row[position[1] - 1]
            # Check the value to the left, if it's a car that moves horizontally and has gas, it can move to
            # the right 1 position.
            if position_to_the_left != '.' and car_orientation[position_to_the_left] == "h" and car_gas[
                position_to_the_left] >= 1:
                possible_moves_list.append([position_to_the_left, "R", 1])
    return possible_moves_list


def move_car(board, move_information):
    new_board = copy.deepcopy(board)

    # Depending on which direction it needs to move, we take the opposing positions of that direction and move the whole car by the desired direction.
    if move_information[1] == "D":
        car_positions = np.argwhere(board == move_information[0])
        up_position = car_positions[0]
        bottom_position = car_positions[len(car_positions) - 1]
        new_board[up_position[0], up_position[1]] = '.'
        new_board[bottom_position[0] + 1, bottom_position[1]] = move_information[0]
    elif move_information[1] == "U":
        car_positions = np.argwhere(board == move_information[0])
        up_position = car_positions[0]
        bottom_position = car_positions[len(car_positions) - 1]
        new_board[up_position[0] - 1, up_position[1]] = move_information[0]
        new_board[bottom_position[0], bottom_position[1]] = '.'
    elif move_information[1] == "L":
        car_positions = np.argwhere(board == move_information[0])
        left_position = car_positions[0]
        right_position = car_positions[len(car_positions) - 1]
        new_board[left_position[0], left_position[1] - 1] = move_information[0]
        new_board[right_position[0], right_position[1]] = '.'
    elif move_information[1] == "R":
        car_positions = np.argwhere(board == move_information[0])
        left_position = car_positions[0]
        right_position = car_positions[len(car_positions) - 1]
        new_board[left_position[0], left_position[1]] = '.'
        new_board[right_position[0], right_position[1] + 1] = move_information[0]
    return new_board
