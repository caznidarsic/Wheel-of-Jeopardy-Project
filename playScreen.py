# play screen class
from re import X
import pygame
import button
import pygame.gfxdraw
import MainDriver
import textDisplay
import textTitle
import jeopardyBoard
import wheel
import random
from flattenList import flattenList
import textDisplayLeft
import textDisplayQuestionWrap
import util


class PlayScreen():
    def __init__(self, screen, clock, height, width):
        self.screen = screen
        self.clock = clock
        self.height = height
        self.width = width
        self.background_input = pygame.image.load(util.resourcePath(
            'images/space_background.jpeg')).convert()
        self.background = pygame.transform.smoothscale(
            self.background_input, (self.width, self.height))
        self.box_color = (255, 255, 255)
        # title boxes
        self.categories = []
        self.questions = []
        self.answers = [[]]
        self.finalScores = []
        self.extraSpinFunctions = False
        self.categorySelected = False

        # self.game = MainDriver.Game()

    # main menu

    def getInput(self, numPlayers, playerList):
        def refresh_all_player_score():
            for x in range(len(game.players)):
                scoreTextArray[x].setText(
                    str(game.players[x].score))
                self.finalScores[x] = game.players[x].score
                # print("[LOG]: Player " + str(x) +
                #       " " + str(self.finalScores[x]))

        def refresh_current_player_indicator():
            for x in range(len(game.players)):
                nameTextArray[x].setText(
                    game.players[x].name + " (" + str(game.players[x].free_token) + ")")
            nameTextArray[game.current_player].setText(
                "->"+nameTextArray[game.current_player].text_input+"<-")

        def randomly_assign_answers():
            tmp_list = [i for i in range(1, 5)]
            random.shuffle(tmp_list)
            game.correctAnswer = tmp_list.index(1)
            ansAText.setText(question[tmp_list[0]])
            ansBText.setText(question[tmp_list[1]])
            ansCText.setText(question[tmp_list[2]])
            ansDText.setText(question[tmp_list[3]])

        # initializing sounds
        pygame.mixer.init()
        back = pygame.mixer.Sound(util.resourcePath('sounds/back.mp3'))
        correct = pygame.mixer.Sound(util.resourcePath('sounds/correct.mp3'))
        free_token = pygame.mixer.Sound(
            util.resourcePath('sounds/free_token.mp3'))
        incorrect = pygame.mixer.Sound(
            util.resourcePath('sounds/incorrect_cut.mp3'))
        negative = pygame.mixer.Sound(util.resourcePath('sounds/negative.mp3'))
        q_intro = pygame.mixer.Sound(util.resourcePath('sounds/q_intro.mp3'))
        selection = pygame.mixer.Sound(
            util.resourcePath('sounds/selection.mp3'))
        wheel_sound = pygame.mixer.Sound(
            util.resourcePath('sounds/wheel_cut1.mp3'))

        show_decision = False
        clickable_mem = []

        def wait_for_player_decision():
            nonlocal show_decision
            show_decision = True
            for x in range(0, 4):
                clickable_mem.append(answerButtonArray[x].clickable)
                answerButtonArray[x].setClickable(False)
            clickable_mem.append(spin_button.clickable)
            spin_button.setClickable(False)

        def player_decision_resolved():
            nonlocal show_decision
            show_decision = False
            for x in range(0, 4):
                answerButtonArray[x].setClickable(clickable_mem[x])
            spin_button.setClickable(clickable_mem[4])
            clickable_mem.clear()
            # force set clicked to false
            no_button.clicked = False
            yes_button.clicked = False
            refresh_all_player_score()
            refresh_current_player_indicator()

        def give_all_player_tokens():
            for x in range(len(game.players)):
                game.players[x].add_token()

        def updateCategoryNames():
            # parse categories to be displayed
            self.categories.clear()
            for x in range(6):
                self.categories.append(game.questions[x][0])
            self.categories = flattenList(self.categories)

        def emptyQuestionText():
            questionText.addText("")
            ansAText.setText("")
            ansBText.setText("")
            ansCText.setText("")
            ansDText.setText("")

        # initialize game instance
        game = MainDriver.Game(numPlayers, playerList)

        # set up final score array
        self.finalScores.clear()
        for x in range(len(game.players)):
            self.finalScores.append(0)

        # parse categories to be displayed
        updateCategoryNames()

        # drawing rectangleS
        pygame.draw.rect(self.background, self.box_color, pygame.Rect(
            50, 50, 600, 400),  2, 3)  # Wheel section
        # pygame.draw.rect(self.background, self.box_color, pygame.Rect(
        #     950, 50, 600, 480),  2, 3)  # Jeopardy section
        pygame.draw.rect(self.background, self.box_color, pygame.Rect(
            680, 50, 240, 400),  2, 3)  # Player info section
        pygame.draw.rect(self.background, self.box_color, pygame.Rect(
            50, 480, 870, 90),  2, 3)  # status/ user promp
        pygame.draw.rect(self.background, self.box_color, pygame.Rect(
            50, 585, 1000, 240),  2, 3)  # questions / answers
        pygame.draw.rect(self.background, self.box_color, pygame.Rect(
            1060, 587, 50, 50),  2, 3)  # asnwer question button: A
        pygame.draw.rect(self.background, self.box_color, pygame.Rect(
            1060, 650, 50, 50),  2, 3)  # asnwer question button: B
        pygame.draw.rect(self.background, self.box_color, pygame.Rect(
            1060, 712, 50, 50),  2, 3)  # asnwer question button: C
        pygame.draw.rect(self.background, self.box_color, pygame.Rect(
            1060, 773, 50, 50),  2, 3)  # asnwer question button: D

        # drawing text
        wheelText = textDisplay.TextDisplay(
            "", 46, 1320, 780)
        spinCountText = textDisplay.TextDisplay(
            "Spins left: ", 26, 150, 425)
        spinCountNum = textDisplay.TextDisplay(
            str(game.spins_left), 26, 230, 425)
        narration = textDisplay.TextDisplay(
            "Press \"SPIN\" to spin the wheel.", 26, 1340, 677)

        # Questions/Answer Display
        questionText = textDisplayQuestionWrap.Pane("No question to answer yet",
                                                    32, 870, 90, 480, 507)
        ansAText = textDisplayLeft.TextDisplayLeft(
            "answer A", 26, 75, 585+12)
        ansBText = textDisplayLeft.TextDisplayLeft(
            "answer B", 26, 75, 585+12+63*1)
        ansCText = textDisplayLeft.TextDisplayLeft(
            "answer C", 26, 75, 585+12+63*2)
        ansDText = textDisplayLeft.TextDisplayLeft(
            "answer D", 26, 75, 585+12+63*3)

        # create text for each player to display scores
        nameTextArray = []
        scoreTextArray = []
        for x in range(len(game.players)):
            nameTextArray.append(textDisplay.TextDisplay(
                game.players[x].name, 26, self.width/2, self.height - 810 + 70*x))
            scoreTextArray.append(textDisplay.TextDisplay(
                str(game.players[x].score), 26, self.width/2, self.height - 780 + 70*x))
        refresh_current_player_indicator()

        # self.screen.blit(self.background, (0, 0))
        board = jeopardyBoard.JeopardyBoard()
        myWheel = wheel.Wheel()

        # buttons
        game_completed_button = button.Button(
            "SEE RESULTS", 32, self.width*(1 - 1/8), self.height - 50, False)
        quit_to_main_button = button.Button(
            "QUIT TO MAIN", 32, self.width/10, self.height - 50)
        spin_button = button.Button(
            "SPIN", 50, 1320, 727)
        yes_button = button.Button(
            "Yes", 32, 1220, 627)
        no_button = button.Button(
            "No", 32, 1420, 627)

        # create array full of answer buttons from A to D
        answerButtonArray = [button.Button(
            "A", 48, 1085, 592 + 22.5, False), button.Button(
            "B", 48, 1085, 677, False), button.Button(
            "C", 48, 1085, 738.5, False), button.Button(
            "D", 48, 1085, 800.5, False)]

        # DEBUG
        # give_all_player_tokens()

        show_spin = True
        loop = True
        enterCategorySelection = False
        while loop:

            # draw elements
            self.screen.blit(self.background, (0, 0))
            game_completed_button.draw(self.screen)
            # game_completed_button.setClickable(True)
            quit_to_main_button.draw(self.screen)

            for x in range(0, 4):
                answerButtonArray[x].draw(self.screen)

            wheelText.draw(self.screen)
            spinCountText.draw(self.screen)
            spinCountNum.draw(self.screen)
            narration.draw(self.screen)
            board.draw(self.screen, self.categories)
            ansAText.draw(self.screen)
            ansBText.draw(self.screen)
            ansCText.draw(self.screen)
            ansDText.draw(self.screen)
            questionText.draw(self.screen)
            myWheel.draw(self.screen)

            # draw player names/scores
            for x in nameTextArray:
                x.draw(self.screen)
            for x in scoreTextArray:
                x.draw(self.screen)

            if show_spin:
                spin_button.draw(self.screen)

            if show_decision:
                narration.setText(
                    "Use a free turn token?")
                yes_button.draw(self.screen)
                no_button.draw(self.screen)

            spun = False

            # event handlers
            for event in pygame.event.get():
                # game window handlers
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if game_completed_button.clicked:
                    selection.play()
                    return True
                if quit_to_main_button.clicked:
                    back.play()
                    loop = False

                # answer selection handlers
                for x in range(0, 4):
                    if answerButtonArray[x].clicked and isinstance(spin_result, int):
                        if x == game.correctAnswer:
                            correct.play()
                            game.players[game.current_player].add_score(
                                game.current_question_value)
                            board.removeSquare(
                                self.screen, spin_result, game.get_question_index(spin_result))
                            # set all answer buttons to unclickable
                            for x in range(0, 4):
                                answerButtonArray[x].setClickable(False)

                            # round 2 logic
                            if game.spins_left <= 0 or game.board_empty:
                                game.current_round += 1

                                if game.current_round > 2:
                                    # TODO: complete game and load final score board screen
                                    emptyQuestionText()
                                    questionText.addText(
                                        "Game over! Press \"SEE RESULTS\" to view game results.")
                                    spin_button.setClickable(False)
                                    game_completed_button.setClickable(True)
                                    quit_to_main_button.setClickable(False)
                                else:
                                    self.extraSpinFunctions = True
                                    emptyQuestionText()
                                    questionText.addText(
                                        "Round 1 over! Press \"SPIN\" to begin Round 2.")
                                    spin_button.setClickable(True)

                            else:
                                spin_button.setClickable(True)
                                narration.setText(
                                    "Press \"SPIN\" to spin the wheel.")

                        else:
                            # prevent incorrect answer from being selected twice
                            answerButtonArray[x].setClickable(False)
                            incorrect.play()
                            game.players[game.current_player].sub_score(
                                game.current_question_value)
                            if game.players[game.current_player].free_token > 0:
                                wait_for_player_decision()
                            else:
                                game.next_player()
                        refresh_all_player_score()
                        refresh_current_player_indicator()

                # jeopardy board category selection button handlers
                for x in range(6):
                    if board.categorySelectionButtons[x].clicked and enterCategorySelection:
                        spin_result = x
                        enterCategorySelection = False
                        board.showButtons(False)

                        question = game.get_category_next_question(x)
                        print(question)
                        if question != None:
                            q_intro.play()
                            questionText.addText(question[0])
                            randomly_assign_answers()
                            # set the four answer buttons to clickable
                            for x in range(0, 4):
                                answerButtonArray[x].setClickable(True)
                        else:
                            negative.play()
                            emptyQuestionText()
                            questionText.addText("Category empty, Spin again!")
                            spin_button.setClickable(True)
                            narration.setText(
                                "Press \"SPIN\" to spin the wheel.")

                        # make sure none of the jeopardy board buttons are set to "clicked"
                        for x in range(6):
                            board.categorySelectionButtons[x].clicked = False

                        refresh_all_player_score()
                        refresh_current_player_indicator()

                # other handlers
                # ...

                if show_decision:
                    if yes_button.clicked:
                        selection.play()
                        game.players[game.current_player].free_token -= 1
                        narration.setText(
                            game.players[game.current_player].name + " uses a free turn token.")
                        player_decision_resolved()
                    if no_button.clicked:
                        selection.play()
                        game.next_player()
                        narration.setText(
                            game.players[game.current_player].name + "'s turn.")
                        player_decision_resolved()

                if spin_button.clicked:
                    # set the spin button to unclickable
                    spin_button.setClickable(False)
                    wheel_sound.play()

                    # check if extra spin button functionality must occur. This extra
                    # functionality gives the spin button the ability to start the second round.
                    if self.extraSpinFunctions:
                        # todo: use different questions
                        game.read_database_two()
                        # game.current_round += 1
                        game.spins_left = game.spin_total
                        game.board_empty = False
                        # todo: reload the whole jeopardy board
                        spinCountNum.setText(str(game.spins_left))
                        # reload board
                        updateCategoryNames()
                        board.showAllSquares()
                        myWheel.update()
                        board.round2()
                        # todo: change active player to 0 but only after current turn is done
                        self.extraSpinFunctions = False

                    # attribute = angle in degrees
                    #myWheel.spin(self.screen, 360)

                    spin_result = game.spin()
                    myWheel.set_angle(spin_result)
                    myWheel.spin(self.screen)
                    game.spins_left -= 1
                    wheelText.setText(str(spin_result))
                    spinCountNum.setText(str(game.spins_left))

                    # game logic
                    if type(spin_result) == str:
                        if spin_result == 'lose turn':

                            negative.play()
                            game.next_player()
                            print(game.current_player)

                            spin_button.setClickable(True)
                            if game.players[game.current_player].free_token > 0:
                                wait_for_player_decision()
                            else:
                                game.next_player()
                            # print(game.current_player)

                        elif spin_result == 'free turn':
                            free_token.play()
                            game.players[game.current_player].add_token()
                            narration.setText(
                                game.players[game.current_player].name + " gets a free turn token.")
                        elif spin_result == 'bankrupt':
                            negative.play()
                            if (game.players[game.current_player].score > 0):
                                game.players[game.current_player].zero_score()
                            # refresh_all_player_score()
                            # print(str(game.players[game.current_player].score))
                            game.next_player()
                        elif spin_result == 'player\'s choice':
                            q_intro.play()
                            board.showButtons(True)
                            enterCategorySelection = True
                            # pass
                        elif spin_result == "opponent's choice":
                            q_intro.play()
                            board.showButtons(True)
                            enterCategorySelection = True
                            # pass
                        elif spin_result == "spin again":
                            q_intro.play()
                            pass

                        emptyQuestionText()

                        # only run this block of code if the string result of the spin
                        # was neither opponent's choice nor player's choice
                        if enterCategorySelection == False:
                            # round 2 logic
                            if game.spins_left <= 0 or game.board_empty:
                                game.current_round += 1

                                if game.current_round > 2:
                                    # TODO: complete game and load final score board screen
                                    emptyQuestionText()
                                    questionText.addText(
                                        "Game over! Press \"SEE RESULTS\" to view game results.")
                                    spin_button.setClickable(False)
                                    game_completed_button.setClickable(True)
                                    quit_to_main_button.setClickable(False)
                                else:
                                    self.extraSpinFunctions = True
                                    emptyQuestionText()
                                    questionText.addText(
                                        "Round 1 over! Press \"SPIN\" to begin Round 2.")
                                    spin_button.setClickable(True)
                                    narration.setText(
                                        "Press \"SPIN\" to spin the wheel.")

                            else:
                                spin_button.setClickable(True)
                                narration.setText(
                                    "Press \"SPIN\" to spin the wheel.")

                        refresh_all_player_score()
                        refresh_current_player_indicator()

                    # spin result  is a category number
                    else:

                        question = game.get_category_next_question(spin_result)
                        print(question)
                        if question != None:
                            q_intro.play()
                            questionText.addText(question[0])
                            randomly_assign_answers()
                            # set the four answer buttons to clickable
                            for x in range(0, 4):
                                answerButtonArray[x].setClickable(True)
                        else:
                            # round 2 logic
                            if game.spins_left <= 0 or game.board_empty:
                                game.current_round += 1

                                if game.current_round > 2:
                                    # TODO: complete game and load final score board screen
                                    emptyQuestionText()
                                    questionText.addText(
                                        "Game over! Press \"SEE RESULTS\" to view game results.")
                                    spin_button.setClickable(False)
                                    game_completed_button.setClickable(True)
                                    quit_to_main_button.setClickable(False)
                                else:
                                    self.extraSpinFunctions = True
                                    emptyQuestionText()
                                    questionText.addText(
                                        "Round 1 over! Press \"SPIN\" to begin Round 2.")
                                    spin_button.setClickable(True)
                                    narration.setText(
                                        "Press \"SPIN\" to spin the wheel.")
                            else:
                                negative.play()
                                emptyQuestionText()
                                questionText.addText(
                                    "Category empty, Spin again!")
                                spin_button.setClickable(True)
                                narration.setText(
                                    "Press \"SPIN\" to spin the wheel.")

                        refresh_all_player_score()
                        refresh_current_player_indicator()

                    spin_button.clicked = False

            # update the game state
            pygame.display.update()
            self.clock.tick(60)