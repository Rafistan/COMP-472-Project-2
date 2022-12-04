class Game:
    cost = 0
    last_board = []
    last_move = ""
    distance_travelled = 0

    def __init__(self, board, car_gas, car_orientation, car_size):
        self.board = board
        self.car_gas = car_gas
        self.car_orientation = car_orientation
        self.car_size = car_size

    def is_game_over(self, boardArray):
        return boardArray[2][5] == 'A' and boardArray[2][4] == 'A'
