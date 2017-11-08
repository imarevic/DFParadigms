import pygame
from tkinter import *
import random
import csv
from os import listdir, path, sep


class Settings:
    """A class to store all the settings for the experiment."""

    def __init__(self):

        self.filename, self.subject, self.group, self.balance  = self.startupInfo()
        self.initializePygame()

        # ========== Some Graphics Parameters =========== #
        self.screenInfoObject = pygame.display.Info()
        self.screenWidth = self.screenInfoObject.current_w
        self.screenHeight = self.screenInfoObject.current_h
        self.instWidth = self.screenWidth - (self.screenWidth / 6)
        self.instHeigth = self.screenHeight - (self.screenHeight / 6)
        self.bgColor = (255, 255, 255)
        self.black = (0, 0, 0)
        self.FPS = 60
        # ========== Experiment Parameters =========== #
        self.numStudyTrials = 30
        self.countdownList = ['3', '2', '1']
        self.practiceList1 = self.getWordsList("practicelist1.csv")
        self.practiceList2 = self.getWordsList("practicelist2.csv")
        self.wordsListA = self.getWordsList("wordlist1.csv")
        self.wordsListB = self.getWordsList("wordlist2.csv")
        self.wordsList1, self.wordsList2 = self.counterbalanceWordList(self.wordsListA, self.wordsListB)
        self.mathList = self.getMathList()
        self.questionList = self.getQuestionList()
        self.instructionsPath = path.dirname(__file__) + sep + "instructions" + sep

        # ========== Text Parameters =========== #
        self.font = pygame.font.SysFont("arial", 42)
        self.instFont = pygame.font.SysFont("arial", 36)
        self.countHeader = self.createText("Die Aufgabe beginnt in:", self.black)
        self.countFooter = self.createText("Sekunden", self.black)
        self.leftText = self.createText("[F] FALSCH", self.black)
        self.rightText = self.createText("RICHTIG [J]", self.black)

        # ========== Instructions =============== #
        self.welcomeText = self.loadInstructions('Welcome.txt')
        self.intro1Text = self.loadInstructions('Instructions1.txt')
        self.intro2Text = self.loadInstructions('Instructions2.txt')
        self.introPractice = self.loadInstructions('PracticeIntro.txt')
        self.introL1 = self.loadInstructions('IntroL1.txt')
        self.introL2 = self.loadInstructions('IntroL2.txt')
        self.learningInitText = self.loadInstructions('InitLearning.txt')
        self.rememberManip = self.loadInstructions('RememberManipulation.txt')
        self.forgetManip = self.loadInstructions('ForgetManipulation.txt')
        self.mathInitText = self.loadInstructions('InitMath.txt')
        self.recallInitText = self.loadInstructions('InitRecall.txt')
        self.introMath = self.loadInstructions('MathInst.txt')
        self.mathEnd = self.loadInstructions('MathEnd.txt')
        self.instPracRecall = self.loadInstructions('PracRecallInst.txt')
        self.instRecall = self.loadInstructions('RecallInst2.txt')
        self.instEndPractice = self.loadInstructions('EndPractice.txt')
        self.introStudy = self.loadInstructions('StudyIntro.txt')
        self.instREMRecallL1 = self.loadInstructions('RememberRecallInstL1.txt')
        self.instREMRecallL2 = self.loadInstructions('RememberRecallInstL2.txt')
        self.instFORRecallL1 = self.loadInstructions('ForgetRecallInstL1.txt')
        self.instFORRecallL2 = self.loadInstructions('ForgetRecallInstL2.txt')
        self.introDem = self.loadInstructions('DemQuestions.txt')
        self.RecallEnd = self.loadInstructions('RecallEnd.txt')
        self.ExpEndText = self.loadInstructions('EndExperiment.txt')

    def startupInfo(self):
        """
        Collects startup info and adds a filename.
        """
        master = Tk()
        master.title("Startup Info")

        def inputStates():
            subject = subEntry.get()
            inGroup = varGrp.get()
            inBalance = varBal.get()

            if inGroup == 1:
                group = "FORCont"
            elif inGroup == 2:
                group = "FORReinst"
            elif inGroup == 3:
                group = "REMCont"
            elif inGroup == 4:
                group = "REMReinst"

            if inBalance == 1:
                balance = "A"
            elif inBalance == 2:
                balance = "B"

            master.quit()

            filename = subject + '_LMDFExp' + '.' + 'csv'

            return filename, subject, group, balance

        Label(master, text="VP Nummer:").grid(row=0,column=0, pady=10)
        subEntry = Entry(master)
        subEntry.grid(row=0, column=1)

        Label(master, text="Bitte Gruppe wählen:").grid(row=1, columnspan=2, pady=10)
        varGrp = IntVar()
        varGrp.set(1)
        groups =[("FORCont",1), ("FORReinst",2), ("REMCont",3), ("REMReinst",4)]
        for txt, val in groups:
            Radiobutton(master,
            text=txt,
            variable=varGrp,
            value=val).grid(row=2+val, columnspan=2, sticky=W, padx=70)

        Label(master, text="Bitte Faktor wählen:").grid(row=7, columnspan=2, pady=10)
        varBal = IntVar()
        varBal.set(1)
        balances = [("A", 1), ("B", 2)]
        for txt, val in balances:
            Radiobutton(master,
            text=txt,
            variable=varBal,
            value=val).grid(row=8+val, columnspan=2, sticky=W, padx=70)

        Button(master, text='Start', command=inputStates).grid(row=11, columnspan=2, pady=10)
        mainloop()

        filename, partnumber, group, balance = inputStates()

        return filename, partnumber, group, balance


    def initializePygame(self):
        """
        Intitializes pygame backends explicitly.
        """

        pygame.init()

    def createText(self, text, color):
        """Returns a pygame font instance."""

        return self.font.render(text, True, color, self.bgColor)

    def getWordsList(self, listname):
        """
        Reads word-pairs from a csv file and returns a randomly shuffled list
        that will serve as the study list.
        """

        # Opens the word list and saves it in "items" variable
        with open(listname, newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            items = []
            for row in reader:
                item = row[0]
                items.append(item)
            random.shuffle(items)
        return items

    def counterbalanceWordList(self, listA, listB):
        if self.balance == "A":
            wordlist1 = listA
            wordlist2 = listB
        elif self.balance == "B":
            wordlist1 = listB
            wordlist2 = listA
        return wordlist1, wordlist2

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
            random.shuffle(mathitems)
        return mathitems


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
