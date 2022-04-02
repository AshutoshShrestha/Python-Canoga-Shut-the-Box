class Player:

    # Function Name: covered_squares
    # Purpose: To return a Player's covered squares 
    # Parameters:
    #             
    # Return Value: covered_tiles, a list of player's covered squares
    # Algorithm:
    #             1) Iterate through a player's board
    #             2) If True is stored in a position, then append it to the list
    #                to be returned.
    # Assistance Received: none 
    def covered_squares(self):
        covered_tiles = []
        for i in range(len(self.board_state)):
            if self.board_state[i]:
                covered_tiles.append(len(self.board_state)-i)
        return covered_tiles
    
    # Function Name: uncovered_squares
    # Purpose: To return a Player's uncovered squares 
    # Parameters:
    #             
    # Return Value: uncovered_tiles, a list of player's covered squares
    # Algorithm:
    #             1) Iterate through a player's board
    #             2) If False is stored in a position, then append it to the list
    #                to be returned.
    # Assistance Received: none 
    def uncovered_squares(self):
        uncovered_tiles = []
        for i in range(len(self.board_state)):
            if not self.board_state[i]:
                uncovered_tiles.append(len(self.board_state)-i)
        return uncovered_tiles

    # Function Name: __init__
    # Purpose: To initialize a Player class 
    # Parameters:
    #             
    # Return Value: none (void)
    # Algorithm:
    #             1) Initialize all the required default values.
    # Assistance Received: none 
    def __init__(self):
        self.score = 0
        self.previous_round_score = 0
        self.first_turn = False
        self.advantage_square = -1
        self.board_state = []
