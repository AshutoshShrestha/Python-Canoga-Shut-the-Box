from kivy.uix.screenmanager import Screen
from views.GameModeScreen import GameModeScreen
from views.LoadFileScreen import LoadFileScreen

class MainScreen(Screen):

    # Function Name: new_game
    # Purpose: To add the mainscreen to the screenmanager and switch to game mode screen
    # Parameters:
    #             
    # Return Value: none (void)
    # Algorithm:
    #             1) Switch to GameModeScreen()
    #             2) Add the MainScreen widget into the screen manager.
    # Assistance Received: none

    def new_game(self):
        print("Switching to new game screen")
        self.manager.switch_to(GameModeScreen())
        self.manager.add_widget(MainScreen())
        print(self.manager.screen_names)

    # Function Name: load_game
    # Purpose: To display saved games 
    # Parameters:
    #             
    # Return Value: none (void)
    # Algorithm:
    #             1) Initialize a LoadScreen instance.
    #             2) Call the load_files function.
    #             3) Switch to LoadScreen
    #             4) Add the MainScreen widget into the screen manager.
    # Assistance Received: none 
    def load_game(self):
        print("Switching to load game screen")
        load_screen = LoadFileScreen()
        load_screen.load_files()
        self.manager.switch_to(load_screen)
        self.manager.add_widget(MainScreen())
        print(self.manager.screen_names)