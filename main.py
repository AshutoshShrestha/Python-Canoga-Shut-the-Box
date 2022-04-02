import sys
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
sys.path.append(".")
from views.MainScreen import MainScreen

import kivysome 
kivysome.enable("https://kit.fontawesome.com/474bbb9801.js", group=kivysome.FontGroup.SOLID)

# setting the minimum window size
Window.size = (900, 650)
Window.minimum_width, Window.minimum_height = Window.size

# loading up the layout as an entire string
Builder.load_string('''
#:import icon kivysome.icon
#:import Label kivy.uix.label.Label

<GameScreen>:
    name: "game_screen"
    BoxLayout:
        id: full_screen
        size: root.size
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: (60/255, 0, 79/255, 0.91)
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            id: title_box
            size_hint: (1, 0.05)
            canvas.before:
                Color:
                    rgba: (1,1,1,1)
                Line:
                    points: (0, self.top*0.95, self.width, self.top*0.95)
                    width: 1
            Label:
                markup: True # Always turn markup on
                text: "Canoga"

        BoxLayout:
            id: game_box
            padding: 10
            spacing: 40
            canvas:
                Color:
                    rgba: (1,1,1,1)
                Line:
                    points: (self.width*0.7, root.height*0.95, self.width*0.7, 0)
                    width: 1
            BoxLayout:
                orientation: "vertical"
                size_hint: (0.7, 1)
                spacing: 20
                BoxLayout:
                    size_hint: (1, 0.2)
                    BoxLayout:
                        orientation: "vertical"
                        size_hint: (0.7, 1)
                        Label:
                            text: "Score"
                            size_hint_x: 0.8
                        BoxLayout:
                            orientation: "vertical"
                            spacing: 10
                            Label:
                                id: player1_score_label
                                text: "Player1: " + str(15)
                                size_hint_x: 0.8
                                canvas.before:
                                    Color:
                                        rgba: (83/255, 32/255, 94/255, 0.9)
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                            Label:
                                id: player2_score_label
                                text: "Player2: " + str(24)
                                size_hint_x: 0.8
                                canvas.before:
                                    Color:
                                        rgba: (83/255, 32/255, 94/255, 0.9)
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                    BoxLayout:
                        orientation: "vertical"
                        size_hint: (0.3, 1)
                        Label:
                            text: "Box States"
                        BoxLayout:
                            canvas.before:
                                Color:
                                    rgba: (0, 1, 0, 0.7)
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                            Label:
                                id: covered_label
                                text: "Covered"
                        BoxLayout:
                            canvas.before:
                                Color:
                                    rgba: (1, 0, 0, 1)
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                            Label:
                                id: uncovered_label
                                text: "Uncovered"
                            
                BoxLayout:
                    orientation: "vertical"
                    size_hint: (1, 0.35)
                    Label: 
                        id: player1_board_label
                        size_hint: (1, 0.2)
                        text: "Player1's board"
                    StackLayout:
                        id: player1_board
                        size_hint: (1, 0.3)
                        spacing: 5
                    Label: 
                        id: player2_board_label
                        size_hint: (1, 0.2)
                        text: "Player2's board"
                    StackLayout:
                        id: player2_board
                        spacing: 5
                        size_hint: (1, 0.3)
                BoxLayout:
                    orientation: "vertical"
                    size_hint: (1, 0.45)
                    BoxLayout:
                        size_hint: (1, 0.1)
                        Label: 
                            id: first_turn_identifier
                            text: ""
                        Label:
                            id: turn_identifier
                            text: ""    
                    BoxLayout:
                        size_hint: (1, 0.5)
                        BoxLayout:
                            size_hint_y: 0.9
                            padding: 20
                            spacing: 20
                            Button:
                                id: roll_one_btn
                                text: "Roll only 1"
                                disabled: True
                                size_hint: (0.3, 0.7)
                                on_press: root.roll_dice(True)
                            Button:
                                id: roll_two_btn
                                text: "Roll" 
                                size_hint: (0.3, 0.7)
                                on_press: root.roll_dice(False)
                        BoxLayout:
                            spacing: 10
                            Image:
                                id: dice_one_image
                                canvas.before:
                                    Color:
                                        rgba: (114/255,60/255,167/255,0.91)
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                                source: "res/zero.jpg"
                            Image:
                                id: dice_two_image
                                canvas.before:
                                    Color:
                                        rgba: (114/255,60/255,167/255,0.91)
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                                source: "res/zero.jpg" 
                    BoxLayout:
                        orientation: "vertical"  
                        size_hint: (1, 0.4)    
                        background_color: (1, 1, 1, 1)
                        padding: 10
                        canvas.before:
                            Color:
                                rgba: (1, 1, 1, 1)
                            Rectangle:
                                size: self.size
                                pos: self.pos
                        ScrollView:
                            do_scroll_x: False
                            do_scroll_y: True
                            bar_width: 8
                            bar_color: 1, 0, 0, 1   # red
                            bar_inactive_color: 0, 0, 1, 1   # blue
                            effect_cls: "ScrollEffect"
                            scroll_type: ['bars']
                            Label:
                                id: log_text
                                color: 0,0,0,1
                                size_hint: (1, None)
                                size: self.size
                                text_size: self.size
            BoxLayout:
                orientation:"vertical"
                size_hint: (0.3, 1)
                BoxLayout:
                    size_hint: (1, 0.85)
                    orientation:"vertical" 
                    Label:
                        text: "Options"
                        size_hint: (1, 0.1)
                        color: (0,0,0,1)
                        canvas.before:
                            Color: 
                                rgba: (1,1,1,1)
                            Rectangle:
                                size: self.size
                                pos: self.pos
                    BoxLayout:
                        id: user_options
                        orientation:"vertical"
                        size_hint: (1, 0.8)
                        ToggleButton:
                            id: to_cover
                            text: "Cover"
                            size_hint: (1, 0.1)
                            group: "option"
                        ScrollView:
                            size_hint_y: 0.4
                            do_scroll_x: False
                            do_scroll_y: True
                            bar_width: 8
                            bar_color: 1, 0, 0, 1   # red
                            bar_inactive_color: 1, 1, 1, 1   # blue
                            effect_cls: "ScrollEffect"
                            scroll_type: ['bars']
                            visible: True if (to_cover.state=='down') else False
                            size_hint_x: 1 if self.visible else 0   
                            opacity: 1 if self.visible else 0
                            canvas.before:
                                Color: 
                                    rgba: (1,1,1,1)
                                Rectangle:
                                    size: self.size
                                    pos: self.pos
                            BoxLayout:
                                id: cover_options
                                size_hint_y: None
                                height: self.minimum_height
                                orientation: "vertical"
                                spacing: 3
                        ToggleButton:
                            id: to_uncover
                            text: "Uncover"
                            size_hint: (1, 0.1)
                            group: "option"
                        ScrollView: 
                            size_hint_y: 0.4
                            do_scroll_x: False
                            do_scroll_y: True
                            bar_width: 8
                            bar_color: 1, 0, 0, 1   # red
                            bar_inactive_color: 1, 1, 1, 1   # blue
                            effect_cls: "ScrollEffect"
                            scroll_type: ['bars']
                            visible: True if (to_uncover.state=='down') else False
                            size_hint_x: 1 if self.visible else 0
                            opacity: 1 if self.visible else 0      
                            canvas.before:
                                Color: 
                                    rgba: (1,1,1,1)
                                Rectangle:
                                    size: self.size
                                    pos: self.pos
                            BoxLayout:
                                id: uncover_options
                                orientation: "vertical"
                                spacing: 3   
                                size_hint_y: None
                                height: self.minimum_height
                    BoxLayout:
                        orientation: "vertical"
                        size_hint:(1, 0.2)
                        Button:
                            id: help_btn
                            size_hint: (1, 0.3)
                            text: "Help"
                            disabled: True if (not roll_two_btn.disabled or select_option_btn.text!="Select") else False
                            on_press: root.provide_help()
                        Button:
                            id: select_option_btn
                            size_hint: (1, 0.3)
                            text: "Select"
                            disabled: False if (help_btn.text == "Help") else True
                            on_press: root.select_option(to_cover.state, to_uncover.state)
                BoxLayout:
                    size_hint: (1, 0.15)
                    Button:
                        text:"Save"
                        size_hint: (0.3, 0.5)
                        disabled: True if (roll_two_btn.disabled and help_btn.text=="Help")else False
                        on_press: root.save_game()
                    Button:
                        text:"Quit"
                        size_hint: (0.3, 0.5)
                        disabled: True if roll_two_btn.disabled else False
                        on_press: root.quit_game()

<MainScreen>:
    name: "main_screen"
    BoxLayout:
        orientation: "vertical"
        size_hint: (0.3,0.2)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        spacing: 40
        Button:
            text: "New Game"
            on_press: root.new_game()
        Button:
            text: "Load Game"
            on_press: root.load_game()

<GameModeScreen>:
    name: "mode_screen"
    BoxLayout:
        orientation: "vertical"
        spacing: 30
        Label:
            text: "Pick Mode"
            size_hint: (1, 0.1)
        BoxLayout:
            orientation: "vertical"
            size_hint: (0.3, 0.2) #(0.3,0.2)
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}
            spacing: 40
            ToggleButton:
                id: single
                text: "Player vs Computer"
                group: "mode"
            ToggleButton:
                id: multi
                text: "Player vs Player"
                group: "mode"
        BoxLayout:
            orientation: 'vertical'
            size_hint: (0.5, 0.2)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            spacing: 50
            BoxLayout:
                size_hint: (1, 0.5)
                visible: True if (single.state=='down' or multi.state=='down') else False
                size_hint_x: 1 if self.visible else 0
                opacity: 1 if self.visible else 0
                Label:
                    id: player1_name_label
                    text: 'Player name: ' if (single.state=='down') else 'Player 1 name: '
                TextInput:
                    id: player1_name
            BoxLayout:
                size_hint: (1, 0.5)
                visible: True if (multi.state=='down') else False
                size_hint_x: 1 if self.visible else 0
                opacity: 1 if self.visible else 0
                Label:
                    id: player2_name_label
                    text: 'Player 2 name: '
                TextInput:
                    id: player2_name
        Label:
            text: "Pick Squares"
            size_hint: (1, 0.1)
        BoxLayout:
            size_hint: (0.5, 0.1) #(0.8,0.2)
            pos_hint: {'center_x': 0.5, 'center_y': 0.8}
            spacing: 40
            ToggleButton:
                id: nine
                text: "9"
                group: "squares"
            ToggleButton:
                id: ten
                text: "10"
                group: "squares"
            ToggleButton:
                id: eleven
                text: "11"
                group: "squares"
            ToggleButton:
                id: twelve
                text: "12"
                group: "squares"
        BoxLayout:
            size_hint: (0.5, 0.1)
            pos_hint: {'center_x': 0.5, 'center_y':0.5}
            Button:
                text: "Start"
                on_press: root.start_game(root.parent)

<EndRoundScreen>:
    name: "end_round_screen"
    BoxLayout:
        id: end_round_screen
        BoxLayout:
            id: end_round_box
            orientation: "vertical"
            Label:
                size_hint: (1, 0.1)
                text: "Round Over"
            Label:
                id: winner_label
                size_hint: (1, 0.1)
                text: "Winner: "
            Label:
                id: winning_score_label
                size_hint: (1, 0.1)
                text: "Winner: "
            BoxLayout:
                size_hint: (0.5,0.2)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                Button:
                    id: finish_game_btn
                    text: "Finish Game"
                    on_press: root.end_game()
                ToggleButton:
                    id: start_next_round
                    text: "Go another Round"
            BoxLayout:
                size_hint: (1, 0.5)
                orientation: "vertical"
                pos_hint: {'center_x': 0.5, 'center_y': 1}
                visible: True if (start_next_round.state=='down') else False
                size_hint_x: 1 if self.visible else 0
                opacity: 1 if self.visible else 0
                Label:
                    size_hint: (1, 0.2) 
                    text: "Pick Squares"
                BoxLayout:
                    size_hint: (1, 0.2) 
                    spacing: 20
                    padding: 40
                    ToggleButton:
                        id: nine
                        text: "9"
                        group: "squares"
                    ToggleButton:
                        id: ten
                        text: "10"
                        group: "squares"
                    ToggleButton:
                        id: eleven
                        text: "11"
                        group: "squares"
                    ToggleButton:
                        id: twelve
                        text: "12"
                        group: "squares"
                BoxLayout:
                    size_hint: (0.5, 0.2)
                    pos_hint: {'center_x': 0.5, 'center_y':0.5}
                    padding: 50
                    Button:
                        text: "Start"
                        on_press: root.start_next_round()

<LoadFileScreen>:
    name: "load_screen"
    BoxLayout:
        id: load_screen_box
        orientation: "vertical"
        size_hint: (0.4,1)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        spacing: 30
        Label:
            size_hint: (1, 0.1)
            text: "Loaded Files"
            color: (1,1,1,1)
        
        BoxLayout:
            size_hint_y: 0.8
            id: saved_games_box
            orientation: "vertical"
            spacing: 5
            ScrollView:
                id: saved_games_scroller
                do_scroll_x: False
                do_scroll_y: True
                bar_width: 8
                bar_color: 1, 0, 0, 1   # red
                bar_inactive_color: 1, 1, 1, 1   # blue
                effect_cls: "ScrollEffect"
                scroll_type: ['bars']
                size_hint_y: None
                size: self.size
        # BoxLayout:
        #     id: saved_games_box
        #     orientation: "vertical"
        #     padding: 40
        #     spacing: 20
        #     size_hint: (1, 0.8)
        Button:
            id: load_btn
            text: "Load"
            disabled: True if (len(saved_games_box.children) <= 1) else False
            on_press: root.load_game()
            size_hint: (1, 0.1)


<QuitPopup>:
    size_hint: 0.4, 0.4
    auto_dismiss: False

    title: "Did you save your game?"
    
''')

# the driver class that has a function that runs the application
class CanogaApp(App):
     def build(self):
        # Create the screen manager
        sm = ScreenManager()

        sm.add_widget(MainScreen(name='main_screen'))
        sm.current = 'main_screen'
        
        return sm
    
if __name__=="__main__":
    CanogaApp().run()
