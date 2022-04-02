from kivy.uix.screenmanager import Screen
from views.GameScreen import GameScreen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from models.Player import Player
from models.Human import Human
from models.Computer import Computer
from models.Game import Game
import os

class LoadFileScreen(Screen):
    # Function Name: load_files
    # Purpose: To display a list of all saved games using the ToggleButton widget 
    # Parameters:
    #             
    # Return Value: none (void)
    # Algorithm:
    #             1) Assign the path of the directory in which the games are saved to 
    #               self.saved_files
    #             2) Check if there are any files in the folder.
    #                If no, add a Label widget with text "No files to load"
    #                If yes, add a ToggleButton widget with the file name as text.
    # Assistance Received: none 
    def load_files(self):
        self.saved_files = os.listdir("canoga_venv/saved_games")
        if not self.saved_files:
            self.ids.saved_games_box.add_widget(Label(text="No files to load."))
        else:
            for file_name in self.saved_files:
                self.ids.saved_games_box.add_widget(ToggleButton(text=file_name, group="file_choices", size_hint_y=0.1))

    # Function Name: load_game
    # Purpose: To read a saved file and parse the information to initialize a game 
    # Parameters:
    #             
    # Return Value: none (void)
    # Algorithm:
    #             1) Check which ToggleButton has been pressed.
    #             2) If a button has been found to be in "down" state, then open the file
    #                with the name of the text of that button.
    #             3) Read the file line by line and parse the lines to get the information
    #                required to initialize an instance of Game class.
    #             4) Once all the information is collected, a Game class is initialized and
    #                passed into the setup_game function of GameScreen class to pass the 
    #                game state.
    # Assistance Received: none 
    def load_game(self):
        found = False
        filename = ""
        for file_toggle in self.ids.saved_games_box.children:
            if file_toggle != self.ids.saved_games_scroller and file_toggle.state == 'down':
                filename = file_toggle.text
                found = True
                break
        
        if found:
            with open(os.path.join("canoga_venv/saved_games", filename), 'r') as file:
                lines = file.readlines()
                player1_name, player2_name, first_turn, next_turn = "","","",""
                player1_score, player2_score = 0,0

                player1_name = lines[0][:lines[0].find(":")]
                player2_name = lines[4][:lines[4].find(":")]

                player1_score = int(lines[2][lines[2].find(":") + 2:])
                player2_score = int(lines[6][lines[6].find(":") + 2:])

                first_turn = lines[8][lines[8].find(":") + 2:-1]
                next_turn = lines[9][lines[9].find(":") + 2:-1]

                if (first_turn != player1_name and first_turn != player2_name) or (next_turn != player1_name and next_turn != player2_name):
                    print("Something went wrong. File could not be loaded")
                    return False

                player1_board, player2_board = "", ""
                player1_board = lines[1][lines[1].find(":") + 2:]
                player2_board = lines[5][lines[5].find(":") + 2:]

                # players whose internal members will be set using the information from the saved file
                p1, p2 = Player(), Player()

                # single_mode True = single player, False = multi player
                single_mode = True

                if player1_name != "Computer":
                    p1 = Human(player1_name)
                    if player2_name == "Computer":
                        p2 = Computer("Computer")
                    else:
                        p2 = Human(player2_name)
                        single_mode = False
                else:
                    p2 = Human(player2_name)
                    p1 = Computer("Computer")

                p1.score = player1_score
                p2.score = player2_score

                player1_board_state = [False] * 12
                player2_board_state = [False] * 12

                # int variable to count the number of squares
                index = 0
                charIndex = 0
                for charIndex in range(len(player1_board)-1):
                    square_state = player1_board[charIndex]
                    if square_state == '*':
                        player1_board_state[index] = True
                        index += 1
                    elif square_state.isdigit():
                        if charIndex < (len(player1_board)-1) and player1_board[charIndex + 1].isdigit():
                            charIndex+=1
                        index+=1

                index -= 1
                if index>=10:
                    if square_state == '*':
                        player1_board_state[index-1] = True
                    player1_board_state = player1_board_state[:index]
                    squares = index
                else:
                    if square_state == '*':
                        player1_board_state[index] = True
                    player1_board_state = player1_board_state[:index+1]
                    squares = index + 1

                # resetting index
                index = 0
                charIndex = 0
                for charIndex in range(len(player2_board)-1):
                    square_state = player2_board[charIndex]
                    if square_state == '*':
                        player2_board_state[index] = True
                        index += 1
                    elif square_state.isdigit():
                        if charIndex < (len(player2_board)-1) and player2_board[charIndex + 1].isdigit():
                            charIndex+=1
                        index+=1

                index -= 1
                if index>=10:
                    if square_state == '*':
                        player2_board_state[index-1] = True
                    player2_board_state = player2_board_state[:index]
                else:
                    if square_state == '*':
                        player2_board_state[index] = True
                    player2_board_state = player2_board_state[:index+1] 
                
                # checking if there was any advantage square that cannot be uncovered ( if its the first round )
                first_turn_indicator = lines[8][lines[8].find("First") + 6]
                if first_turn_indicator != 'T':
                    if player1_name == next_turn and len(p2.covered_squares()) == 1:
                        p2.advantage_square = p2.covered_squares()[0]
                    elif player2_name == next_turn and len(p1.covered_squares()) == 1:
                        p1.advantage_square = p2.covered_squares()[0]
                # booleans to check if the first player's name was assigned to first turn correctly
                b_p1, b_p2 = True, True
                if first_turn == p1.name:
                    b_p1 = p1.first_turn = True
                else:
                    b_p2 = p2.first_turn = True
                if not b_p1 or not b_p2:
                    print("Error while setting first turn identifier.")
                    return
                
                dice_rolls = []
                dice_rolls_location = len(lines)
                for line in lines:
                    if line.find("Dice:") == 0:
                        dice_rolls_location = lines.index(line) + 1
                        break

                for i in range(dice_rolls_location, len(lines)):
                    if len(lines[i]) > 0:
                        dice_roll = []
                        for char in lines[i]:
                            if char.isdigit():
                                dice_roll.append(int(char))
                        if dice_roll:
                            dice_rolls.append(dice_roll)
                        
                game = Game(single_mode, squares, p1, p2, next_turn, dice_rolls)
                game_screen = GameScreen()
                game_screen.setup_game(game, player1_board_state, player2_board_state)
                game.currentPlayer.board_state.reverse()
                game.nextPlayer.board_state.reverse()
                if first_turn_indicator != 'T':
                    game_screen.game.first_turn = True
                else:
                    game_screen.game.first_turn = False

                print("Switching to game screen")
                print(self.manager.screen_names)
                # creating new game_screen every time, creates additional _screen0 screens
                self.manager.switch_to(game_screen)
                print(self.manager.screen_names)
                    
        
