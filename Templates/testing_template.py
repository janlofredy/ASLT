from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter as tk
import numpy as np
import os
import cv2
import json
from getKeyPoints import getKeyPoints
from Modules.EmissionTest import emissionTest
from tkinter import messagebox
from Modules.HMM import HMM
import time
import copy
from threading import Thread

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.openPose = getKeyPoints()
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
        # self.tryTestAll()
        # PLAY VIDEO WHILE PROCESSING VIDEO
        self.tr = Thread(target=self.openPose.learn,args =(self.master.filename, False, self.lbl_Words, self.v_tab, self.video_tab) )
        self.tr2 = Thread(target=self.tryHmmEmission)
        self.tr.daemon = True
        self.tr2.daemon = True
        try:
            self.tr.start()
            self.tr2.start()
        except Exception as e:
            raise

        # print(self.master.filename)
        # PLAY VIDEO AFTER LEARNING
        # self.openPose.learn(self.master.filename, False, self.lbl_Words, self.v_tab,[self.video_tab.winfo_width(),self.video_tab.winfo_height()])
        # self.tryHmmEmission()
        # self.video = openPose.getPosedVideo()
        # # self.cap_video(self.master.filename)
        # # self.play_video()

    def tryHmmEmission(self):
        self.tr.join()
        self.tr._stop()
        testData = self.openPose.keypoints


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
            # print(key,value)
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

        # print(str(posSent))
        print(ansWithCount)
        print(self.getMax(ansWithCount))
        self.tempANSWER = ansWithCount
        ansString = ""
        for i,j in sorted(ansWithCount.items(), key = 
             lambda kv:(kv[1], kv[0]), reverse=True):
            print(i,j)
            ansString += str(i) + "=" + str(j) + "\n"

        self.lbl_Words['text'] = self.getMax(ansWithCount)
        messagebox.showinfo("Possible Answers", ansString)



    def tryTestAll(self):
        sent = [
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\are You Okay\\1.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\are You Okay\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\are You Okay\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\are You Okay\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\are You Okay\\5.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\are You Okay\\6.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\are You Okay\\7.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\are You Okay\\8.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Good Morning\\1.mov",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Good Morning\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Good Morning\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Good Morning\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Good Morning\\5.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Good Morning\\6.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Good Morning\\7.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Good Morning\\8.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Good Morning\\9.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\1.mov",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\5.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\6.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\7.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\8.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\9.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\10.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\How are You\\11.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\how Old are You\\1.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\how Old are You\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\how Old are You\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\how Old are You\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\how Old are You\\5.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\how Old are You\\6.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\how Old are You\\7.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\how Old are You\\8.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\how Old are You\\9.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I Like You\\1.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I Like You\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I Like You\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I Like You\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I Like You\\5.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I Like You\\6.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I'm Fine\\1.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I'm Fine\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I'm Fine\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I'm Fine\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I'm Fine\\5.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I'm Fine\\6.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I'm Fine\\7.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I'm Fine\\8.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\I'm Fine\\9.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\let's Eat\\1.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\let's Eat\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\let's Eat\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\let's Eat\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\let's Eat\\5.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Nice to Meet You\\1.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Nice to Meet You\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Nice to Meet You\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Nice to Meet You\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Nice to Meet You\\5.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Nice to Meet You\\6.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Nice to Meet You\\7.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Nice to Meet You\\8.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Nice to Meet You\\9.mov",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\what are you Doing\\1.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\what are you Doing\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\what are you Doing\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\what are you Doing\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\what are you Doing\\5.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Where are You From\\1.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Where are You From\\2.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Where are You From\\3.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Where are You From\\4.MOV",
                "D:\\Users\\JanlofreDy\\Desktop\\By Sentence\\Where are You From\\5.MOV",
                ]
        ans = {}
        for i in sent: 
            print(i)
            self.openPose.learn(videoLocation = i, showDisplay =False, label = self.lbl_Words, vFrame = self.v_tab, scrSize = self.video_tab)
            self.tryHmmEmission()
            ans[i] = self.tempANSWER
        print(ans)
        print('Finished Test All')


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