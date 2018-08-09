'''
AUTHOR: OMER HEN
PURPOSE: class Graph for my Hemda Final Project 2017-2018: Nuclear Fission Reactor

This is a seperate program from Reactor.

In order to use this part of the model, copy the name of the data file that was printed onto the simulation when you run Reactor
Then run this program to recieve the k-variable by iterations graph. Note that the data file is updated every "update" iterations.
See Data_lib to change "update".

'''

import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#### Graph Settings ####

filename = '03;10PM on August 09, 2018.txt' # paste the data file name plus the ending (example: testing.txt)

graph_title = "Default Settings"

xaxis_label = "Iterations"

yaxis_label = "K Variable"

#######################################


PATH = os.path.dirname(os.path.realpath(__file__)) + "\Runs\\" + filename 

class Graph:

    x = [] #Time/Ticks/Iterations
    y = [] #K Variable

    fig = plt.figure()
    
    def __init__(self):
        ''' Constractor --> calls all essentiall methods '''
        self.readFile()
        self.graph()

    def readFile(self):
        ''' Reading the information from specified data file and preparing it for plotting '''
        
        with open(PATH) as file:
            self.y = file.readlines()

        self.y = [round(float(line.strip()),3) for line in self.y]
        self.x = [tick+1 for tick in range(len(self.y))]

        print("Average k value: ", sum(self.y)/len(self.y))

    def graph(self):
        ''' Configuring the figure and graph settings and plotting the information onto the graph '''
        
        self.fig.canvas.set_window_title('Fission Reactor K Variable Graph - Omer Hen')
        
        plt.plot(self.x,self.y,'bo',ms = 2,label='data') #PLotting the data points

        plt.legend(loc=1, title='graphs', fontsize=12)
        plt.grid(True)
        plt.xlabel(xaxis_label, fontsize=16)
        plt.ylabel(yaxis_label, fontsize=16)
        plt.title(graph_title, fontsize=16)
        plt.show()
        
        
if __name__ == "__main__":
    graph = Graph()
