from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter as tk
import numpy as np
import os
import cv2
import json
from getKeyPoints import getKeyPoints
from Modules.EmissionTest import emissionTest
from Modules.HMM import HMM
import time
import copy
from threading import Thread

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.__init__window()
        self.har = 0
        self.frameNum = -1
        self.video = ''
        self.notIncludedParts = ['neck','nose','midHip','rightShoulder','leftShoulder','rightElbow','leftElbow']
    #Don't mind, just a null function
    def donothing(self):
        x = 0
    #initializing Window
    def init_window(self):
        self.w = 1000
        self.h = 700
        self.ws = self.master.winfo_screenwidth()
        self.hs = self.master.winfo_screenheight()
        self.x = (self.ws/2) - (self.w/2)
        self.y = (self.hs/2) - (self.h/2)
        self.master.geometry('%dx%d+%d+%d'%(self.w,self.h,self.x,self.y))
        self.master.title('ASLT Prototype')
        self.master.configure(background='white')
        self.master.iconbitmap(r'Assets/icons/sign/favicon.ico')
        self.__init__menu()
        self.__init__winlayout()
        self.__init__widgets()
        self.openPose = getKeyPoints()
        self.tr = None
        self.tr2 = None
    # initializing Menu
    def init_menu(self):
        self.menubar = tk.Menu(self.master)
        self.menubar.add_cascade(label="Test Video",command=self.get_filename )
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.donothing)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="About...", command=self.donothing)
        self.helpmenu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.master.config(menu=self.menubar)
    #initializing Layouts
    def init_layout(self):
        #Initialization
        self.top_pane = tk.Frame(self.master,bg='white',width=self.ws, height=40, pady=3)
        self.video_tab = tk.Frame(self.master,bg='Black',width=self.ws, padx=10,pady=3)
        self.words_tab = tk.Frame(self.master,bg='white',width=self.ws, height=80, pady=3)
        self.stats_tab = tk.Frame(self.master,bg='white',width=self.ws, height=20, pady=3)
        # layout all of the main containers
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        # Set rows and directions
        self.top_pane.grid(row=0, sticky="wens")
        self.video_tab.grid(row=1, sticky="wens")
        self.words_tab.grid(row=2, sticky="wens")
        self.stats_tab.grid(row=3, sticky="wens")

    def create_widgets(self):
        #
        self.lbl_Words=tk.Label(self.words_tab,text="", bg="white", fg="black", font=('bold',25),padx=10,pady=10)
        self.lbl_Words.grid(row=0,column=0,sticky="nesw")
        # #
        # self.lbl_stats=tk.Label(self.stats_tab,text="Statistics X:0.213213  Y:0.193413", font='bold')
        # self.lbl_stats.grid(row=0,column=0,sticky="nesw")
        #
        self.lbl_filename=tk.Label(self.stats_tab,text="Filename: ",bg='white',fg='black',font='bold')
        self.lbl_filename.grid(row=0,column=1)
        # 
        self.v_tab = tk.Label(self.video_tab,bg="black")
        self.v_tab.pack(fill=tk.BOTH,expand=1)

    def get_filename(self):
        self.master.filename =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("mp4 files","*.mp4"),("mov files","*.mov")))
        self.name = os.path.basename(self.master.filename)
        self.lbl_filename.configure(text="Filename: "+self.name)
        # print (self.master.filename)

        self.lbl_Words['text'] = "Processing Please Wait..."
        # self.lbl_Words.configure(text="Processing Please Wait...")

       
        # self.openPose = getKeyPoints()
        self.tr = Thread(target=self.openPose.learn,args =(self.master.filename, False, self.lbl_Words, self.v_tab, self.video_tab) )
        self.tr2 = Thread(target=self.tryHmmEmission)
        self.tr.daemon = True
        self.tr2.daemon = True
        try:
            self.tr.start()
            self.tr2.start()
            # self.tr.join()
            # self.tr2.join()

        except Exception as e:
            raise
        # self.openPose.learn(self.master.filename, False, self.lbl_Words, self.v_tab,[self.video_tab.winfo_width(),self.video_tab.winfo_height()])
        # self.video = openPose.getPosedVideo()

        # # self.cap_video(self.master.filename)
        # # self.play_video()
        # self.tryHmmEmission()

    def tryHmmEmission(self):
        self.tr.join()
        self.tr._stop()
        testData = self.openPose.keypoints
        datasByParts = {}
        for frame in testData:
            for part, keyPointsXnY in frame.items():
                if part not in self.notIncludedParts:
                    for i in range(2):
                        partName = part+'X' if i==0 else part+'Y'
                        if partName not in datasByParts.keys():
                            datasByParts[partName] = [round(keyPointsXnY[i])]
                        else:
                            datasByParts[partName].append(round(keyPointsXnY[i]))


        with open('Dataset/learningCache.json') as json_file:
            file = json.load(json_file)
            # print(file.keys())

            forInitProb = []
            forTransition = []

            states = tuple(file['states'])

            for i in states:
                forInitProb.append(file['initialProbabilities'][i]/sum(file['initialProbabilities'].values()))
                tempInner = []
                for j in states:
                    # print(file['transitionProbabilities'][i][j])
                    tempInner.append(file['transitionProbabilities'][i][j])
                # print(tempInner)
                forTransition.append(tempInner)
            # print(forTransition)

            pi = forInitProb
            A = forTransition

            mgaAnswers = {}

            for key, value in file['emissions'].items():
                # print(key)
                observations = tuple(value['observations'][0])

                forEmission = {}
                for st in states:
                    forEmission[str(st)] = []

                for i in states:
                    for j in observations:
                        forEmission[str(i)].append(value['emissionProbabilities'][str(j)][str(i)])

                emm = []
                for i in states:
                    emm.append(forEmission[i])
                B = emm
                sequence = []
                for i in datasByParts[key]:
                    if i in observations:
                        sequence.append(observations.index(i))

                states = states
                pi = np.array(pi)
                A = np.array(A)
                observations = observations
                B = np.array(B)
                sequence = np.array(sequence)
                hmm = HMM(states, pi, A, observations, B, sequence)
                mgaAnswers[key] = hmm.getSequence() if type(hmm.getSequence()) == type(list()) else []


            print('The Possible answers are')
            posAns = {}
            for key, value in mgaAnswers.items():
                tempAns = [value[0]]
                for j in range(1,len(value)):
                    if value[j] != value[j-1]:
                        tempAns.append(value[j])
                posAns[key] = tempAns

            posSent = []
            ansWithCount = {}
            for key,value in posAns.items():
                sent = ""
                for w in value:
                    sent+=w+" "
                if sent not in ansWithCount.keys():
                    ansWithCount[sent] = 1
                else:
                    ansWithCount[sent] += 1
                if sent not in posSent:
                    posSent.append(sent)

            print(str(posSent))
            print(ansWithCount)
            self.lbl_Words['text'] = self.getMax(ansWithCount)





    def tryEmissionTest(self,testData):
        emTest = emissionTest(testData)
        emTest.start()
        emissions = emTest.getEmissions()
        parts = list(emissions[0].keys())
        wordss = list(emissions[0]['leftLFOneX'].keys())
        print(parts)
        print(wordss)
        some = {}
        for frame in emissions:
            # print("FRAME!!!!\n\n\n\n")
            for part,datas in frame.items():
                if part not in some.keys():
                    some[part] = {}
                for word,val in datas.items():
                    if word not in some[part].keys():
                        some[part][word] = val
                    else:
                        some[part][word] += val
        # print(some)
        mgaAns = []
        for  k,v in some.items():
            an = self.getMax(v)
            mgaAns.append(an)
            print(k, an, v)
        print(mgaAns)

    def getMax(self, PartWords):
        curMax = 0
        maxWord = ''
        counter = 0
        for word, val in PartWords.items():
            if counter==0:
                curMax = val
                maxWord = word
            else:
                if val > curMax:
                    curMax = val
                    maxWord = word
            counter+=1
        return maxWord



    def cap_video(self,filename):
        # self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture(filename)

    def nextFrame(self):
        if self.frameNum <= len(self.video):
            self.frameNum += 1
            return self.video[self.frameNum]
        return None


    def play_video(self):
        sad = 1
        try:
            frame = self.nextFrame()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(img.resize((self.video_tab.winfo_width(),self.video_tab.winfo_height())))
            self.v_tab.imgtk = imgtk
            self.v_tab.configure(image=imgtk)
            self.v_tab.after(100, self.play_video)
        except:
            pass
            self.frameNum = -1

    def update_stat(self,i):
        self.lbl_stats.config(text="FPS :"+str(i)+" Accuracy :"+str(i)+"", font='bold')

    #Private Objects of the functions
    __init__window = init_window
    __init__menu = init_menu
    __init__winlayout = init_layout
    __init__widgets = create_widgets