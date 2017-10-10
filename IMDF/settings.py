import pygame
import random
import csv
from os import listdir, path, sep


class Settings:
    """A class to store all the settings for the experiment."""

    def __init__(self):

        self.filename = self.createFile()
        self.initializePygame()

        # ========== Some Graphics Parameters =========== #
        self.screenWidth = 1920
        self.screenHeight = 1080
        self.instWidth = self.screenWidth - (self.screenWidth / 6)
        self.instHeigth = self.screenHeight - (self.screenHeight / 6)
        self.bgColor = (255, 255, 255)
        self.black = (0, 0, 0)
        self.FPS = 60
        # ========== Experiment Parameters =========== #
        self.numStudyTrials = 30
        self.countdownList = ['3', '2', '1']
        self.wordsList = self.getWordsList()
        self.mathList = self.getMathList()
        self.cuesList = self.getCuesList()
        self.questionList = self.getQuestionList()
        self.possibleMemCues = ['**FFF**', '**RRR**']
        self.memCueList = self.getMemCueList()
        self.instructionsPath = path.dirname(__file__) + sep + "instructions" + sep

        # ========== Text Parameters =========== #
        self.font = pygame.font.SysFont("arial", 42)
        self.instFont = pygame.font.SysFont("arial", 33)
        self.countHeader = self.createText("The task starts in:", self.black)
        self.countFooter = self.createText("seconds", self.black)
        self.leftText = self.createText("[F] FALSE", self.black)
        self.rightText = self.createText("TRUE [J]", self.black)

        # ========== Instructions =============== #
        self.welcomeText = self.loadInstructions('Welcome.txt')
        self.intro1Text = self.loadInstructions('Instructions1.txt')
        self.intro2Text = self.loadInstructions('Instructions2.txt')
        self.learningInitText = self.loadInstructions('InitLearning.txt')
        self.mathInitText = self.loadInstructions('InitMath.txt')
        self.recallInitText = self.loadInstructions('InitRecall.txt')
        self.mathText = self.loadInstructions('MathInst.txt')
        self.mathEnd = self.loadInstructions('MathEnd.txt')
        self.FRText1 = self.loadInstructions('RecallInst1.txt')
        self.FRText2 = self.loadInstructions('RecallInst2.txt')
        self.CRText1 = self.loadInstructions('CuedRecallInst1.txt')
        self.CRText2 = self.loadInstructions('CuedRecallInst2.txt')
        self.demText = self.loadInstructions('DemQuestions.txt')
        self.FREnd = self.loadInstructions('RecallEnd.txt')
        self.CREnd = self.loadInstructions('CuedRecallEnd.txt')
        self.ExpEndText = self.loadInstructions('EndExperiment.txt')

    def createFile(self):
        """
        Creates a results file with part.number, and exp.name
        as the file name.
        """
        partnumber = input('Enter participant number: ')
        name = partnumber + '_IMDFExp' + '.' + 'csv'

        file = open(name, 'a')
        file.close()

        return name

    def initializePygame(self):
        """
        Intitializes pygame backends explicitly.
        """

        pygame.init()

    def createText(self, text, color):
        """Returns a pygame font instance."""

        return self.font.render(text, True, color, self.bgColor)

    def getWordsList(self):
        """
        Reads word-pairs from a csv file and returns a randomly shuffled list
        that will serve as the study list.
        """

        # Opens the word list and saves it in "items" variable
        with open('itemlist.csv', newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            items = []
            for row in reader:
                item = row[0] + ' - ' + row[1]
                items.append(item)
            random.shuffle(items)
        return items

    def getMemCueList(self):
        """
        Creates a memory cue list consisting of TBF and TBR cues.
        The length of the list matches the number of study trials.
        """
        # read memcue list
        memcues = [cue for cue in self.possibleMemCues] * int((self.numStudyTrials / len(self.possibleMemCues)))
        # Shuffle
        random.shuffle(memcues)
        return memcues

    def getMathList(self):
        """
        Creates a math task list consiting of math tasks.
        Length of list: 50 math tasks
        """

        with open('mathlist.csv', newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            mathitems = []
            for row in reader:
                mathitem = row[0]
                mathitems.append(mathitem)
        return mathitems

    def getCuesList(self):
        """
        Reads the first word of the pairs from a csv file and returns a randomly shuffled list
        that will serve as the cues during cued recall.
        """

        # Opens the cue list and saves it in "cues" variable
        with open('itemlist.csv', newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            cues = []
            for row in reader:
                cue = row[0] + " - "
                cues.append(cue)
            random.shuffle(cues)
        return cues

    def getQuestionList(self):
        """
        Reads demographic questions from a csv file and returns them.
        These will serve as demographic questions at the end of the experiment.
        """

        # Opens the question list and saves it in "questions" variable
        with open('demquestions.csv', newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar = '|')
            questions = []
            for row in reader:
                question = row[0]
                questions.append(question)
        return questions

    def loadInstructions(self, filename):
        with open(self.instructionsPath + filename, 'r') as file:
            infile = file.read()
        return infile
