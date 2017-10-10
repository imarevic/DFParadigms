import pygame
import csv
from settings import Settings
from instBlitter import Textblock
from textInput import TextInput

class Experiment:
    """Main experiment class."""

    fixationWidth = 5
    fixationLength = 40

    def __init__(self):

        # ======= Main Attributes ====== #
        self.settings = Settings()
        self.textblock = Textblock()
        self.textinput = None
        self.screen = None
        self.screenRect = None
        self.studyItem = None
        self.cueItem = None
        self.question = None
        self.userInput = None
        self.countdown = None
        self.memCue = None
        self.mathItem = None
        self.response = None
        self.responseTime = 0
        self.clock = pygame.time.Clock()
        self.results = []

        # ======= Initialize Screen ===== #
        self.prepare()

    def run(self):
        """Main method to run experiment."""

        # Runs the experiment loop
        while True:

            #self.startWelcomeIntroBlock()
            #self.startLearningInitBlock()
            #self.startCountdownBlock()
            #self.startStudyBlock()
            #self.startMathIntroBlock()
            #self.startMathInitBlock()
            #self.startCountdownBlock()
            #self.startMathBlock(30.0)
            #self.startMathEndBlock()
            #self.startFreeRecallIntroBlock()
            #self.startRecallInitBlock()
            #self.doFreeRecall(10.0)
            #self.startFreeRecallEndBlock()
            #self.startCuedRecallIntroBlock()
            #self.startRecallInitBlock()
            #self.doCuedRecall()
            #self.startCuedRecallEndBlock()
            #self.startDemIntroBlock()
            #self.doDemQuestions()
            #self.saveResultsToFile(self.settings.filename, self.results)
            self.startExpEndBlock()
            quit()

    def processMathEvents(self):
        """Sample user input for math task."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:

            # Respond to a keypress
                if event.key == pygame.K_ESCAPE:
                    quit()
                elif event.key == pygame.K_f:
                    self.response = 1
                elif event.key == pygame.K_j:
                    self.response = 2

    def processInstEvents(self):
        """Sample user input for instructions."""

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
            # Respond to a keypress
                if event.key == pygame.K_ESCAPE:
                    quit()
                elif event.key == pygame.K_RETURN or pygame.K_SPACE:
                    break

    def processQuitExpEvent(self):
        """Sample user input for quitting at study end."""

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
            # Respond to a keypress
                if event.key == pygame.K_q:
                    quit()


    def prepare(self):
        """Initialize pygame with some default settings."""

        self.screen = pygame.display.set_mode((self.settings.screenWidth,
                                 self.settings.screenHeight), pygame.FULLSCREEN)
        pygame.display.set_caption("IMDF Experiment")
        self.clock.tick(self.settings.FPS) # Add Frame rate
        # Get rect of the screen
        self.screenRect = self.screen.get_rect()
        # Create a fixation point
        self.createFixation()

# ================================================================================================ #
# === Section of methods that blit all instructions of the Experiment === #
    def startWelcomeIntroBlock(self):
        # Presentation of Welcome screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instWelcome = self.textblock.textObject(self.settings.welcomeText, self.settings.instFont,
                                                      self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instWelcome, (self.screenRect.centerx - (self.textwidth/2),
                                             self.screenRect.centery - (self.textheigth/2)))
        pygame.display.flip()
        self.processInstEvents()

        # Presentation of first Instruction screen
        self.screen.fill(self.settings.bgColor)
        self.instIntro1 = self.textblock.textObject(self.settings.intro1Text, self.settings.instFont,
                                                     self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instIntro1, (self.screenRect.centerx - (self.textwidth / 2),
                                            self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

        # Presentation of second Instruction screen
        self.screen.fill(self.settings.bgColor)
        self.instIntro2 = self.textblock.textObject(self.settings.intro2Text, self.settings.instFont,
                                                    self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instIntro2, (self.screenRect.centerx - (self.textwidth / 2),
                                           self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startLearningInitBlock(self):
        # Presentation of Learning Init screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.initLearning = self.textblock.textObject(self.settings.learningInitText, self.settings.instFont,
                                                      self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.initLearning, (self.screenRect.centerx - (self.textwidth/2),
                                             self.screenRect.centery - (self.textheigth/2)))
        pygame.display.flip()
        self.processInstEvents()

    def startMathIntroBlock(self):
        # Presentation of first Math Intro screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instMath = self.textblock.textObject(self.settings.mathText, self.settings.instFont,
                                                  self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instMath, (self.screenRect.centerx - (self.textwidth / 2),
                                         self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startFreeRecallIntroBlock(self):
        # Presentation of first FR Intro screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instFreeRecall1 = self.textblock.textObject(self.settings.FRText1, self.settings.instFont,
                                                  self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instFreeRecall1, (self.screenRect.centerx - (self.textwidth / 2),
                                         self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

        # Presentation of second FR Intro screen
        self.screen.fill(self.settings.bgColor)
        self.instFreeRecall2 = self.textblock.textObject(self.settings.FRText2, self.settings.instFont,
                                                  self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instFreeRecall2, (self.screenRect.centerx - (self.textwidth / 2),
                                         self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startCuedRecallIntroBlock(self):
        # Presentation of first Math Intro screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instCuedRecall1 = self.textblock.textObject(self.settings.CRText1, self.settings.instFont,
                                                         self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instCuedRecall1, (self.screenRect.centerx - (self.textwidth / 2),
                                                self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

        # Presentation of second FR Intro screen
        self.screen.fill(self.settings.bgColor)
        self.instCuedRecall2 = self.textblock.textObject(self.settings.CRText2, self.settings.instFont,
                                                         self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instCuedRecall2, (self.screenRect.centerx - (self.textwidth / 2),
                                                self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()


    def startDemIntroBlock(self):
        # Presentation of Dem. Questions Intro screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instDem = self.textblock.textObject(self.settings.demText, self.settings.instFont,
                                                  self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instDem, (self.screenRect.centerx - (self.textwidth / 2),
                                         self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()


    def startRecallInitBlock(self):
        # Presentation of recall init screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instRecallInit = self.textblock.textObject(self.settings.recallInitText, self.settings.instFont,
                                                        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instRecallInit, (self.screenRect.centerx - (self.textwidth / 2),
                                               self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startMathInitBlock(self):
        # Presentation of recall init screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instMathInit = self.textblock.textObject(self.settings.mathInitText, self.settings.instFont,
                                                        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instMathInit, (self.screenRect.centerx - (self.textwidth / 2),
                                               self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startMathEndBlock(self):
        # Presentation of End Math screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instEndMath = self.textblock.textObject(self.settings.mathEnd, self.settings.instFont,
                                                     self.settings.instWidth, self.settings.instHeigth)
        # set sceen timout to 1 second
        timeout = 1
        startTime = pygame.time.get_ticks() / 1000
        while pygame.time.get_ticks() / 1000 - startTime < timeout:
            self.screen.blit(self.instEndMath, (self.screenRect.centerx - (self.textwidth / 2),
                                                self.screenRect.centery - (self.textheigth / 2)))
            pygame.display.flip()

    def startFreeRecallEndBlock(self):
        # Presentation of End FR screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instEndFR = self.textblock.textObject(self.settings.FREnd, self.settings.instFont,
                                                     self.settings.instWidth, self.settings.instHeigth)
        # set sceen timout to 1 second
        timeout = 1
        startTime = pygame.time.get_ticks() / 1000
        while pygame.time.get_ticks() / 1000 - startTime < timeout:
            self.screen.blit(self.instEndFR, (self.screenRect.centerx - (self.textwidth / 2),
                                                self.screenRect.centery - (self.textheigth / 2)))
            pygame.display.flip()

    def startCuedRecallEndBlock(self):
        # Presentation of End CR screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instEndCR = self.textblock.textObject(self.settings.CREnd, self.settings.instFont,
                                                     self.settings.instWidth, self.settings.instHeigth)
        # set sceen timout to 1 second
        timeout = 1
        startTime = pygame.time.get_ticks() / 1000
        while pygame.time.get_ticks() / 1000 - startTime < timeout:
            self.screen.blit(self.instEndCR, (self.screenRect.centerx - (self.textwidth / 2),
                                                self.screenRect.centery - (self.textheigth / 2)))
            pygame.display.flip()

    def startExpEndBlock(self):
         # Presentation of exp. end screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instExpEnd = self.textblock.textObject(self.settings.ExpEndText, self.settings.instFont,
                                                     self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instExpEnd, (self.screenRect.centerx - (self.textwidth / 2),
                                                 self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processQuitExpEvent()

# =================================================================================================== #

    def startCountdownBlock(self):
        """Starts presentation of countdown"""

        for trialIdx in range(len(self.settings.countdownList)):

            # Prepare text to be drawn
            self.renderCountdown(trialIdx)

            # Draw visual objects
            self.drawCountdown(1)

    def startStudyBlock(self):
        """Starts presentation of stimuli"""

        for trialIdx in range(len(self.settings.wordsList)):

            # Prepare stimuli
            self.renderStimuli(trialIdx)

            # Draw visual objects
            self.drawStimulus(5.0)
            self.drawMemCue(2.0)
            self.drawISI(1.0)

            # Save results
            # TODO - save results to a file


    def startMathBlock(self, duration):
        """Starts presentation of math trials"""

        # Get timestamp
        startTime = pygame.time.get_ticks() / 1000
        while pygame.time.get_ticks() / 1000 - startTime < duration:
            for trialIdx in range(len(self.settings.mathList)):
                # Prepare math items
                self.renderMathItems(trialIdx)
                # Draw visual objects
                self.drawFixation(1.0)
                self.drawMathtask()
                if pygame.time.get_ticks() / 1000 - startTime > duration:
                    break
            else:
                continue
            break


                # Save results
                # TODO - save results to a file

    def renderCountdown(self, trial):
        """Creates the countdown to be displayed on the screen."""
        # Render countdown
        # parameters are the string, anti-aliasing, color of text, color of background
        self.countdown = self.settings.font.render(self.settings.countdownList[trial],
                                                   True, self.settings.black, self.settings.bgColor)

        # Place countdown at center
        self.CountdownRect = self.countdown.get_rect()

        # Place countdown at center of screen
        self.CountdownRect.center = self.screenRect.center

    def renderStimuli(self, trial):
        """Creates the study word to be displayed on the screen"""

        # Render item and memory cue
        # parameters are the string, anti-aliasing, color of text, color of background
        self.studyItem = self.settings.font.render(self.settings.wordsList[trial],
                                                   True, self.settings.black, self.settings.bgColor)

        self.memCue = self.settings.font.render(self.settings.memCueList[trial],
                                                True, self.settings.black, self.settings.bgColor)
        # Get the rectangle of the word and memory cue (for positioning)
        self.studyItemRect = self.studyItem.get_rect()
        self.memCueRect = self.memCue.get_rect()
        # Place both at the center of the screen
        self.studyItemRect.center = self.screenRect.center
        self.memCueRect.center = self.screenRect.center

    def renderMathItems(self, trial):
        """Renders the math equations that are displayed on the screen"""
        # Render math equation
        # parameters are the string, anti-aliasing, color of text, color of background
        self.mathItem = self.settings.font.render(self.settings.mathList[trial],
                                                  True, self.settings.black, self.settings.bgColor)
        # Get the rectangle of the math item
        self.mathItemRect = self.mathItem.get_rect()

        # Place math item at the center of the screen
        self.mathItemRect.center = self.screenRect.center

    def renderCues(self, trial):
        """Renders the Cue to be displayed on the screen during Cued Recall"""

        # Render cues
        # parameters are the string, anti-aliasing, color of text, color of background
        self.cueItem = self.settings.font.render(self.settings.cuesList[trial],
                                                   True, self.settings.black, self.settings.bgColor)

        # Get the rectangle of the cue (for positioning)
        self.cueItemRect = self.cueItem.get_rect()
        # Place at the center of the screen
        self.cueItemRect = self.cueItemRect.move(self.screenRect.width/2 - self.cueItemRect.width,
                                                 self.screenRect.centery)

    def renderQuestions(self, trial):
        """Renders the question to be displayed on the screen during the demog. quesionnaire"""

        # Render cues
        # parameters are the string, anti-aliasing, color of text, color of background
        self.question = self.settings.font.render(self.settings.questionList[trial],
                                                 True, self.settings.black, self.settings.bgColor)

        # Get the rectangle of the cue (for positioning)
        self.questionRect = self.question.get_rect()
        # Place at the center of the screen
        self.questionRect = self.questionRect.move(self.screenRect.width/2 - self.questionRect.width/2,
                                                   self.screenRect.height/2 - self.questionRect.height*2)

    def drawCountdown(self, duration):
        """Draws a countdown from 3 downwards."""

        # Get time stamp
        startTime = pygame.time.get_ticks() / 1000

        # Fill background
        self.screen.fill(self.settings.bgColor)

        # Get positions of header and footer
        headerPos, footerPos = self.getCountdownTextsPosition()

        # while loop for drawing countdown to screen
        while (pygame.time.get_ticks() / 1000) - startTime < duration:
            # Draw to background...
            self.screen.blit(self.settings.countHeader, headerPos)
            self.screen.blit(self.countdown, self.CountdownRect)
            self.screen.blit(self.settings.countFooter, footerPos)
            # Draw to foreground...
            pygame.display.flip()

    def drawStimulus(self, duration):
        """Draws a stimulus word for a given duration of time."""

        # Get time stamp
        startTime = pygame.time.get_ticks() / 1000

        # Fill background
        self.screen.fill(self.settings.bgColor)

        # while loop for drawing stimulus to screen for "duration" of time
        while (pygame.time.get_ticks() / 1000) - startTime < duration:
            # Draw to background...
            self.screen.blit(self.studyItem, self.studyItemRect)
            # Draw to foreground...
            pygame.display.flip()

    def drawMemCue(self, duration):
        """ Draws a memory cue for a given duration of time."""

        # Get time stamp
        startTime = pygame.time.get_ticks() / 1000

        # Fill background
        self.screen.fill(self.settings.bgColor)

        # while loop for drawing stimulus to screen for "duration" of time
        while (pygame.time.get_ticks() / 1000) - startTime < duration:
            # Draw to background...
            self.screen.blit(self.memCue, self.memCueRect)
            # Draw to foreground...
            pygame.display.flip()

    def drawISI(self, duration):
        """Draws a blank screen for a given duration of time."""
        # Get time stamp
        startTime = pygame.time.get_ticks() / 1000

        # Fill background
        self.screen.fill(self.settings.bgColor)

        # While loop for drawing blank ISI screen for "duration" of time.
        while (pygame.time.get_ticks() / 1000) - startTime < duration:
            pygame.display.flip()

    def drawFixation(self, duration):
        """Draws a fixation for a given duration."""

        # Get a time stamp
        startTime = pygame.time.get_ticks() / 1000

        # Fill screen with background color
        self.screen.fill(self.settings.bgColor)

        # Get positions of left and right text
        leftTextPos, rightTextPos = self.getHelperTextsPosition()

        # Loop until duration elapsed
        while pygame.time.get_ticks() / 1000 - startTime < duration:
            # Draw line in background
            pygame.draw.lines(self.screen, self.settings.black,
                              False, self.pointsHor, self.fixationWidth)
            pygame.draw.lines(self.screen, self.settings.black,
                              False, self.pointsVer, self.fixationWidth)

            # Draw left and right helper texts
            self.screen.blit(self.settings.leftText, leftTextPos)
            self.screen.blit(self.settings.rightText, rightTextPos)

            # Draw everything from back buffer to foreground
            pygame.display.flip()

    def drawMathtask(self):
        """Draws math equations to verify by user."""

        self.response = 0

        # Fill screen with background color
        self.screen.fill(self.settings.bgColor)

        # Get positions of left and right text
        leftTextPos, rightTextPos = self.getHelperTextsPosition()

        # Loop until participant responds
        while self.response != 1 and self.response != 2:
            # Process events in event queue
            self.processMathEvents()

            # Draw math trial and left and right helper texts
            self.screen.blit(self.mathItem, self.mathItemRect)
            self.screen.blit(self.settings.leftText, leftTextPos)
            self.screen.blit(self.settings.rightText, rightTextPos)

            # Flip to foreground
            pygame.display.flip()


    def doFreeRecall(self, duration):
        """Samples user input for Free Recall Task and blits it to the screen."""

        # Get time stamps
        startTime = pygame.time.get_ticks() / 1000
        clock = pygame.time.Clock()

        # Initialize list to store user input
        self.userInputs = []

        # Fill surface background at the beginning
        self.screen.fill(self.settings.bgColor)
        self.textinput = TextInput("arial", 40)

        # while loop for free recall for "duration" of time
        while (pygame.time.get_ticks() / 1000) - startTime < duration:

            # create event instance to handle exit
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            # Feed with events every frame
            if self.textinput.update(events):
                self.userInputs.append(self.settings.createText(self.textinput.get_text(), self.settings.black))
                self.textinput = TextInput("arial", 40)

                # Fill screen
            self.screen.fill((self.settings.bgColor))
            # Blit surface onto the screen
            self.screen.blit(self.textinput.get_surface(), (self.screenRect.centerx,
                                                            self.screenRect.height / 5))

            for y, text_surf in enumerate(self.userInputs):
                self.screen.blit(text_surf, (10, (self.screenRect.height / 4) + 30 * y))

            # Update screen
            pygame.display.update()
            clock.tick(30)

    def doCuedRecall(self):
        """Samples user input for Cued Recall Task and blits it to the screen."""

        # Get time stamps
        clock = pygame.time.Clock()

        # Initialize list to store user input
        self.userInputs = []
        self.responses = []
        self.cues = []

        # Fill surface background at the beginning
        self.screen.fill(self.settings.bgColor)
        self.textinput = TextInput("arial", 40)

        for trialIdx in range(len(self.settings.cuesList)):

            while True:
                 # create event instance to handle exit
                 events = pygame.event.get()
                 for event in events:
                    if event.type == pygame.QUIT:
                        exit()
                 # Feed with events every frame
                 if self.textinput.update(events):
                     self.userInputs.append(self.settings.createText(self.textinput.get_text(), self.settings.black))
                     # append user input to list of strings (for results saving)
                     self.cues.append(self.settings.cuesList[trialIdx])
                     self.responses.append(self.textinput.get_text())

                     self.textinput = TextInput("arial", 40)
                     break

                 # Fill screen
                 self.screen.fill((self.settings.bgColor))
                 # Blit surface onto the screen
                 self.screen.blit(self.textinput.get_surface(), (self.screenRect.centerx,
                                                                 self.screenRect.centery))
                 # Prepare stimuli and blit to screen
                 self.renderCues(trialIdx)
                 self.screen.blit(self.cueItem, self.cueItemRect)

                 # Update screen
                 pygame.display.update()
                 clock.tick(30)

        # Append user inputs to results file
        self.results.append(self.cues)
        self.results.append(self.responses)

    def doDemQuestions(self):
        """Samples user input for demographic questions and blits them to the screen."""

        # Get time stamps
        clock = pygame.time.Clock()

        # Initialize list to store user input
        self.userInputs = []
        self.finalItems = []

        # Fill surface background at the beginning
        self.screen.fill(self.settings.bgColor)
        self.textinput = TextInput("arial", 40)

        for trialIdx in range(len(self.settings.questionList)):

            while True:
                # create event instance to handle exit
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        exit()
                # Feed with events every frame
                if self.textinput.update(events):
                    # append user input to text surface
                    self.userInputs.append(self.settings.createText(self.textinput.get_text(), self.settings.black))
                    # append user input to list of strings (for results saving)
                    self.finalItems.append(self.textinput.get_text())
                    #  Reinitialize textinput object
                    self.textinput = TextInput("arial", 40)

                    break
                # Fill screen
                self.screen.fill((self.settings.bgColor))
                # Blit surface onto the screen
                self.screen.blit(self.textinput.get_surface(), (self.screenRect.centerx,
                                                                self.screenRect.centery))
                # Prepare stimuli and blit to screen
                self.renderQuestions(trialIdx)
                self.screen.blit(self.question, self.questionRect)

                # Update screen
                pygame.display.update()
                clock.tick(30)

        # Append user inputs to results file
        self.results.append(self.finalItems)

    def createFixation(self):
        """Creates a fixation point."""

        # Parameters are two tuples - (x1, y1) - (x2, y2)
        self.pointsVer = [(self.screenRect.centerx - self.fixationLength*0.5,
                           self.screenRect.centery),
                          (self.screenRect.centerx + self.fixationLength*0.5,
                           self.screenRect.centery)]

        self.pointsHor = [(self.screenRect.centerx,
                           self.screenRect.centery + self.fixationLength*0.5),
                           (self.screenRect.centerx,
                            self.screenRect.centery - self.fixationLength*0.5)]

    def getCountdownTextsPosition(self):
        """Returns the countdown header and footer positions."""

        offsetUp = 80
        offsetDown = 40
        rectHeader = self.settings.countHeader.get_rect()
        rectHeader = rectHeader.move(self.screenRect.width/2 - rectHeader.width/2,
                                     self.screenRect.height/2 - offsetUp)

        rectFooter = self.settings.countFooter.get_rect()
        rectFooter = rectFooter.move(self.screenRect.width/2 - rectFooter.width/2,
                                     self.screenRect.height/2 + offsetDown)

        return rectHeader, rectFooter

    def getHelperTextsPosition(self):
        """
        Returns the positions of the left and right helper texts:
        Left bottom and right bottom corners, returned as rects.
        """

        offset = 5
        rectLeft = self.settings.leftText.get_rect()
        rectLeft = rectLeft.move(0 + offset, self.screenRect.height - rectLeft.height)

        rectRight = self.settings.rightText.get_rect()
        rectRight = rectRight.move(self.screenRect.width - rectRight.width - offset,
                                   self.screenRect.height - rectRight.height)

        return rectLeft, rectRight


# TODO: Finish this results saver method
    def saveResultsToFile(self, filename, list):

        readlist = list
        finalList = zip(*readlist)

        with open(filename, "w") as file:
            writer = csv.writer(file)
            writer.writerow(['var1', 'var2', 'var3', 'var4'])
            writer.writerows(finalList)


