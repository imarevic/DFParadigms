import pygame
import csv
from itertools import zip_longest
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
        self.mathItem = None
        self.response = None
        self.responseTime = 0
        self.clock = pygame.time.Clock()
        self.results = {
            "subject": [self.settings.subject],
            "group": [self.settings.group],
            "balance": [self.settings.balance],
            "L1words": "",
            "L2words": "",
            "L1recall": "",
            "L2recall": "",
            "age": [],
            "gender": [],
            "major": [],
            "semester": [],
            "mothertongue": []
        }


        # ======= Initialize Screen ===== #
        self.prepare()

    def run(self):
        """Main method to run experiment."""

        # Runs the experiment loop
        while True:
            # === Welcome Part === #
            self.startWelcomeIntroBlock()

            # === Practice Block === #
            self.startPracticeIntroBlock()
            # learn L1
            self.startL1IntroBlock()
            self.startLearningInitBlock()
            self.startCountdownBlock()
            self.startStudyBlock(self.settings.practiceList1) # PracticeList 1 presentation
            self.startFORManipBlock()
            # distractor math task
            self.startMathIntroBlock()
            self.startMathInitBlock()
            self.startCountdownBlock()
            self.startMathBlock(30.0)
            self.startMathEndBlock()
            # learn L2
            self.startL2IntroBlock()
            self.startLearningInitBlock()
            self.startCountdownBlock()
            self.startStudyBlock(self.settings.practiceList2) # PracticeLlist 2 presentation
            self.startREMManipBlock()
            # distractor math task
            self.startMathIntroBlock()
            self.startMathInitBlock()
            self.startCountdownBlock()
            self.startMathBlock(30.0)
            self.startMathEndBlock()
            # recall L2
            self.startPracRecallIntroBlock()
            self.startRecallInitBlock()
            self.doFreeRecall(30.0)
            self.startRecallEndBlock()

            # ====REAL STUDY === #
            self.startPracRecallEndBlock()
            self.startIntroStudyBlock()

            # learn L1
            self.startL1IntroBlock()
            self.startLearningInitBlock()
            self.startCountdownBlock()
            self.startStudyBlock(self.settings.wordsList1) # list 1 presentation
            # F vs R Manipulation
            if self.settings.group == "FORCont" or self.settings.group == "FORReinst":
                self.startFORManipBlock()
            elif self.settings.group == "REMCont" or self.settings.group == "REMReinst":
                self.startREMManipBlock()
            # distractor math task
            self.startMathIntroBlock()
            self.startMathInitBlock()
            self.startCountdownBlock()
            self.startMathBlock(30.0)
            self.startMathEndBlock()
            # learn L2
            self.startL2IntroBlock()
            self.startLearningInitBlock()
            self.startCountdownBlock()
            self.startStudyBlock(self.settings.wordsList2) # list 2 presentation
            self.startREMManipBlock()

            # distractor math task
            self.startMathIntroBlock()
            self.startMathInitBlock()
            self.startCountdownBlock()
            self.startMathBlock(30.0)
            self.startMathEndBlock()
            # F vs R recall instructions L1
            if self.settings.group == "FORCont" or self.settings.group == "FORReinst":
                self.startinstFORRecallL1Block()
            elif self.settings.group == "REMCont" or self.settings.group == "REMReinst":
                self.startinstREMRecallL1Block()
            # initiate recall L1
            self.startRecallInitBlock()
            self.doFreeRecallL1(30.0)
            self.startRecallEndBlock()
            # F vs R recall instructions L2
            if self.settings.group == "FORCont" or self.settings.group == "FORReinst":
                self.startinstFORRecallL2Block()
            elif self.settings.group == "REMCont" or self.settings.group == "REMReinst":
                self.startinstREMRecallL2Block()
            self.startRecallInitBlock()
            self.doFreeRecallL2(30.0)
            self.startRecallEndBlock()

            # === Demographic Questions === #
            self.startDemIntroBlock()
            self.doDemQuestions()
            self.saveResultsToFile(self.settings.filename, self.results)
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
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
            # Respond to a keypress
                if event.key == pygame.K_ESCAPE:
                    quit()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    break
                elif event.key != pygame.K_RETURN or event.key != pygame.K_SPACE:
                    pass

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
        pygame.display.set_caption("IMDF Experiment") # in fullscreen mode this is redundant
        pygame.mouse.set_visible(False)
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

    def startPracticeIntroBlock(self):
        # Presentation of Welcome screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instPractice = self.textblock.textObject(self.settings.introPractice, self.settings.instFont,
                                                      self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instPractice, (self.screenRect.centerx - (self.textwidth/2),
                                             self.screenRect.centery - (self.textheigth/2)))
        pygame.display.flip()
        self.processInstEvents()

    def startL1IntroBlock(self):
        # Presentation of Welcome screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instL1 = self.textblock.textObject(self.settings.introL1, self.settings.instFont,
                                                      self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instL1, (self.screenRect.centerx - (self.textwidth/2),
                                             self.screenRect.centery - (self.textheigth/2)))
        pygame.display.flip()
        self.processInstEvents()

    def startL2IntroBlock(self):
        # Presentation of Welcome screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instL2 = self.textblock.textObject(self.settings.introL2, self.settings.instFont,
                                                      self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instL2, (self.screenRect.centerx - (self.textwidth/2),
                                             self.screenRect.centery - (self.textheigth/2)))
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

    def startREMManipBlock(self):
        # Presentation of Learning Init screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.remManip = self.textblock.textObject(self.settings.rememberManip, self.settings.instFont,
                                                      self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.remManip, (self.screenRect.centerx - (self.textwidth/2),
                                             self.screenRect.centery - (self.textheigth/2)))
        pygame.display.flip()
        self.processInstEvents()

    def startFORManipBlock(self):
        # Presentation of Learning Init screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.forManip = self.textblock.textObject(self.settings.forgetManip, self.settings.instFont,
                                                      self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.forManip, (self.screenRect.centerx - (self.textwidth/2),
                                             self.screenRect.centery - (self.textheigth/2)))
        pygame.display.flip()
        self.processInstEvents()

    def startMathIntroBlock(self):
        # Presentation of first Math Intro screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instMath = self.textblock.textObject(self.settings.introMath, self.settings.instFont,
                                                  self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instMath, (self.screenRect.centerx - (self.textwidth / 2),
                                         self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startPracRecallIntroBlock(self):
        # Presentation of first FR Intro screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instPracRecall = self.textblock.textObject(self.settings.instPracRecall, self.settings.instFont,
                                                  self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instPracRecall, (self.screenRect.centerx - (self.textwidth / 2),
                                         self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startDemIntroBlock(self):
        # Presentation of Dem. Questions Intro screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instDem = self.textblock.textObject(self.settings.introDem, self.settings.instFont,
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

    def startinstREMRecallL1Block(self):
        # Presentation of recall init screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instREML1Recall = self.textblock.textObject(self.settings.instREMRecallL1, self.settings.instFont,
                                                        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instREML1Recall, (self.screenRect.centerx - (self.textwidth / 2),
                                               self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

        # Presentation of second FR Intro screen
        self.screen.fill(self.settings.bgColor)
        self.instGenRecall = self.textblock.textObject(self.settings.instRecall, self.settings.instFont,
        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instGenRecall, (self.screenRect.centerx - (self.textwidth / 2),
        self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startinstREMRecallL2Block(self):
        # Presentation of recall init screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instREML2Recall = self.textblock.textObject(self.settings.instREMRecallL2, self.settings.instFont,
                                                        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instREML2Recall, (self.screenRect.centerx - (self.textwidth / 2),
                                               self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

        # Presentation of second FR Intro screen
        self.screen.fill(self.settings.bgColor)
        self.instGenRecall = self.textblock.textObject(self.settings.instRecall, self.settings.instFont,
        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instGenRecall, (self.screenRect.centerx - (self.textwidth / 2),
        self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startinstFORRecallL1Block(self):
        # Presentation of recall init screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instFORL1Recall = self.textblock.textObject(self.settings.instFORRecallL1, self.settings.instFont,
                                                        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instFORL1Recall, (self.screenRect.centerx - (self.textwidth / 2),
                                               self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

        # Presentation of second FR Intro screen
        self.screen.fill(self.settings.bgColor)
        self.instGenRecall = self.textblock.textObject(self.settings.instRecall, self.settings.instFont,
        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instGenRecall, (self.screenRect.centerx - (self.textwidth / 2),
        self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startinstFORRecallL2Block(self):
        # Presentation of recall init screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instFORL2Recall = self.textblock.textObject(self.settings.instFORRecallL2, self.settings.instFont,
                                                        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instFORL2Recall, (self.screenRect.centerx - (self.textwidth / 2),
                                               self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

        # Presentation of second FR Intro screen
        self.screen.fill(self.settings.bgColor)
        self.instGenRecall = self.textblock.textObject(self.settings.instRecall, self.settings.instFont,
        self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instGenRecall, (self.screenRect.centerx - (self.textwidth / 2),
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

        self.screen.blit(self.instEndMath, (self.screenRect.centerx - (self.textwidth / 2),
                                            self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startPracRecallEndBlock(self):
         # Presentation of exp. end screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instExpEnd = self.textblock.textObject(self.settings.instEndPractice, self.settings.instFont,
                                                     self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instExpEnd, (self.screenRect.centerx - (self.textwidth / 2),
                                                 self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startIntroStudyBlock(self):
         # Presentation of exp. end screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth

        self.instStudyIntro = self.textblock.textObject(self.settings.introStudy, self.settings.instFont,
                                                     self.settings.instWidth, self.settings.instHeigth)
        self.screen.blit(self.instStudyIntro, (self.screenRect.centerx - (self.textwidth / 2),
                                                 self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

    def startRecallEndBlock(self):
        # Presentation of End FR screen
        self.screen.fill(self.settings.bgColor)
        self.textwidth = self.settings.instWidth
        self.textheigth = self.settings.instHeigth
        self.instRecallEnd = self.textblock.textObject(self.settings.RecallEnd, self.settings.instFont,
                                                     self.settings.instWidth, self.settings.instHeigth)

        self.screen.blit(self.instRecallEnd, (self.screenRect.centerx - (self.textwidth / 2),
                                            self.screenRect.centery - (self.textheigth / 2)))
        pygame.display.flip()
        self.processInstEvents()

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

    def startStudyBlock(self, wordlist):
        """Starts presentation of stimuli"""

        stimlist = []

        for trialIdx in range(len(wordlist)):

            # Prepare stimuli
            self.renderStimuli(wordlist, trialIdx)

            # Draw visual objects
            self.drawStimulus(5.0)
            self.drawISI(1.0)

            # Save results
            stimlist.append(wordlist[trialIdx])

        # append stimlist to results dict
        if wordlist == self.settings.wordsList1:
            self.results['L1words'] = stimlist
        elif wordlist == self.settings.wordsList2:
            self.results['L2words'] = stimlist

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

    def renderStimuli(self, word, trial):
        """Creates the study word to be displayed on the screen"""

        # Render items
        # parameters are the string, anti-aliasing, color of text, color of background
        self.studyItem = self.settings.font.render(word[trial],
                                                   True, self.settings.black, self.settings.bgColor)

        # Get the rectangle of the word
        self.studyItemRect = self.studyItem.get_rect()
        # Place at the center of the screen
        self.studyItemRect.center = self.screenRect.center

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

            for n, text_surf in enumerate(self.userInputs):
                # 12 rows, offset 50 pixels.
                ypos = self.screenRect.height/3 + (n % 12) * 50
                # After these 12 rows add a new column with up to 3 columns.
                xpos = 50 + n // 12 * self.screenRect.width/3
                # blit every input to screen
                self.screen.blit(text_surf, (xpos, ypos))

            # Update screen
            pygame.display.update()
            clock.tick(30)

    def doFreeRecallL1(self, duration):
        """Samples user input for Free Recall Task and blits it to the screen."""

        # Get time stamps
        startTime = pygame.time.get_ticks() / 1000
        clock = pygame.time.Clock()

        # Initialize list to store user input
        self.userInputs = []
        recalledItemsL1 = []

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
                # append user input to list of strings (for results saving)
                recalledItemsL1.append(self.textinput.get_text())
                self.textinput = TextInput("arial", 40)

                # Fill screen
            self.screen.fill((self.settings.bgColor))
            # Blit surface onto the screen
            self.screen.blit(self.textinput.get_surface(), (self.screenRect.centerx,
                                                            self.screenRect.height / 5))

            for n, text_surf in enumerate(self.userInputs):
                # 12 rows, offset 50 pixels.
                ypos = self.screenRect.height/3 + (n % 12) * 50
                # After these 12 rows add a new column with up to 3 columns.
                xpos = 50 + n // 12 * self.screenRect.width/3
                # blit every input to screen
                self.screen.blit(text_surf, (xpos, ypos))

            # Update screen
            pygame.display.update()
            clock.tick(30)

        # Append user inputs to results file
        self.results['L1recall'] = recalledItemsL1

    def doFreeRecallL2(self, duration):
        """Samples user input for Free Recall Task and blits it to the screen."""

        # Get time stamps
        startTime = pygame.time.get_ticks() / 1000
        clock = pygame.time.Clock()

        # Initialize list to store user input
        self.userInputs = []
        recalledItemsL2 = []

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
                # append user input to list of strings (for results saving)
                recalledItemsL2.append(self.textinput.get_text())
                self.textinput = TextInput("arial", 40)

                # Fill screen
            self.screen.fill((self.settings.bgColor))
            # Blit surface onto the screen
            self.screen.blit(self.textinput.get_surface(), (self.screenRect.centerx,
                                                            self.screenRect.height / 5))

            for n, text_surf in enumerate(self.userInputs):
                # 12 rows, offset 50 pixels.
                ypos = self.screenRect.height/3 + (n % 12) * 50
                # After these 12 rows add a new column with up to 3 columns.
                xpos = 50 + n // 12 * self.screenRect.width/3
                # blit every input to screen
                self.screen.blit(text_surf, (xpos, ypos))

            # Update screen
            pygame.display.update()
            clock.tick(30)

        # Append user inputs to results file
        self.results['L2recall'] = recalledItemsL2

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
        self.results['age'].append(self.finalItems[0])
        self.results['gender'].append(self.finalItems[1])
        self.results['major'].append(self.finalItems[2])
        self.results['semester'].append(self.finalItems[3])
        self.results['mothertongue'].append(self.finalItems[4])

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

        xoffset = self.screenRect.width/4
        yoffset = self.screenRect.height/4
        rectLeft = self.settings.leftText.get_rect()
        rectLeft = rectLeft.move(0 + xoffset, self.screenRect.height - yoffset)

        rectRight = self.settings.rightText.get_rect()
        rectRight = rectRight.move(self.screenRect.width - rectRight.width - xoffset,
                                   self.screenRect.height - yoffset)

        return rectLeft, rectRight

    def saveResultsToFile(self, filename, dict):
        """Saves all exp. results to a csv file."""
        resultsdict = dict


        with open(filename, 'w') as f:
            w = csv.writer(f, delimiter=',', lineterminator='\n')
            w.writerow(resultsdict.keys())
            w.writerows(zip_longest(*resultsdict.values()))
