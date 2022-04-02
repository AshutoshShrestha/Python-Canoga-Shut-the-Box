from kivy.uix.screenmanager import Screen
from models.Game import Game
from models.Human import Human
from models.Computer import Computer
from views.GameScreen import GameScreen

class GameModeScreen(Screen):
    # Function Name: start_game
    # Purpose: To initialize a new game and take the user to the game screen. 
    # Parameters:
    #          parent, a variable that holds information on the parent of 
    #          the button that triggered the function. It hasn't been used but
    #          python syntax requires to include it as a parameter.
    # Return Value: none (void)
    # Algorithm:
    #             1) Check which ToggleButton has been clicked down for the game
    #                squares information.
    #             2) Initialize new Player variables, whether it be Human or Computer
    #                according to the game_mode selected by the user.
    #             3) Instantiate a new Game class nad pass it into the setup_game
    #                method inside the GameScreen class to pass the game state.
    #             4) Switch to GameScreen.
    # Assistance Received: none 
    def start_game(self, parent):
        valid_input = True
        if self.ids.nine.state == 'down':
            self.squares = 9
        elif self.ids.ten.state == 'down':
            self.squares = 10
        elif self.ids.eleven.state == 'down':
            self.squares = 11
        elif self.ids.twelve.state == 'down':
            self.squares = 12
        else:
            print("Select one squares value")
            valid_input = False
        
        if self.ids.single.state == 'down':
            self.single_mode = True
            if len(self.ids.player1_name.text) != 0: 
                self.player1_name = self.ids.player1_name.text
                self.player2_name = "Computer"
            else:
                print("Enter player name")
                valid_input = False
        elif self.ids.multi.state == 'down':
            self.single_mode = False
            if len(self.ids.player1_name.text) != 0 and len(self.ids.player2_name.text): 
                self.player1_name = self.ids.player1_name.text
                self.player2_name = self.ids.player2_name.text
            else:
                print("Enter player names")
                valid_input = False
        else:
            print("Select one mode value")
            valid_input = False
        
        if valid_input:
            game_screen = GameScreen()
            if self.single_mode:
                player1 = Human(self.player1_name)
                player2 = Computer(self.player2_name)
            else:
                player1 = Human(self.player1_name)
                player2 = Human(self.player2_name)
            # game_screen.ids.roll_two_btn.text = "First turn decider" 
            game_screen.setup_game(Game(self.single_mode, self.squares, player1, player2))
            
            print("Switching to game screen")
            print(self.manager.screen_names)
            # creating new game_screen every time, creates additional _screen0 screens
            self.manager.switch_to(game_screen)
            print(self.manager.screen_names)

    def build(self):
        pass