from Board import *
from  Game import *
from PolicyValueNet import *
import pickle
from collections import deque

# Global Variable
root_data_file = "data/"
tmp_data_file = "tmp/"

class Config:
    def __init__(self):
        self.board_width = 6
        self.board_height = 6
        self.n_in_row = 4
        self.board = Board(width=self.board_width, height=self.board_height, n_in_row=self.n_in_row)
        self.game = Game(self.board)
        # training params
        self.learn_rate = 2e-3
        self.lr_multiplier = 1.0  # adaptively adjust the learning rate based on KL
        self.lr_decay_per_iterations = 100  # learning rate decay after how many iterations
        self.lr_decay_speed = 5  # learning rate decay speed
        self.temp = 1.0  # the temperature param
        self.n_playout = 400  # num of simulations for each move
        self.c_puct = 5
        self.buffer_size = 10000
        self.batch_size = 512  # mini-batch size for training
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.play_batch_size = 1  # how many games of each self-play epoch
        self.per_game_opt_times = 5  # num of train_steps for each update
        self.is_adjust_lr = True  # whether dynamic changing lr
        self.kl_targ = 0.02  # KL，用于early stop
        self.check_freq = 30  # frequency of checking the performance of current model and saving model
        self.start_game_num = 0  # the starting num of training
        self.game_batch_num = 1500
        # num of simulations used for the pure mcts, which is used as the opponent to evaluate the trained policy
        self.pure_mcts_playout_num = 1000

        # New Added Parameters
        self.network = ResNet  # the type of network
        self.policy_param = None  # Network parameters
        self.loss_records = [] # loss records
        self.best_win_pure_so_far = 0.0 # win ratio against rollout mcts player
        self.continuous_win_pure_times = 0 # the time of continuous winning against rollout mcts player
        self.change_opponent_continuous_times = 3 # time when change evaluate opponent from Pure to AlphaZero
        self.win_ratio_alphazero = 0.55 # if win ratio against previous best alphazero is larger than 0.55 then it is ok to save
        self.cur_best_alphazero_store_filename = None # the current best AlphaZero Player
        self.evaluate_opponent = 'Pure' # The opponent to evaluate. Pure Opponent at the beginning of training, when beat pure opponent many times, then change to Previous Best AlphaZero Player
