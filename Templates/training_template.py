from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter as tk
import numpy as np
import os
import cv2
import json
from getKeyPoints import getKeyPoints
from Modules.HmmEmission import hmmLearning
from tkinter import messagebox

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.datasetLocation = "Dataset/dataset.json"
        self.wordTransitionsLocation = "Dataset/wordTransitions.json"
        self.master = master
        self.text_number=0
        self.text_name = []
        self.text_filename = []
        self.wordsList = []
        self.fileLocations = []
        self.btn_file = []
        self.__init__window()

    def init_window(self):
        self.w = 500
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

    def init_menu(self):
        self.menubar = tk.Menu(self.master)
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.donothing)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="About...", command=self.donothing)
        self.helpmenu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.master.config(menu=self.menubar)

    def init_layout(self):
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(sticky="e")
        self.MainFrame = tk.Frame(self.master,width=self.ws)
        self.top_frame = tk.Frame(self.MainFrame,bg='#292f3d',width=self.ws,height=40)
        self.scroll_frame = tk.Canvas(self.MainFrame,bg='white',width=self.ws,height=40 ,yscrollcommand=self.scrollbar.set)
        self.bottom_frame = tk.Frame(self.MainFrame,bg='white',width=self.ws,height=40)

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.MainFrame.grid(row=0, sticky="wens")
        self.top_frame.grid(row=1, sticky="wens")
        self.scroll_frame.grid(row=2, sticky="wens")
        self.scrollbar.config(command=self.scroll_frame.yview)
        self.bottom_frame.grid(row=3, sticky="nw")

    def create_widgets(self):
        self.text_name.append(tk.Entry(self.scroll_frame,bg="#292f3d", fg="white", font=('bold',12)))
        self.text_name[len(self.text_name)-1].grid(row=len(self.text_name)-1,column=0,sticky="news")

        self.text_filename.append(tk.Entry(self.scroll_frame, bg="#292f3d", fg="white", font=('bold',12)))
        self.text_filename[len(self.text_filename)-1].grid(row=len(self.text_filename)-1,column=1,sticky="nesw")

        self.btn_file.append(tk.Button(self.scroll_frame,bg="gray", text="Insert File",font=('bold',12),width=14,command=self.get_filename))
        self.btn_file[len(self.btn_file)-1].grid(row=0,column=2,sticky="nesw")
        print("Entry:",len(self.text_name)-1)

        self.button_addword = tk.Button(self.bottom_frame, text="Add Word",font=('bold',12), command=self.add_entry)
        self.button_addword.grid(row=0,column=0,sticky="w")

        self.pv = tk.Button(self.bottom_frame, text="print values",font=('bold',12), command=self.print_values)
        self.pv.grid(row=0,column=1,sticky="w")

        self.btn_delete = tk.Button(self.bottom_frame,bg="red", text="Delete Entry",font=('bold',12),command=self.delete_entry)
        self.btn_delete.grid(row=0,column=2,sticky="w")

        self.button_train_word = tk.Button(self.bottom_frame, text="Start Training",font=('bold',12),bg="green",width=9,command=self.train_signs)
        self.button_train_word.grid(row=0,column=3,sticky="e")

        self.button_train_asd = tk.Button(self.bottom_frame, text="autoDoThis",font=('bold',12),bg="green",width=9,command=self.autoDoThis)
        self.button_train_asd.grid(row=0,column=4,sticky="e")
    
    def add_entry(self):
        if self.text_name[len(self.text_name)-1].get()=="" or self.text_filename[len(self.text_filename)-1].get()=="":
            pass
        else:
            self.text_name.append(tk.Entry(self.scroll_frame, bg="#292f3d", fg="white", font=('bold',12)))
            self.text_name[len(self.text_name)-1].grid(row=len(self.text_name)-1,column=0,sticky="nesw")

            self.text_filename.append(tk.Entry(self.scroll_frame, bg="#292f3d", fg="white", font=('bold',12)))
            self.text_filename[len(self.text_filename)-1].grid(row=len(self.text_filename)-1,column=1,sticky="nesw")

            self.btn_file.append(tk.Button(self.scroll_frame,bg="gray", text="Insert File",width=14,font=('bold',12),command=self.get_filename))
            self.btn_file[len(self.btn_file)-1].grid(row=len(self.btn_file)-1,column=2,sticky="nesw")

        print("Entry word:",len(self.text_name)," Entry file:",len(self.text_filename))

    def delete_entry(self):
        if len(self.text_name)-1==0:
            pass
        else:
            self.text_name[len(self.text_name)-1].destroy()
            self.text_name.pop(len(self.text_name)-1)

            self.text_filename[len(self.text_filename)-1].destroy()
            self.text_filename.pop(len(self.text_filename)-1)

            self.btn_file[len(self.btn_file)-1].destroy()
            self.btn_file.pop(len(self.btn_file)-1)

    def print_values(self):
        name = len(self.text_name)
        for x in range(name):
            print("Word: ",self.text_name[x].get(),"  File:",self.text_filename[x].get())
            # print("  File path: ", self.fileLocations[x])

    def get_filename(self):
        self.master.filename =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
        self.name = os.path.basename(self.master.filename)
        self.text_filename[len(self.btn_file)-1].delete(0,tk.END)
        self.text_filename[len(self.btn_file)-1].insert(0,self.name)

        self.fileLocations.append(self.master.filename)
        print (self.master.filename)
    
    def donothing(self):
        x = 0

    def train_signs(self):
        self.wordsList = []
        for i in self.text_name:
            self.wordsList.append(str(i.get()).lower())
        print(self.wordsList)
        numOfWords = len(self.text_name)
        if "" not in self.wordsList or "" not in self.fileLocations:
            for i in range(numOfWords):
                wordName = self.wordsList[i]
                fileLocation = self.fileLocations[i]
                # print("Word:",self.wordsList[i])
                # print("Location:",self.fileLocations[i])
                openPose = getKeyPoints()
                openPose.learn(fileLocation,showDisplay=False)
                self.saveToDataset(openPose.getKeyPoints(), wordName)
            with open(self.wordTransitionsLocation,'r') as wordTransitionsDataset:
                transitionsDataset = json.load(wordTransitionsDataset)
                transitionsDataset['sentences'].append(self.wordsList)
                datasetString = json.dumps(transitionsDataset, cls=MyEncoder)
                f = open(self.wordTransitionsLocation,'w')
                f.write(datasetString)
                f.close()

        else:
            print('SOMETHING IS EMPTY PLEASE FILL IT IN!!!')

        learning = hmmLearning(self.datasetLocation)
        learning.startLearnFromDataset()
        learning.saveLearningCache()

        for i in range(len(self.text_name)):
            self.delete_entry()
        self.text_filename[0].delete(0,'end')
        self.text_name[0].delete(0,'end')

        print('FINISHED!!!')
        messagebox.showinfo("Complete", 'Learn Complete!!!')

    def saveToDataset(self,data,word):
        
        f = open(self.datasetLocation,'r')
        for line in f:
            strJSON = line
        f.close()
        dataset = json.loads(strJSON)
        if word.lower() not in dataset.keys():
            dataset[word.lower()] = [data]
        else:
            dataset[word.lower()].append(data)

        datasetString = json.dumps(dataset, cls=MyEncoder)
        f = open(self.datasetLocation,'w')
        f.write(datasetString)
        f.close()

        # self.doEmissionTest()


    def doEmissionTest(self):

        datasetLearn = emissionLearn(self.datasetLocation)
        datasetLearn.start()
        datasetLearn.saveData()

    def autoDoThis(self):
        mgaWords = [
            ['you','okay'],
            ['you','okay'],
            ['you','okay'],
            ['you','okay'],
            ['you','okay'],
            ['good','morning'],
            ['good','morning'],
            ['good','morning'],
            ['good','morning'],
            ['good','morning'],
            ['good','morning'],
            ['how','you'],
            ['how','you'],
            ['how','you'],
            ['how','you'],
            ['how','you'],
            ['how','you'],
            ['how','you'],
            ['how','you'],
            ['how','you'],
            ['old','you'],
            ['old','you'],
            ['old','you'],
            ['old','you'],
            ['old','you'],
            ['old','you'],
            ['old','you'],
            ['i','like','you'],
            ['i','like','you'],
            ['i','like','you'],
            ['i','like','you'],
            ['i','like','you'],
            ['im','fine'],
            ['im','fine'],
            ['im','fine'],
            ['im','fine'],
            ['im','fine'],
            ['im','fine'],
            ['im','fine'],
            ['eat'],
            ['eat'],
            ['eat'],
            ['eat'],
            ['where','you','from'],
            ['where','you','from'],
            ['where','you','from'],
            ['where','you','from'],
            ['doing'],
            ['doing'],
            ['doing'],
            ['doing'],
            ['nice','meet','you'],
            ['nice','meet','you'],
            ['nice','meet','you'],
            ['nice','meet','you']
            ]
        mgaLocation = [
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 1\\You 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 1\\Okay 1.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 2\\You 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 2\\Okay 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 3\\You 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 3\\Okay 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 4\\You 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 4\\Okay 4.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 5\\You 5.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Are you okay\\You Okay 5\\Okay 5.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 1\\Good 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 1\\Morning 1.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 2\\Good 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 2\\Morning 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 3\\Good 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 3\\Morning 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 4\\Good 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 4\\Morning 4.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 5\\Good 5.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 5\\Morning 5.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 6\\Good 6.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Good Morning\\Good Morning 6\\Morning 6.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 1\\How 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 1\\You 1.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 2\\How 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 2\\You 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 3\\How 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 3\\You 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 4\\How 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 4\\You 4.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 5\\How 5.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 5\\You 5.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 6\\How 6.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 6\\You 6.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 7\\How 7.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 7\\You 7.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 8\\How 8.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 8\\You 8.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 9\\How 9.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How are you\\How You 9\\You 9.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 1\\Old.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 1\\You.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 2\\Old 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 2\\You 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 3\\Old 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 3\\You 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 4\\Old 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 4\\You 4.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 5\\Old 5.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 5\\You 5.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 6\\Old 6.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 6\\You 6.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 7\\Old 7.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\How old are you\\Old You 7\\You 7.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 1\\I 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 1\\Like 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 1\\You 1.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 2\\I 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 2\\Like 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 2\\You 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 3\\I 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 3\\Like 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 3\\You 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 4\\I 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 4\\Like 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 4\\You 4.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 5\\I 5.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 5\\Like 5.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I like you\\I Like You 5\\You 5.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\I\'m Fine 1\\Im 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\I\'m Fine 1\\Fine 1.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 2\\Im 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 2\\Fine 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 3\\Im 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 3\\Fine 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 4\\Im 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 4\\Fine 4.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 5\\Im 5.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 5\\Fine 5.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 6\\Im 6.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 6\\Fine 6.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 7\\Im 7.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\I\'m fine\\Im Fine 7\\Fine 7.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Let\'s eat\\Eat 1\\Eat 1.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Let\'s eat\\Eat 2\\Eat 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Let\'s eat\\Eat 3\\Eat 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Let\'s eat\\Eat 4\\Eat 4.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 1\\Where 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 1\\You 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 1\\From 1.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 2\\Where 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 2\\You 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 2\\From 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 3\\Where 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 3\\You 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 3\\From 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 4\\Where 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 4\\You 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Where are you from\\Where You From 4\\From 4.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\What are you doing\\Doing 1\\Doing 1.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\What are you doing\\Doing 2\\Doing 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\What are you doing\\Doing 3\\Doing 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\What are you doing\\Doing 4\\Doing 4.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 1\\Nice 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 1\\Meet 1.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 1\\You 1.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 2\\Nice 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 2\\Meet 2.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 2\\You 2.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 3\\Nice 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 3\\Meet 3.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 3\\You 3.mp4'],
            ['D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 4\\Nice 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 4\\Meet 4.mp4',
            'D:\\Users\\JanlofreDy\\Desktop\\Sign Language Videos\\Nice to meet you\\Nice Meet You 4\\You 4.mp4']
            ]
        # print(len(mgaWords),len(mgaLocation))
        for sentNum in range(len(mgaWords)):
            for wordNum in range(len(mgaWords[sentNum])):
                wordName = mgaWords[sentNum][wordNum]
                fileLocation =  mgaLocation[sentNum][wordNum]
                openPose = getKeyPoints()
                openPose.learn(fileLocation,showDisplay=False)
                self.saveToDataset(openPose.getKeyPoints(), wordName)
                # f = open('MgaKeypointsEachWord\\'+str(i)+str(mgaWords[i])+'.txt','w')
                # f.write(str(openPose.getKeyPoints()))
                # f.close()
            with open(self.wordTransitionsLocation,'r') as wordTransitionsDataset:
                transitionsDataset = json.load(wordTransitionsDataset)
                transitionsDataset['sentences'].append(mgaWords[sentNum])
                datasetString = json.dumps(transitionsDataset, cls=MyEncoder)
                f = open(self.wordTransitionsLocation,'w')
                f.write(datasetString)
                f.close()
                
        learning = hmmLearning(self.datasetLocation)
        learning.startLearnFromDataset()
        learning.saveLearningCache()
        print('FINISHED!!!')
        messagebox.showinfo("Complete", 'Learn Complete!!!')

    __init__window = init_window
    __init__menu = init_menu
    __init__winlayout = init_layout
    __init__widgets = create_widgets