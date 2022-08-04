from termo_solver import Solver
from web_interact import play_termo

if __name__ == '__main__':
    game = Solver()
    max_attempts = 6
    word_len = 5
    play_termo(game, max_attempts, word_len)
