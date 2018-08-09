'''
AUHTOR: OMER HEN
PURPOSE: class Data for my Hemda Final Project 2017-2018: Nuclear Fission Reactor

This class saves the k variable in a file every predefined number of iterations in order for data analysis after
the end of the simulation. 

'''

import os
import datetime

PATH = os.getcwd() + '\Runs'

class Data:

    k = []          #K list: will hold all the values of k --> from here to be written into the file
    update = 100    #How often (in iteration) does the data file needs to be updated
    
    def __init__(self):
        '''Constractor --> executes essential methods when called. '''

        self.filepath = ''
        
        self.createFolder()
        self.createFile()

    def createFile(self):
        ''' Creates a new data text file called: the spesific date at that moment. This file will record the data from the simulation '''
        
        filename = datetime.datetime.now().strftime("%I;%M%p on %B %d, %Y")+".txt" #Name of the text file 
        self.filepath = os.path.join(PATH,filename)                                #Creates the text file

        print(self.filepath) #Printing the exact path of the file to the console --> for user to find.
            
    def createFolder(self):
        ''' If a "Runs" folder does not exist, create it in order to store the data text file in it '''
        
        if not os.path.exists(PATH):
            os.makedirs(PATH)

    def update_k_factor(self,k_variable):
        ''' Called every iterations --> appending the k variable to the k list, and checking if the file needs to be updated '''
        
        self.k.append(k_variable)

        if (len(self.k) % self.update == 0):
            file = open(self.filepath, "w")
            
            file.truncate(0)                                                #Delete the former contects of the file
            file.write('\n'.join(str(round(elem,3)) for elem in self.k))    #Write all the new positions including the old ones

            file.close()
