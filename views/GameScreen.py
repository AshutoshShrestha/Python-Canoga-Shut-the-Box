from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import random
import os

class GameScreen(Screen):
    # Function Name: __init__
    # Purpose: To initialize a GameScreen class 
    # Parameters:
    #             
    # Return Value: 
    # Algorithm:
    #             1) Initialize all required default values
    # Assistance Received: none
    def __init__(self):
        self.sq = 9
        self.single_player = True
        self.all_dice_values = [1, 2, 3, 4, 5, 6]

    # Function Name: change_dice_pics
    # Purpose: To change the dice pics according to the dice rolls 
    # Parameters:
    #             dice1_val, an int that holds the value of the first dice roll
    #             dice2_val, an int that holds the value of the second dice roll
    # Return Value: none (void)
    # Algorithm:
    #             1) Check the dice1 and dice2 values and get the respective image
    #                with the help of the switcher.
    #             2) Set the image source.
    # Assistance Received: none 
    def change_dice_pics(self, dice1_val, dice2_val):
        switcher = {
            1: "res/one.jpg",
            2: "res/two.jpg",
            3: "res/three.jpg",
            4: "res/four.jpg",
            5: "res/five.jpg",
            6: "res/six.jpg",
        }
        self.ids.dice_one_image.source = switcher.get(dice1_val, "nothing")
        if dice2_val <= 0 or dice2_val > 6:
            self.ids.dice_two_image.source = "res/zero.jpg"
        else:
            self.ids.dice_two_image.source = switcher.get(dice2_val, "nothing")

    # Function Name: roll_dice
    # Purpose: To simulate rolling a dice 
    # Parameters:
    #             roll_one, a boolean that holds true if rolling one option is available
    # Return Value: True if first player is decided (first player wasn't decided before)
    #               False if first player is not decided (first player wasn't decided before)
    #               total value of the rolled dice (if first player was already decided before)
    # Algorithm:
    #             1) Check if the first player has been decided by checking the roll_two_btn text
    #             2) If not, then roll the dice for both the players until one gets a higher value,
    #                and set that player as the currentPlayer and the other player as the nextPlayer
    #             3) If yes, then roll the dice for the currentPlayer only.
    # Assistance Received: none 
    def roll_dice(self, roll_one):
        if self.ids.roll_two_btn.text != "Roll":
            # decide first player
            player1_total, player2_total = 0,0

            if self.game.dice_rolls:
                self.game.log.add_log(self.game.currentPlayer.name + " was made to roll dices loaded from a file.")
                self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " was made to roll dices loaded from a file."
                dice_roll = self.game.dice_rolls[0]
                self.game.dice_rolls.pop(0)
                if len(dice_roll) == 2:
                    player1_total = dice_roll[0] + dice_roll[1]               
                else:
                    player1_total = dice_roll[0]
                
                self.game.log.add_log(self.game.currentPlayer.name + " used loaded dices: " + str(dice_roll))
                self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " used loaded dices: " + str(dice_roll)

                if self.game.dice_rolls:
                    self.game.log.add_log(self.game.nextPlayer.name + " was made to roll dices loaded from a file.")
                    self.ids.log_text.text += "\n" + self.game.nextPlayer.name + " was made to roll dices loaded from a file."
                    dice_roll = self.game.dice_rolls[0]
                    self.game.dice_rolls.pop(0)
                    if len(dice_roll) == 2:
                        player2_total = dice_roll[0] + dice_roll[1]         
                    else:
                        player2_total = dice_roll[0]
                    
                    self.game.log.add_log(self.game.nextPlayer.name + " used loaded dices: " + str(dice_roll))
                    self.ids.log_text.text += "\n" + self.game.nextPlayer.name + " used loaded dices: " + str(dice_roll)
                else:
                    val1 = random.choice(self.all_dice_values)
                    val2 = random.choice(self.all_dice_values)
                    player2_total = val1 + val2

                    self.game.log.add_log(self.game.nextPlayer.name + " rolled " + str(val1) + " and " + str(val2))
                    self.ids.log_text.text += "\n" + self.game.nextPlayer.name + " rolled " + str(val1) + " and " + str(val2)
            else:
                val1 = random.choice(self.all_dice_values)
                val2 = random.choice(self.all_dice_values)
                player1_total = val1 + val2

                self.game.log.add_log(self.game.currentPlayer.name + " rolled " + str(val1) + " and " + str(val2))
                self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " rolled " + str(val1) + " and " + str(val2)

                val1 = random.choice(self.all_dice_values)
                val2 = random.choice(self.all_dice_values)
                player2_total = val1 + val2

                self.game.log.add_log(self.game.nextPlayer.name + " rolled " + str(val1) + " and " + str(val2))
                self.ids.log_text.text += "\n" + self.game.nextPlayer.name + " rolled " + str(val1) + " and " + str(val2)
            
            if player1_total == player2_total:
                return False

            if player1_total < player2_total or player1_total > player2_total:
                if player1_total < player2_total:
                    self.switch_player_turns()
                self.game.first_turn = True
                self.ids.roll_two_btn.text = "Roll"
                self.ids.turn_identifier.text = "Current turn: " + self.game.currentPlayer.name
                self.ids.first_turn_identifier.text = "First turn: " + self.game.currentPlayer.name

                log_msg = self.game.currentPlayer.name + " goes first"
                self.game.log.add_log(log_msg)
                self.ids.log_text.text += "\n" + log_msg

                self.game.currentPlayer.first_turn = True
                self.game.nextPlayer.first_turn = False
                if self.game.currentPlayer.name == "Computer":
                    self.ids.roll_two_btn.disabled = True
                    self.ids.help_btn.disabled = False
                    self.ids.help_btn.text = "Click for Computer move"
                else:
                    self.ids.roll_two_btn.disabled = False
                self.ids.roll_one_btn.disabled = True
                return True

        else:
            self.ids.roll_two_btn.disabled = True
            self.ids.roll_one_btn.disabled = True
            self.ids.to_cover.disabled = False
            self.ids.to_uncover.disabled = False
            
            totalVal = 0
            val1, val2 = 0,0
            if self.game.dice_rolls:
                self.game.log.add_log(self.game.currentPlayer.name + " was made to roll dices loaded from a file.")
                self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " was made to roll dices loaded from a file."
                dice_roll = self.game.dice_rolls[0]
                self.game.dice_rolls.pop(0)
                if len(dice_roll) == 2:
                    val1 = dice_roll[0]
                    val2 = dice_roll[1] 
                    self.game.log.add_log(self.game.currentPlayer.name + " used loaded dices: " + str(val1) + " and " + str(val2))
                    self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " used loaded dices: " + str(val1) + " and " + str(val2)        
                else:
                    val1 = dice_roll[0]
                    val2 = 0
                    self.game.log.add_log(self.game.currentPlayer.name + " used loaded dices: " + str(val1))
                    self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " used loaded dices: " + str(val1)
            else:
                val1 = random.choice(self.all_dice_values)
                if roll_one:
                    val2 = 0
                    self.game.log.add_log(self.game.currentPlayer.name + " rolled " + str(val1))
                    self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " rolled " + str(val1)
                else:
                    val2 = random.choice(self.all_dice_values)
                    self.game.log.add_log(self.game.currentPlayer.name + " rolled " + str(val1) + " and " + str(val2))
                    self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " rolled " + str(val1) + " and " + str(val2)

            self.change_dice_pics(val1,val2)

            totalVal = val1+val2
            if self.game.currentPlayer.name != "Computer":
                self.display_options(totalVal)

            self.totalVal = totalVal

            return totalVal
    
    # Function Name: setup_game
    # Purpose: To initialize all the necessary variables for the game and set the 
    #          widgets according to the initialize game state. 
    # Parameters:
    #             game, a Game class variable that holds the in-game information
    #             player1_board_state and player2_board_state, boolean arrays that
    #               hold the player's board states.
    # Return Value:
    # Algorithm:
    #             1) Set the first_turn to be true 
    #             2) Check if player1_board_state and player2_board_state has been passed
    #             to the function. If yes, set the player boards as the parameters, if no, 
    #             initialize new board_state arrays for each player.
    #             3) Set the widgets according to player board state.
    #             4) Decide the first player of the round
    #             5) Change the Label widgets for the first player and current player, and 
    #             change the dice pictures as well
    # Assistance Received: none 
    def setup_game(self, game, player1_board_state = [], player2_board_state = []):
        self.game = game
        # indicates that this is the first turn in the round
        self.game.first_turn = True

        if not player1_board_state or not player2_board_state:
            self.game.player1.board_state = [False] * self.game.squares
            self.game.player2.board_state = [False] * self.game.squares
        else:
            self.game.player1.board_state = player1_board_state
            self.game.player2.board_state = player2_board_state

        if self.ids.player1_board.children or self.ids.player2_board.children:
            self.ids.player1_board.clear_widgets()
            self.ids.player2_board.clear_widgets()

        for i in range(self.game.squares):
            print(i)
            print(len(self.game.player1.board_state))
            tile1 = Button(
                text=str(i+1), 
                size_hint=(1/game.squares, 0.75), 
                disabled=True, 
                background_disabled_normal='', 
                background_color=(1,0,0,1) if not self.game.player1.board_state[i] else (0,1,0,1))
            tile2 = Button(
                text=str(i+1), 
                size_hint=(1/game.squares, 0.75), 
                disabled=True, 
                background_disabled_normal='', 
                background_color=(1,0,0,1) if not self.game.player2.board_state[i] else (0,1,0,1))            
            self.ids.player1_board.add_widget(tile1)
            self.ids.player2_board.add_widget(tile2) 
        
        self.ids.player1_board_label.text = self.game.player1.name + "'s board"
        self.ids.player2_board_label.text = self.game.player2.name + "'s board"

        self.ids.player1_score_label.text = self.game.player1.name + ": " + str(self.game.player1.score)
        self.ids.player2_score_label.text = self.game.player2.name + ": " + str(self.game.player2.score)
        if self.game.round_winning_score != 0 and self.game.round_winner != "":
            if not self.game.player1.first_turn and self.game.player2.first_turn:
                self.give_advantage(self.game.player1)
            elif not self.game.player2.first_turn and self.game.player1.first_turn:
                self.give_advantage(self.game.player2)
                    
        if self.game.next_turn!="":
            if self.game.next_turn == self.game.player1.name:
                self.game.currentPlayer = self.game.player1
                self.game.nextPlayer = self.game.player2
            else:
                self.game.currentPlayer = self.game.player2
                self.game.nextPlayer = self.game.player1
            first_player = self.game.next_turn
            self.game.next_turn = ""
            if self.game.currentPlayer.name == "Computer":
                self.ids.roll_two_btn.disabled = True
                self.ids.roll_one_btn.disabled = True
                self.ids.to_cover.disabled = True
                self.ids.to_uncover.disabled = True
            else:
                self.ids.roll_two_btn.disabled = False
            

            self.ids.turn_identifier.text = "Current turn: " + first_player

            if self.game.currentPlayer.first_turn:
                self.ids.first_turn_identifier.text = "First turn: " + self.game.currentPlayer.name
            else:
                self.ids.first_turn_identifier.text = "First turn: " + self.game.nextPlayer.name

            self.ids.dice_one_image.source = "res/zero.jpg"
            self.ids.dice_two_image.source = "res/zero.jpg"

            if self.game.currentPlayer.name != "Computer" and self.game.nextPlayer.name != "Computer":
                self.ids.help_btn.disabled = True
            elif self.game.currentPlayer.name == "Computer":
                self.ids.help_btn.disabled = False
                self.ids.help_btn.text = "Click for Computer move"
            
            self.ids.log_text.text += "\n" + "Round Started"
            self.ids.roll_one_btn.disabled = True
        else:
            self.ids.roll_two_btn.text = "First Turn Decider"
            self.ids.roll_two_btn.disabled = False
        self.ids.cover_options.clear_widgets()
        self.ids.uncover_options.clear_widgets()

    # Function Name: display_options
    # Purpose: To display the options to cover or uncover to the user.
    # Parameters:
    #             totalVal, the total dice value rolled by a player.
    # Return Value:
    # Algorithm:
    #             1) Call all_available_cover_moves and all_available_uncover_moves
    #                funtions to find out the user's available moves.
    #             2) Display the respective cover and uncover moves as ToggleButtons
    #                inside the cover_options and uncover_options widget.
    #             3) If there are no cover and uncover options then switch the turns.
    # Assistance Received: none 
    def display_options(self, totalVal):
        cover_options = self.all_available_cover_moves(self.findCombinations(totalVal), self.game.currentPlayer)
        uncover_options = self.all_available_uncover_moves(self.findCombinations(totalVal), self.game.nextPlayer)

        if cover_options or uncover_options:
            self.ids.select_option_btn.disabled = False
            self.ids.cover_options.clear_widgets()
            self.ids.uncover_options.clear_widgets()
            for cover_option in cover_options:
                option_btn = ToggleButton(text = str(cover_option), color=(0,0,0,1), size_hint_y=None, group="user_choice")
                option_btn.height = option_btn.height * 0.4
                self.ids.cover_options.add_widget(option_btn)
            for uncover_option in uncover_options:
                option_btn = ToggleButton(text = str(uncover_option), color=(0,0,0,1), size_hint_y=None, group="user_choice")
                option_btn.height = option_btn.height * 0.4
                self.ids.uncover_options.add_widget(option_btn)
        
        if not cover_options:
            self.ids.to_cover.disabled = True
        if not uncover_options:
            self.ids.to_uncover.disabled = True

        if not cover_options and not uncover_options:
            self.ids.to_cover.disabled = True
            self.ids.to_uncover.disabled = True
            self.ids.select_option_btn.text = self.game.nextPlayer.name + "'s turn"
            self.ids.select_option_btn.disabled = False
            
            self.ids.roll_one_btn.disabled = True
            self.ids.roll_two_btn.disabled = True

    # Function Name: check_unique
    # Purpose: To check if all the numbers in a combination are unique. 
    # Parameters:
    #             arr - one_combination, a list of integers that holds
    #               a combination of moves (ints)
    #             index - index at which to check upto.
    # Return Value:
    # Algorithm:
    #             1) Iterate through the list of the combination, and check if
    #               there are any two numbers that are equal to each other.
    # Assistance Received: none 
    def check_unique(self, arr, index):
        for i in range(index-1):
            for j in range(i+1, index):
                if arr[i] == arr[j]:
                    return False
        
        return True

    # Function Name: findCombinationsUtil
    # Purpose: To find all possible combinations 
    # Parameters:
    #             all_possible_combinations, a list of lists.
    #               It holds all the possible combinations of moves a user
    #               can make from a given dice roll values
    #             arr, an integer array. It holds one possible combination
    #               from all possible combinations of moves a user can make.
    #             index, an integer variable. It holds the index of array
    #               which holds one possible combination out of all combinations
    #             num, an integer variable. It holds the value from which
    #               all moves need to be calculated from. This value is the sum
    #               of both dice rolled values of a player.
    #             reducedNum, an integer variable. It holds the number of levels
    #               in the recursive tree when the function findCombinationsUtil 
    #               is called recursively.
    # Return Value:
    # Algorithm:
    #             1) If reducedNum is less than 0, then return from the function.
    #             2) If reducedNum is equal to 0, then form a list and copy
    #               the elements from arr into the list one_possible_combination.
    #               Check if the combination has all unique elements. If yes, append to
    #               the list into the all_possible_combinations list.
    #             3) If reducedNum is greater than 0, then find the previous
    #               number stored in arr, if none then use 1.
    #             4) Loop from the previous number upto passed num value.
    #             5) Set the value at index position of array to k.
    #             6) Recursively call findCombinationsUtil function with
    #               reducedNum.
    # Assistance Received: Geeks4Geeks
    def findCombinationsUtil(self, all_possible_moves, arr, index, num, reducedNum):  
        # Base condition
        if (reducedNum < 0):
            return
    
        if (reducedNum == 0):
            if self.check_unique(arr, index):
                one_possible_move = []
                for i in range(index):
                    one_possible_move.append(arr[i])
        
                all_possible_moves.append(one_possible_move)
            return
    
        # Find the previous number stored in arr[].
        # It helps in maintaining increasing order
        prev = 1 if(index == 0) else arr[index - 1]
    
        # note loop starts from previous
        # number i.e. at array location
        # index - 1
        for k in range(prev, num + 1):
            
            # next element of array is k
            arr[index] = k
    
            # call recursively with
            # reduced number
            self.findCombinationsUtil(all_possible_moves, arr, index + 1, num, reducedNum - k)

    # Function Name: findCombinations
    # Purpose: To recursively call the findCombinationsUtil function 
    # Parameters:
    #             val, it holds the value from which all moves need to 
    #               be calculated from. This value is the sum of both 
    #               dice rolled values of a player.
    # Return Value:
    # Algorithm:
    #             1) call findCombinationsUtil function to initiate the recursive sequence.
    # Assistance Received: none 
    def findCombinations(self, val):
        # array to store the combinations
        # It can contain max n elements
        arr = [0] * val
        all_possible_moves = []
        # find all combinations
        self.findCombinationsUtil(all_possible_moves, arr, 0, val, val)
        
        return all_possible_moves
    
    # Function Name: all_available_cover_moves
    # Purpose: To find all available cover moves by comparing a given list of all
    # possible moves with the player's uncovered squares.
    # Parameters:
    #             all_moves, a list of list of integers. It holds all possible moves
    #               from a rolled dice value.
    # Return Value:
    # Algorithm:
    #             1) Iterate through the list of all_moves.
    #             2) Iterate thorugh each move inside the list.
    #             3) Iterate through the currentPlayer's uncovered_sq list.
    #             4) Check if you find all the numbers from each list of all_moves
    #                in the currentPlayer's uncovered_sq list.
    #             5) If there is a list that has all integers in the currentPlayer's 
    #                uncovered_sq list, then append to all_available_cover_moves list
    #             6) Return all_available_cover_moves list.
    # Assistance Received: none   
    def all_available_cover_moves(self, all_moves):
        all_available_moves = []
        for move in all_moves:
            found = False
            for tile in move:
                found = False
                if tile > self.game.squares:
                    found = True
                    break
                for covered_tile in self.game.currentPlayer.covered_squares():
                    if tile == covered_tile:
                        found = True
                        break
                if found:
                    break
            if not found:
                all_available_moves.append(move)
        return all_available_moves

    # Function Name: all_available_uncover_moves
    # Purpose: To find all available uncover moves by comparing a given list of all
    # possible moves with the next player's covered squares.
    # Parameters:
    #             all_moves, a list of list of integers. It holds all possible moves
    #               from a rolled dice value.
    # Return Value:
    # Algorithm:
    #             1) Iterate through the list of all_moves.
    #             2) Iterate thorugh each move inside the list.
    #             3) Iterate through the nextPlayer's covered_sq list.
    #             4) Check if you find all the numbers from each list of all_moves
    #                in the nextPlayer's covered_sq list.
    #             5) If there is a list that has all integers in the nextPlayer's 
    #                covered_sq list, then append to all_available_cover_moves list.
    #             6) Return all_available_cover_moves list.
    def all_available_uncover_moves(self, all_moves):
        all_available_moves = []
        for move in all_moves:
            found = False
            for tile in move:
                found = False
                if tile > self.game.squares:
                    found = True
                    break
                for player_tile in self.game.nextPlayer.uncovered_squares():
                    if tile == player_tile:
                        found = True
                        break
                if found:
                    break
            if not found:
                all_available_moves.append(move)
        if len(all_available_moves) == 1 and all_available_moves[0][0] == self.game.nextPlayer.advantage_square:
            return []
        
        return all_available_moves

    # Function Name: switch_player_turns
    # Purpose: To switch the player's turns.
    # Parameters:
    # Return Value:
    # Algorithm:
    #             1) Set the currentPlayer as the nextPlayer.
    #             2) Set the nextPlayer as the currentPlayer.
    #             3) Change the respective relevant widgets.
    # Assistance Received: none 
    def switch_player_turns(self):
        temp = self.game.nextPlayer
        self.game.nextPlayer = self.game.currentPlayer
        self.game.currentPlayer = temp
        self.game.first_turn = False
        if self.game.currentPlayer.name == "Computer":
            self.ids.help_btn.text = "Click for Computer move"
            self.ids.roll_one_btn.disabled = True
            self.ids.roll_two_btn.disabled = True
            self.ids.user_options.disabled = True
        else:
            self.ids.help_btn.text = "Help"
            self.ids.roll_one_btn.disabled = False
            self.ids.user_options.disabled = False
            self.ids.cover_options.clear_widgets()
            self.ids.uncover_options.clear_widgets()
            self.ids.to_cover.disabled = True
            self.ids.to_uncover.disabled = True

        # update log
        filepath = os.path.join('canoga_venv/log', "latest_log")
        if not os.path.exists('canoga_venv/log'):
            os.makedirs('canoga_venv/log')
        f = open(filepath + ".txt", "w")

        for log in self.game.log.get_all_log():
            f.write(log + "\n")
        f.write("Log updated" + "\n")

    # Function Name: refresh_tiles
    # Purpose: To reset the player tiles display according to their real state.
    # Parameters:
    # Return Value:
    # Algorithm:
    #             1) Change the widgets of the player boards according to their board_state.
    # Assistance Received: none 
    def refresh_tiles(self):
        index = 0
        for tile in self.ids.player1_board.children:
            if self.game.player1 == self.game.currentPlayer:
                tile.background_color = (0,1,0,1) if self.game.currentPlayer.board_state[index] else (1,0,0,1)
            else:
                tile.background_color = (0,1,0,1) if self.game.nextPlayer.board_state[index] else (1,0,0,1)
            index+=1
        index = 0
        for tile in self.ids.player2_board.children:
            if self.game.player2 == self.game.currentPlayer:
                tile.background_color = (0,1,0,1) if self.game.currentPlayer.board_state[index] else (1,0,0,1)
            else:
                tile.background_color = (0,1,0,1) if self.game.nextPlayer.board_state[index] else (1,0,0,1)
            index+=1

    # Function Name: string_to_list
    # Purpose: To convert the string form of user selected move to a list. 
    # Parameters:
    #             option_btn_text, a string variable that holds the user's selected option.
    # Return Value:
    # Algorithm:
    #             1) Remove the parenthesis from the string.
    #             2) Check if each element is a digit. 
    #             3) Check if the next element is a digit as well. If yes, then concatenate 
    #                both characters and convert it to int and append it to list. If next 
    #                element is not a digit then append the char to the list as an int.
    # Assistance Received: none 
    def string_to_list(self, option_btn_txt):
        option_btn_txt = option_btn_txt.replace("(", "").replace(")", "")
        option = []
        prev = -1
        for char in option_btn_txt:
            if prev!=-1:
                if char.isdigit():
                    prev+=char
                else:
                    option.append(int(prev))
                    prev=-1
                continue
            if char.isdigit():
                prev = char
        if prev!=-1:
            option.append(int(prev))
        return option

    # Function Name: round_won
    # Purpose: To check if a player has won the round. 
    # Parameters:
    # Return Value:
    # Algorithm:
    #             1) Check if a player's squares are all covered.
    #             2) Or if it is not the first turn of the game, check if
    #             the other's player's squares are all uncovered.
    #             3) If a player has all squares covered, or the opponent's 
    #             are all uncovered unless it's the first turn, the player has won.
    # Assistance Received: none 
    def round_won(self):
        round_over = False
        self.game.round_winning_score = 0
        if len(self.game.currentPlayer.uncovered_squares()) == 0:
            round_over = True
            for tile in self.game.nextPlayer.uncovered_squares():
                self.game.round_winning_score += tile
            self.game.currentPlayer.score += self.game.round_winning_score
        # because python supports short circuiting
        elif (not self.game.first_turn) and (len(self.game.nextPlayer.covered_squares()) == 0):
            round_over = True
            for tile in self.game.currentPlayer.covered_squares():
                self.game.round_winning_score += tile
            self.game.currentPlayer.score += self.game.round_winning_score
        else:
            round_over = False
        if round_over:
            self.game.round_winner = self.game.currentPlayer.name
            # self.ids.cover_options.disabled = True
            # self.ids.uncover_options.disabled = True
            self.ids.to_cover.disabled = True
            self.ids.to_uncover.disabled = True

        return round_over

    # Function Name: end_round
    # Purpose: To display the end round screen to the user.
    # Parameters:
    # Return Value:
    # Algorithm:
    #             1) Check which player is winning the round and update the game_winner variable
    #             2) Remove the game_box widget.
    #             3) Create a end_round widget with the widgets that show the user the results of the
    #                round and the widgets that allow that user to start a new round.
    #             4) Add the end_round widget to the full_screen widget.
    # Assistance Received: none 
    def end_round(self):
        self.game.game_winner = "Draw"
        self.game.game_winning_score = 0
        if self.game.currentPlayer.score > self.game.nextPlayer.score:
            self.game.game_winner = self.game.currentPlayer.name
            self.game.game_winning_score = self.game.currentPlayer.score
        elif self.game.nextPlayer.score > self.game.currentPlayer.score:
            self.game.game_winner = self.game.nextPlayer.name
            self.game.game_winning_score = self.game.nextPlayer.score

        self.game.log.add_log(self.game.round_winner + " won the round.")

        self.game_box = self.ids.game_box

        self.ids.full_screen.remove_widget(self.ids.game_box)

        end_round_screen = BoxLayout()
        self.ids['end_round_screen'] = end_round_screen 
        end_round_box = BoxLayout( orientation="vertical")
        self.ids["end_round_box"] = end_round_box
        round_over_label = Label(size_hint=(1, 0.1), text="Round Over")
        winner_label = Label(size_hint=(1, 0.1), text="Winner: "+self.game.round_winner)
        self.ids["winner_label"] = winner_label
        winning_score_label = Label(size_hint=(1, 0.1), text="Winning Score: " + str(self.game.round_winning_score))
        self.ids["winning_score_label"] = winning_score_label
        end_round_box.add_widget(round_over_label)
        end_round_box.add_widget(winner_label)
        end_round_box.add_widget(winning_score_label)

        options_box = BoxLayout(size_hint=(0.5,0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        finish_game_btn = Button(text="Finish Game")
        finish_game_btn.bind(on_press=self.end_game)
        self.ids["finish_game_btn"] = finish_game_btn
        options_box.add_widget(finish_game_btn)
        end_round_box.add_widget(options_box)
        squares_box = BoxLayout(
            size_hint_y=0.5, 
            orientation="vertical", 
            pos_hint={'center_x': 0.5, 'center_y': 1},
            size_hint_x = 1
            )

        pick_squares_label=Label(size_hint=(1, 0.1), text="Pick Squares")
        squares_box.add_widget(pick_squares_label)
        square_numbers_box = BoxLayout(size_hint=(1, 0.2), spacing=20, padding=40)
        nine_btn = ToggleButton(text="9", group="squares")
        ten_btn = ToggleButton(text="10", group="squares")
        eleven_btn = ToggleButton(text="11", group="squares")
        twelve_btn = ToggleButton(text="12", group="squares")
        self.ids["nine"] = nine_btn
        self.ids["ten"] = ten_btn
        self.ids["eleven"] = eleven_btn
        self.ids["twelve"] = twelve_btn

        square_numbers_box.add_widget(nine_btn)
        square_numbers_box.add_widget(ten_btn)
        square_numbers_box.add_widget(eleven_btn)
        square_numbers_box.add_widget(twelve_btn)

        start_btn_box = BoxLayout(size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5, 'center_y':0.5}, padding=50)
        start_btn = Button(text="Start New Round")
        start_btn.bind(on_press=self.start_next_round)

        start_btn_box.add_widget(start_btn)
        squares_box.add_widget(square_numbers_box)
        squares_box.add_widget(start_btn_box)

        end_round_box.add_widget(squares_box)
        end_round_screen.add_widget(end_round_box)
        self.ids.full_screen.add_widget(end_round_screen)

    # Function Name: provide_help
    # Purpose: To provide help to the user or make the computer make it's move 
    # Parameters:
    # Return Value:
    # Algorithm:
    #             1) Check if the help button text is Help or not.
    #             2) If yes, then use the Computer class's choose_a_move method to suggest a move.
    #             3) If no, then make the Computer player make it's move.
    #             4) Update the widgets respectively.
    # Assistance Received: none 
    def provide_help(self):
        
        if self.ids.help_btn.text == "Help" and self.game.nextPlayer.name == "Computer":
            self.game.nextPlayer.latest_log = ""
            self.game.nextPlayer.set_opponent(self.game.currentPlayer)
            
            cover_options = self.all_available_cover_moves(self.findCombinations(self.totalVal), self.game.currentPlayer)
            uncover_options = self.all_available_uncover_moves(self.findCombinations(self.totalVal), self.game.nextPlayer)

            self.game.nextPlayer.helper = True
            computer_move = self.game.nextPlayer.choose_a_move(cover_options, uncover_options)
            self.game.nextPlayer.helper = False

            self.game.log.add_log(self.game.nextPlayer.latest_log)
            self.ids.log_text.text += "\n" + self.game.nextPlayer.latest_log      
        elif self.game.currentPlayer.name == "Computer" and self.ids.help_btn.text != "Help":
            self.game.currentPlayer.latest_log = ""
            self.game.currentPlayer.set_opponent(self.game.nextPlayer)
            if self.check_roll_one() and self.game.currentPlayer.roll_one():
                totalVal = self.roll_dice(True)
            else:
                totalVal = self.roll_dice(False)
            
            cover_options = self.all_available_cover_moves(self.findCombinations(totalVal), self.game.currentPlayer)
            uncover_options = self.all_available_uncover_moves(self.findCombinations(totalVal), self.game.nextPlayer)

            self.game.currentPlayer.set_opponent(self.game.nextPlayer)
            
            computer_move = self.game.currentPlayer.choose_a_move(cover_options, uncover_options)

            if len(computer_move) <= 1:
                self.switch_player_turns()
                log_msg = "Turns changed"
                self.game.log.add_log(log_msg)
                self.ids.log_text.text += "\n" + log_msg
                self.ids.dice_one_image.source = "res/zero.jpg"
                self.ids.dice_two_image.source = "res/zero.jpg"
                self.ids.turn_identifier.text = "Current turn: " + self.game.currentPlayer.name
                self.ids.select_option_btn.text = "Select"
                self.ids.select_option_btn.disabled = True
                self.ids.roll_two_btn.disabled = False
                self.ids.roll_one_btn.disabled = not self.check_roll_one()
                return
            # cover
            if computer_move[0] == 0:
                for tile in computer_move:
                    if tile >=1:
                        self.game.currentPlayer.board_state[self.game.squares - tile] = True
            # uncover
            elif computer_move[0] == -1:
                for tile in computer_move:
                    if tile >=1:
                        self.game.nextPlayer.board_state[self.game.squares - tile] = False
            
            self.game.log.add_log(self.game.currentPlayer.latest_log)
            self.ids.log_text.text += "\n" + self.game.currentPlayer.latest_log
            self.refresh_tiles()
            if self.round_won():
                self.game.log.add_log("Computer won the round")
                self.end_round()
                return

    # Function Name: select_option
    # Purpose: To implement a user's selected option and switch turns.
    # Parameters:
    #             to_cover, a string variable which holds down if the to_cover toggle
    #               button is in a clicked state and normal if it is not.
    #             to_uncover, a string variable which holds down if the to_uncover toggle
    #               button is in a clicked state and normal if it is not.
    # Return Value:
    # Algorithm:
    #             1) Check select option button's text. If it is Select then go on covering
    #                  or uncovering the user's selected moves.
    #             2) If not, then switch the player's turns and change the widget contents 
    #                 respectively. 
    # Assistance Received: none 
    def select_option(self, to_cover, to_uncover):
        if self.ids.select_option_btn.text=="Select":
            option = []
            found = False
            if to_cover=='down' and to_uncover=='normal':
                for option_btn in self.ids.cover_options.children:
                    if option_btn.state == 'down':
                        found = True
                        option = self.string_to_list(option_btn.text)
                        break
                if found:
                    for tile in option:
                        self.game.currentPlayer.board_state[self.game.squares-tile] = True
                    self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " covered " + str(option)
                    self.game.log.add_log(self.game.currentPlayer.name + " covered " + str(option))
            elif to_uncover=='down' and to_cover=='normal':
                found = False
                for option_btn in self.ids.uncover_options.children:
                    if option_btn.state == 'down':
                        found = True
                        option = self.string_to_list(option_btn.text)
                        break
                if found:
                    for tile in option:
                        self.game.nextPlayer.board_state[self.game.squares-tile] = False
                self.ids.log_text.text += "\n" + self.game.currentPlayer.name + " uncovered " + str(option)    
                self.game.log.add_log(self.game.currentPlayer.name + " uncovered " + str(option))

            if found:  
                self.refresh_tiles()
                if self.round_won():
                    self.end_round()
                    return

                self.ids.roll_two_btn.disabled = False
                self.ids.select_option_btn.disabled = True
                self.ids.to_cover.state = 'normal'
                self.ids.to_uncover.state = 'normal'
                self.ids.to_cover.disabled = True
                self.ids.to_uncover.disabled = True
        else:
            log_msg = "\n" + "Turns changed"
            self.game.log.add_log(log_msg)
            self.ids.log_text.text += "\n" + log_msg
            self.switch_player_turns()
            self.ids.dice_one_image.source = "res/zero.jpg"
            self.ids.dice_two_image.source = "res/zero.jpg"
            self.ids.turn_identifier.text = "Current turn: " + self.game.currentPlayer.name
            self.ids.select_option_btn.text = "Select"
            self.ids.select_option_btn.disabled = True
            self.ids.roll_two_btn.disabled = False if self.game.currentPlayer.name != "Computer" else True
        
        self.ids.roll_one_btn.disabled = not self.check_roll_one()

    # Function Name: check_roll_one
    # Purpose: To check if a player is eligible to have to option to roll one dice. 
    # Parameters:
    # Return Value:
    # Algorithm:
    #             1) Iterate 7-n tiles through the currentPlayer's board_state.
    #             2) If any False value is found, return False. Else return True
    # Assistance Received: none    
    def check_roll_one(self):
        for index in range(len(self.game.currentPlayer.board_state)-6):
            if not self.game.currentPlayer.board_state[index]:
                return False
        return True

    # Function Name: start_next_round
    # Purpose: To initialize all the necessary variables for the game and set the 
    #          widgets according to the initialize game state. 
    # Parameters:
    #             instance, a variable that holds the info on widget that triggers the function
    # Return Value:
    # Algorithm:
    #             1) Check which ToggleButton was selected for the number of squares.
    #             2) If the input is valid, remove the end_round_screen.
    #             3) Call the setup_game function and pass the game_box member as parameter.
    #             4) Add the game_box widget back to the full_screen widget.
    # Assistance Received: none 
    def start_next_round(self, instance):
        self.game.round_num += 1
        valid_input = True
        if self.ids.nine.state == 'down':
            self.game.squares = 9
        elif self.ids.ten.state == 'down':
            self.game.squares = 10
        elif self.ids.eleven.state == 'down':
            self.game.squares = 11
        elif self.ids.twelve.state == 'down':
            self.game.squares = 12
        else:
            print("Select one squares value")
            valid_input = False
        
        if valid_input:
            self.ids.full_screen.remove_widget(self.ids.end_round_screen)

            self.game.log.add_log("Switching to game screen")
            self.ids.dice_one_image.source = "res/zero.jpg"
            self.ids.dice_two_image.source = "res/zero.jpg"
            self.ids.log_text.text += "\n" + "Switching to game screen"
            self.setup_game(self.game)
            self.ids.full_screen.add_widget(self.game_box)

    # Function Name: give_advantage
    # Purpose: To calculate which square should be covered to provide advantage
    # to the decided player, and then cover it. 
    # Parameters:
    #             player, a Player class variable. It holds the info of a player who has 
    #               to be given the advantage.
    # Return Value:
    # Algorithm:
    #             1) Add every digit of score. If the digit is equal or more than the
    #               number of squares, then repeat the process until it passes that condition.
    #             2) The result should be passsed into the player's cover
    #               function to cover that square.
    # Assistance Received: none             
    def give_advantage(self, player):
        q, r, sum = self.game.round_winning_score, 0, 0
        while q > 0:
            r = q % 10
            q = int(q / 10)
            sum += r
            if q <= 0 and sum > self.game.squares:
                q = sum + self.game.round_winning_score
                sum = 0
                if q < 0:
                    print(q)
                    break
    
        if sum > 0 and sum <= self.game.squares:
            self.game.log.add_log(player.name + " was given the advantage. The square " + str(sum) + " will be covered beforehand.")
            self.ids.log_text.text += "\n" + player.name + " was given the advantage. The square " + str(sum) + " will be covered beforehand."
            
            player.board_state[self.game.squares-sum] = True
            if player.name == self.game.currentPlayer.name:
                self.game.currentPlayer.advantage_square = sum
                self.game.nextPlayer.advantage_square = 0
            elif player.name == self.game.nextPlayer.name:
                self.game.nextPlayer.advantage_square = sum
                self.game.currentPlayer.advantage_square = 0

        else:
            self.game.log.add_log("Advantage count not be given.")
            self.ids.log_text.text += "\n" + "Advantage count not be given."
            
        self.refresh_tiles()

    # Function Name: write_to_file
    # Purpose: To save the current game state into a file 
    # Parameters:
    #             instance, a variable that holds the info on widget that triggers the function
    # Return Value:
    # Algorithm:
    #             1) Get all the required information from the GameScreen by using widget ids.
    #             2) Validate the naming for the file.
    #             3) Create a new file with the name the user entered if the file doesn't exist.
    #             4) Write the game state information into the file according to the serialization layout.
    # Assistance Received: none 
    def write_to_file(self, instance):
        if len(self.ids.file_name.text) > 0:

            player1_board_state, player2_board_state = self.game.currentPlayer.board_state, self.game.nextPlayer.board_state
            player1_name, player2_name= self.game.currentPlayer.name, self.game.nextPlayer.name
            player1_score, player2_score = self.game.currentPlayer.score, self.game.nextPlayer.score 

            first_turn = self.game.currentPlayer.name if self.game.currentPlayer.first_turn else self.game.nextPlayer.name
            next_turn = self.game.currentPlayer.name
            

            filename = self.ids.file_name.text
            valid_filename = True

            # filename cannot be blank or have /\?<>:*"| in it
            if len(filename) == 0:
                valid_filename = False
            else:
                for i in range(len(filename)):
                    if filename[i] == '?' or filename[i] == '/' or filename[i] == '\\' or filename[i] == '<' or filename[i] == '>' or filename[i] == ':' or filename[i] == '\"' or filename[i] == '|' or filename[i] == '*':
                        valid_filename = False
                        break
            if not valid_filename:
                print("Invalid filename : You cannot have a blank filename or the characters /\\?<>:*\" in it.")
                return

            filepath = os.path.join('canoga_venv/saved_games', filename)
            if not os.path.exists('canoga_venv/saved_games'):
                os.makedirs('canoga_venv/saved_games')
            f = open(filepath + ".txt", "w")

            f.write(player1_name + ":" + "\n")
            f.write("    Squares: ")
            for index in range(len(player1_board_state)):
                if not player1_board_state[index]:
                    f.write(str(index+1))
                else:
                    f.write("*")
                if index < (len(player1_board_state) - 1):
                    f.write(" ")

            f.write("\n")
            f.write("    Score: ")
            f.write(str(player1_score) + "\n\n")
            f.write(player2_name + ":" + "\n")
            f.write("    Squares: ")
            for index in range(len(player2_board_state)):
                if not player2_board_state[index]:
                    f.write(str(index+1) + " ")
                else:
                    f.write("* ")
            f.write("\n")
            f.write("    Score: ")
            f.write(str(player2_score) + "\n\n")
            if self.game.first_turn: 
                f.write("First  turn: ")
            else:
                f.write("First turn: ")
            f.write(first_turn + "\n")
            f.write("Next turn: " + next_turn + "\n\n")

            if self.game.dice_rolls:
                f.write("Dice: \n")
                for dice_roll in self.game.dice_rolls:
                    f.write("   ")
                    for dice in dice_roll:
                        f.write(str(dice) + " ")
                    f.write("\n")

            f.close()
            self.manager.current = "main_screen"

    # Function Name: cancel_save
    # Purpose: To go back to the latest game screen 
    # Parameters:
    #             
    # Return Value:
    # Algorithm:
    #             1) Remove the save_box widget from the full_screen widget.
    #             2) Add the game_box widget back to the full_Screen widget.
    # Assistance Received: none 
    def cancel_save(self, instance):
        self.ids.full_screen.remove_widget(self.ids.save_box)
        self.ids.full_screen.add_widget(self.game_box)

    # Function Name: save_game
    # Purpose: To display widgets that allow a user to enter file name before saving a game. 
    # Parameters:
    # Return Value:
    # Algorithm:
    #             1) Remove the game_box widget from the full_screen.
    #             2) Create a save_box widget that consists of widgets to let user enter file name
    #             and initiate the save.
    #             3) Add save_box widget to the full_screen.
    # Assistance Received: none     
    def save_game(self):
        self.game_box = self.ids.game_box

        self.ids.full_screen.remove_widget(self.ids.game_box)

        save_box = BoxLayout(orientation="vertical", size_hint=(0.7, 1), pos_hint={'center_x': 0.5, 'center_y':0.5}, padding=60, spacing=20)
        self.ids["save_box"] = save_box

        save_title = Label(text="Save Game", size_hint=(0.5,0.1))
        save_box.add_widget(save_title)
        file_name_label = Label(text="Enter file name", size_hint=(0.5,0.1))
        save_box.add_widget(file_name_label)
        filename = TextInput(multiline=False, size_hint=(1,0.1))
        self.ids["file_name"] = filename
        save_box.add_widget(filename)

        save_btn = Button(text="Save and Quit", size_hint=(0.5,0.1))
        save_btn.bind(on_press=self.write_to_file)
        cancel_btn = Button(text="Cancel and Go Back", size_hint=(0.5,0.1))
        cancel_btn.bind(on_press=self.cancel_save)

        save_box.add_widget(save_btn)
        save_box.add_widget(cancel_btn)

        self.ids.full_screen.add_widget(save_box)

    # Function Name: quit_game
    # Purpose: To switch to the main screen 
    # Parameters:
    #             instance, a variable that holds the info on widget that triggers the function
    # Return Value:
    # Algorithm:
    #             1) Set the current screen to be the "main_screen"
    # Assistance Received: none 
    def quit_game(self):
        self.manager.current = 'main_screen'

    # Function Name: end_game
    # Purpose: To display the end game screen to the user.
    # Parameters:
    #             instance, a variable that holds the info on widget that triggers the function
    # Return Value:
    # Algorithm:
    #             1) Remove the end round widget.
    #             2) Create new widgets and add them into the end_game BoxLayout 
    #                to insert into the full_screen widget.
    # Assistance Received: none 
    def end_game(self, instance):
        self.ids.end_round_screen.remove_widget(self.ids.end_round_box)

        end_game_box = BoxLayout(orientation="vertical", size_hint=(0.5, 0.7), pos_hint={'center_x': 0.5})
        game_over_label = Label(text="Game Over", size_hint=(1,0.2))
        game_winner_label = Label(size_hint=(1,0.2))
        winner_score_label = Label(size_hint=(1,0.2))
        if self.game.game_winner != "Draw":
            game_winner_label.text="Winner: " + self.game.game_winner
            self.game.log.add_log(self.game.game_winner + " won the game.")
            winner_score_label.text= "Score: " + str(self.game.game_winning_score)
        else:
            game_winner_label.text= "Game was a draw."
            self.game.log.add_log( "Game was a draw.")
            winner_score_label.text = "Both players scored " + str(self.game.currentPlayer.score)
            self.game.log.add_log("Both players scored " + str(self.game.currentPlayer.score))

        thank_you_label = Label(text="Thank you for playing!", size_hint=(1,0.2))
        go_to_main_btn = Button(text="Go back to Main", size_hint=(1,0.2))
        go_to_main_btn.bind(on_press=self.switch_to_main)
        end_game_box.add_widget(game_over_label)
        end_game_box.add_widget(game_winner_label)
        end_game_box.add_widget(winner_score_label)
        end_game_box.add_widget(thank_you_label)
        end_game_box.add_widget(go_to_main_btn)
        
        self.ids.end_round_screen.add_widget(end_game_box)

    # Function Name: switch_to_main
    # Purpose: To switch to the main screen 
    # Parameters:
    #             instance, a variable that holds the info on widget that triggers the function
    # Return Value:
    # Algorithm:
    #             1) Set the current screen to be the "main_screen"
    # Assistance Received: none     
    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'