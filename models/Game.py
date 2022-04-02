from models.Log import Log

class Game:
    # Function Name: __init__
    # Purpose: To initialize a Game class
    # Parameters:
    #             
    # Return Value: none (void)
    # Algorithm:
    #             1) Initialize all members passed into the function
    # Assistance Received: none 
    def __init__(self, single_player, squares, player1, player2, next_turn="", dice_rolls=[]):
        self.single_player = single_player
        self.squares = squares
        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = player1
        self.nextPlayer = player2
        self.round_num = 1
        self.round_winner = ""
        self.round_winning_score = 0
        self.log = Log()
        self.next_turn = next_turn
        self.dice_rolls = dice_rolls