from models.Player import Player

class Human(Player):
    # Function Name: __init__
    # Purpose: To initialize a Human class 
    # Parameters:
    #             
    # Return Value: none (void)
    # Algorithm:
    #             1) Set the name passed as member variable
    # Assistance Received: none 
    def __init__(self, name):
        self.name = name