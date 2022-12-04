import numpy as np


def h1(board):
    blocking_vehicles = []
    # Position of the ambulance
    right_ambulance_position = np.argwhere(board[2] == 'A')[1][0]
    # Iterate through all of the positions in front of the ambulance and see if a car is blocking it or not, no repeat values
    for x in range(right_ambulance_position, 6):
        if board[2][x] != '.' and board[2][x] not in blocking_vehicles:
            blocking_vehicles.append(board[2][x])
    # Return the number of cars in front of the ambulance
    return len(blocking_vehicles)


def h2(board):
    # List keeping track of all the blocked positions
    blocked_positions = []
    right_ambulance_position = np.argwhere(board[2] == 'A')[1][0]
    # Iterate through all the positions in front of the ambulance and see if it is occupied or not.
    for x in range(right_ambulance_position, 6):
        if board[2][x] != '.':
            blocked_positions.append(board[2][x])
    # Return the number of blocked positions in front of the ambulance.
    return len(blocked_positions)


def h3(board):
    # We're using theta as 2
    return 2 * h1(board)


def h4(board):
    number_of_empty_spots = 0
    right_ambulance_position = np.argwhere(board[2] == 'A')[1][0]
    for x in range(right_ambulance_position, 6):
        if board[2][x] == '.':
            number_of_empty_spots += 1
    return number_of_empty_spots
