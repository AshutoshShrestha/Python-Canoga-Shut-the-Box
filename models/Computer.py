from models.Player import Player

class Computer(Player):
    # Function Name: __init__
    # Purpose: To initialize the Computer class 
    # Parameters:
    #             
    # Return Value: none (void)
    # Algorithm:
    #             1) Initialize name, helper and latest_log
    # Assistance Received: none 
    def __init__(self, name):
        self.name = name
        self.helper = False
        self.latest_log=""

    # Function Name: set_opponent
    # Purpose: To set the opponent player for a computer player
    # Parameters:
    #           opp, a Player type pointer. It holds the info of an
    #			the opponent player.  
    # Return Value: none (void)
    # Assistance Received: none 
    def set_opponent(self, opponent):
        self.opponent = opponent
    
    # Function Name: choose_a_move
    # Purpose: To select a move for the Computer player 
    # Parameters:
    #             cover_options, a list of all cover options available for
    #             a player for a given dice roll value\
    #             uncover_options, a list of all uncover options available for
    #             a player for a given dice roll value
    # Return Value: player_moves, a list of moves selected by the computer
    # Algorithm:
    #             1) Check if cover_options and uncover_options have values in them.
    #             2) Call the find_best_move after checking whether cover_options and
    #             uncover options have value in them or not and save them in player_moves
	#		      3) Return player_moves.
    # Assistance Received: none 
    def choose_a_move(self, cover_options, uncover_options):
        player_moves = []
        if cover_options and uncover_options:
            # find best possible move from available cover and available uncover moves		
            if self.cover_or_uncover():
                player_moves = self.find_best_move(cover_options, True)
            else:
                player_moves = self.find_best_move(uncover_options, False)

        elif cover_options and not uncover_options:
            # find best possible move from available cover moves
            self.latest_log += "Because there are no available moves to uncover, "
            player_moves = self.find_best_move(cover_options, True)

        elif uncover_options and not cover_options:
            # find best possible move from available uncover moves
            self.latest_log += "Because there are no available moves to cover, "
            player_moves = self.find_best_move(uncover_options, False)
        
        return player_moves

    # Function Name: find_best_move
    # Purpose: To find and return the best move from all available moves. 
    # Parameters:
    #           moves, list of moves out of which best move has to be selected
    #           to_cover, an indicator that tells whether the moves are for 
    #           covering or uncovering  
    # Return Value: best_move, returns the best move out of all passed moves
    # Algorithm:
    #             1) Iterate through the moves list to find the move with the largest
	#               number in it.
	#             2) If two moves in the moves list has the same largest number, then
	#          		 pick the one with the smaller size, since the list with the smaller
    #                size will have the larger numbers than the list with bigger size.
	#             3) If this instance of the Computer class is a helper, then use the
	#                appropriate words a helper would use. And likewise if this instance is a
    #                Computer player.
    # Assistance Received: none 
    def find_best_move(self, moves, to_cover):
        # an int variable to hold the maximum numbered square from all combinations
        best_move = []
        max_square = 1
        for move in moves:
            for tile in move:
                # picking the move with the largest value of square
                if tile > max_square:
                    max_square = tile
                    best_move = move
                # if two combinations have same largest square, then pick the combination with smaller size
                elif tile == max_square:
                    if len(move) < len(best_move):
                        best_move = move
        log_msg = ""
        if self.helper:
            log_msg += "you should probably "
        else:
            log_msg += self.name + " decided to "

        if to_cover: 
            log_msg += "cover "
        else:
            log_msg += "uncover "

        log_msg += "( "
        for tile in best_move:
            log_msg += str(tile) + " "
        log_msg += ") "


        if to_cover:
            best_move.insert(0, 0)
        else:
            best_move.insert(0, -1)

        if len(moves) == 1:
            log_msg += "because there is no other options for "
            if best_move[0]==0:
                log_msg += "covering."
            else: 
                log_msg += "uncovering."
        else:
            if best_move[0]==0:
                log_msg += "because covering "
            else: 
                log_msg += "because uncovering "
            log_msg += "the largest possible values maximizes winning score. "

        self.latest_log += log_msg
        return best_move

    # Function Name: cover_or_uncover
    # Purpose: To figure out whether to cover your own square of uncover an
    # opponent's squares in order to win and maximize points.
    # Parameters:
    #             
    # Return Value: A boolean value which is true if the player decides to cover
    # and is false if the player decides to uncover.
    # Algorithm:
    #             1) If player has less covered squares than opponent's uncovered square,
    #               go for uncover
    #             2) If player has less uncovered squares than opponent's covered square,
    #               go for cover, unless there is less than or equal to 3 opponents uncovered squares
    #               left and more than 3 own uncovered squares, then go for uncover. Because you
    #               have to minimize the opponent's chances of winning.
    # Assistance Received: none   
    def cover_or_uncover(self):
        log_msg = " "
        if len(self.opponent.uncovered_squares()) <= 3 and len(self.uncovered_squares()) > 3:
		    # uncover
            self.latest_log += "In order to minimize opponent's chances, "
            return False

        if len(self.covered_squares()) < len(self.opponent.uncovered_squares()):
            # uncover 
            self.latest_log += "In order to maximize uncovered squares, "
            return False
        elif len(self.uncovered_squares()) < len(self.opponent.covered_squares()):
            # cover
            self.latest_log += "In order to maximize covered squares, "
            return True
        else:
            # if both equal then compare your uncovered squares with opponents uncovered squares 
            # and see for number with max value
            max_num = 1
            for tile in self.uncovered_squares():
                if tile > max_num:
                    max_num = tile
            for tile in self.opponent.covered_squares():
                if tile > max_num:
                    # uncover
                    self.latest_log += "In order to maximize uncovered squares and maximize score, "
                    return False
            self.latest_log += "In order to maximize covered squares and minimize opponents score, "
            # cover
            return True

    # Function Name: roll_one
    # Purpose: To decide whether it is good to roll one die or two dice 
    # Parameters:
    #             
    # Return Value: A boolean value that is true if the player decides to roll one
    # dice and false if the player decides to roll two.
    # Algorithm:
    #             1) Iterate through a list of the opponent's covered squares.
    #             2) roll one if opponent's covered squares are all less than 6, else
    #               roll two.
    # Assistance Received: none 
    def roll_one(self):
        # a boolean variable that indicated whether the player will roll one (true)
        # or roll two (false)
        rollOne = True
        log_msg = ""
        log_msg += self.name + " decided to "
        for tile in self.opponent.covered_squares():
            if tile > 6:
                rollOne = False
                break
        if rollOne:
            log_msg += "roll one die because opponent has all squares greater than 6 uncovered."
        else:
            log_msg += "roll two dice because opponent's covered squares can be uncovered as well."
        self.latest_log += log_msg
        return rollOne