#coding:utf-8
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
from hopfield import HOP


class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.training_data_num = 0
        self.testing_data_num = 0
        self.classify_data_index = 0
        self.input_x = 0
        self.input_y = 0
        self.training_data = []
        self.testing_data = []
        self.testing_result = []
        self.root = master
        self.grid()
        self.create_widgets()


    def create_widgets(self):

        self.winfo_toplevel().title("Yochien NN HW3")

        # 選取訓練資料集檔案
        self.load_training_data_label = tk.Label(self)
        self.load_training_data_label["text"] = "載入訓練資料集"
        self.load_training_data_label.grid(row=0, column=0, sticky=tk.N+tk.W)

        self.load_training_data_button = tk.Button(self)
        self.load_training_data_button["text"] = "選取檔案"
        self.load_training_data_button.grid(row=0, column=1, sticky=tk.N+tk.W)
        self.load_training_data_button["command"] = self.load_training_data

        self.training_data_file_path_label = tk.Label(self)
        self.training_data_file_path_label["text"] = ""
        self.training_data_file_path_label.grid(row=0, column=2, sticky=tk.N+tk.W)

        # 選取測試資料集檔案
        self.load_testing_data_label = tk.Label(self)
        self.load_testing_data_label["text"] = "載入測試練資料集"
        self.load_testing_data_label.grid(row=1, column=0, sticky=tk.N+tk.W)

        self.load_testing_data_button = tk.Button(self)
        self.load_testing_data_button["text"] = "選取檔案"
        self.load_testing_data_button.grid(row=1, column=1, sticky=tk.N+tk.W)
        self.load_testing_data_button["command"] = self.load_testing_data

        self.testing_data_file_path_label = tk.Label(self)
        self.testing_data_file_path_label["text"] = ""
        self.testing_data_file_path_label.grid(row=1, column=2, sticky=tk.N+tk.W)

        # run run
        self.run_label = tk.Label(self)
        self.run_label["text"] = "進行訓練及測試"
        self.run_label.grid(row=2, column=0, sticky=tk.N+tk.W)

        self.run_button = tk.Button(self)
        self.run_button["text"] = "Run"
        self.run_button.grid(row=2, column=1, sticky=tk.N+tk.W)
        self.run_button["command"] = self.run

        self.classify_origin_label = tk.Label(self)
        self.classify_origin_label["text"] = "測試資料"
        self.classify_origin_label.grid(row=3, column=0, sticky=tk.N+tk.W)
        
        self.classify_origin_data_label = tk.Label(self)
        self.classify_origin_data_label["text"] = ""
        self.classify_origin_data_label.grid(row=3, column=1, sticky=tk.N+tk.W)

        self.classify_label = tk.Label(self)
        self.classify_label["text"] = "辨識結果"
        self.classify_label.grid(row=4, column=0, sticky=tk.N+tk.W)
        
        self.classify_data_label = tk.Label(self)
        self.classify_data_label["text"] = ""
        self.classify_data_label.grid(row=4, column=1, sticky=tk.N+tk.W)

        self.change_classify_data_button = tk.Button(self)
        self.change_classify_data_button["text"] = "切換辨識資料"
        self.change_classify_data_button.grid(row=3, column=0, sticky=tk.N+tk.W)
        self.change_classify_data_button["command"] = self.change_classify_data

    def change_classify_data(self):
        self.classify_data_index += 1
        if self.classify_data_index >= self.testing_data_num:
            self.classify_data_index = 0
        print(self.print_format(self.testing_data[self.classify_data_index]))
        print(self.print_format(self.testing_data[self.classify_data_index]))
        self.classify_origin_data_label["text"] = self.get_print_format(self.testing_data[self.classify_data_index])
        self.classify_data_label["text"] = self.get_print_format(self.testing_result[self.classify_data_index])

    def load_training_data(self):
        try:
            self.training_data = []
            filename = askopenfilename()
            self.training_data_file_path_label["text"] = filename
            if (filename.split('/')[len(filename.split('/'))-1].split("_")[0]) == "Basic":
                self.input_x = 9
                self.input_y = 13
            elif (filename.split('/')[len(filename.split('/'))-1].split("_")[0]) == "Bonus":
                self.input_x = 10
                self.input_y = 11
            f = open(filename, "r")
            line_num = 0
            for line in f:
                line_num += 1
            f = open(filename, "r") 
            print(line_num)
            self.training_data_num = int((line_num + 1) / self.input_y)
            print(self.training_data_num)
            for i in range(self.training_data_num):
                a = []
                for j in range(self.input_y):
                    line = f.readline()
                    if j == self.input_y - 1 :
                        break
                    for c in line:
                        if c == '\n':
                            break
                        elif c == ' ':
                            a.append(0)
                        else:
                            a.append(c)
                #print(a)
                #print(len(a))
                self.training_data.append(a)

                
            for data in self.training_data:
                self.print_format(data)
        except Exception as e:
            print(e)
            self.training_data_file_path_label["text"] = ""

    def load_testing_data(self):
        self.testing_data = []
        try:
            filename = askopenfilename()
            self.testing_data_file_path_label["text"] = filename
            if (filename.split('/')[len(filename.split('/'))-1].split("_")[0]) == "Basic":
                self.input_x = 9
                self.input_y = 13
            elif (filename.split('/')[len(filename.split('/'))-1].split("_")[0]) == "Bonus":
                self.input_x = 10
                self.input_y = 11
            f = open(filename, "r")
            line_num = 0
            for line in f:
                line_num += 1
            f = open(filename, "r") 
            print(line_num)
            self.testing_data_num = int((line_num + 1) / self.input_y)
            print(self.testing_data_num)
            for i in range(self.testing_data_num):
                a = []
                for j in range(self.input_y):
                    line = f.readline()
                    if j == self.input_y - 1:
                        break
                    for c in line:
                        if c == '\n':
                            break
                        elif c == ' ':
                            a.append(0)
                        else:
                            a.append(c)
                #print(a)
                #print(len(a))
                self.testing_data.append(a)

                
            for data in self.testing_data:
                self.print_format(data)
        except Exception as e:
            print(e)
            self.testing_data_file_path_label["text"] = ""
        
    def print_format(self, a):
        s = ''
        for c in a:
            if c == 0 or c == 0.:
                c = '　'
            elif c == 1 or c == 1.:
                c = '１'
            s += c
            if(len(s) == self.input_x):
                print(s)
                s = ''

    def get_print_format(self, a):
        ss = ''
        s = ''
        for c in a:
            if c == 0 or c == 0.:
                c = '　'
            elif c == 1 or c == 1.:
                c = '１'
            s += c
            if(len(s) == self.input_x):
                ss += s
                ss += '\n'
                s = ''
        return ss

    def run(self):
        if(self.training_data_file_path_label["text"] == "" or self.testing_data_file_path_label["text"] == "" ):
            print("未選取檔案")
            tk.messagebox.showinfo("Error","未選取資料集")
            return
        hop = HOP(self.input_x * (self.input_y-1))
        hop.hopTrain(self.training_data)
        for data in self.testing_data:
            print("Origin:")
            self.print_format(data)
            result = hop.hopRun(data)
            print("Recovered:")
            self.print_format(result)
            self.testing_result.append(result)


        



root = tk.Tk()
app = Application(root)
root.mainloop()
