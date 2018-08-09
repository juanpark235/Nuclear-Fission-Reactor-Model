'''
AUTHOR: OMER HEN
PURPOSE: class Display for my Hemda Final Project 2017-2018: Nuclear Fissio Reactor

This class handles all of the display related operations and methods that needs to be performed in order for the simulation to update itself and show on the monitor
There are four axs in the simulation, each displays a different piece of information:

1. Main axs:                      Displays the actuall fission simulation of the core, including the fuel particles, neutrons and rods. 
2. Energy graph axs:              Displays a graph with the average energy produced every five iterations
3. Power output and change axs:   Displays text with the current power output of the reactor and the power change since last iteration
4. Iterations and k value axs:    Displays the current iteration number and the current value of the "k" variable 

Also includes a pause feature, in which the user can click on the screen of the simulation and pause it for unlimited time, then click on the screen again
to continue the simulation
'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Display:
    fig = plt.figure() #Main Figure 
    frame_counter = 0  #Counts the frames/ticks/iterations 
    pause = False      #If true, the simulation will pause

    def __init__(self,bounds,size,power_desired):
        ''' Constractor:
            size = size of particles on the monitor (related to the graphics of the simulation)
            bounds = bounds of the core, everything happens within the bounds
            power_desired = a power value that is desired to be achieved and maintained by the reactor
        '''
        self.bounds = bounds
        self.size = size
        self.power_desired = power_desired
        
        self.createAxs()
        self.createPlots()
        self.initializeFigure() 
 

    def createAxs(self):
        ''' Creates the different axs according to settings that were meant to beautify and organize the simulation and do not matter for it's scientific part '''
        
        self.ax1 = plt.subplot2grid((3,3),(0,0), rowspan = 3, colspan = 2, aspect = 'equal',
                      autoscale_on = False, xlim = (self.bounds[0]-1.2,self.bounds[1]+1.2), ylim = (self.bounds[2]-0.4,self.bounds[3]+0.4)) #Fission axs 
        self.ax2 = plt.subplot2grid((3,3),(1,2))                                                                                            #Energy graph axs
        self.ax3 = plt.subplot2grid((3,3),(0,2),aspect='equal',autoscale_on = False)                                                        #Power output and change axs
        self.ax4 = plt.subplot2grid((3,3),(2,2),aspect='equal',autoscale_on = False)                                                        #Iterations and k value axs


    def createPlots(self):
        ''' Creates the plots objects which will be used to plot information into the first axs, each plot object plots a differnet particle '''
        
        self.plot_neutrons, = self.ax1.plot([],[],'yo',ms = self.size) #This is where self.size comes in, as it is the physical size of the particles, 
        self.plot_fuel, = self.ax1.plot([],[],'ro',ms = self.size)     #and helps set the proportion ratio in the simulation --> to organize and beautify the simulation
        self.plot_rods, = self.ax1.plot([],[],'co',ms = self.size)
                             

    def initializeFigure(self):
        ''' Initializes each axs according to its spesific tasks '''
        
        self.fig.canvas.set_window_title('Fission Reactor - Omer Hen')
        self.fig.subplots_adjust(left=0,bottom=0,right=0.96,top=0.97,wspace=0.37,hspace=0) #To better organize the simulation

        #First Axs#
        rect = plt.Rectangle(self.bounds[::2],                  #Bottom-Corner
                             self.bounds[1] - self.bounds[0],   #Width 
                             self.bounds[3] - self.bounds[2],   #Height
                             ec='black', lw=2, fc='black')      #Background of the core. Created upon the sizes of the bounds


        self.ax1.add_patch(rect)
        self.ax1.axis('off')

        #Second Axs#
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Power')
        self.ax2.set_title('Energy Produced')
        self.ax2.ticklabel_format(style = 'plain')
        self.ax2.axhline(y = self.power_desired, color = 'green')
        self.ax2.set_ylim([0,(self.power_desired*3)])

    def plotPower(self,power,power_change,k):
        ''' Recieves the info about the current power output, power change since last iteration and k value and prepares them to be plotted into their appropriate axs '''

        self.power = "Power Output:" +  str(power)
        self.powerChange = "Power Change:" + str(power_change)
        self.k = "k: " + str(round(k,3))

    def plotThirdAxs(self):
        ''' Plots the power output and power change in the third axs '''
        
        self.ax3.clear() #First vlear the old values 
        self.ax3.plot(0.5,0.5,color = 'white')

        self.ax3.text(0.49,0.5, self.power, fontsize = 14, horizontalalignment = 'center')          #Plots power output 
        self.ax3.text(0.49,0.49, self.powerChange, fontsize = 14, horizontalalignment = 'center')   #Plots power change

        self.ax3.axis('off')

    def plotSecondAxs(self,power_list):
        ''' Plots the average energy output in the second axs '''
        
        x_positions = []
        y_positions = []
        
        for tick in range(self.frame_counter):
            x_positions.append(tick + 1) #tick + 1 since the for loop is required to start at 0 due to the indexs in an array
            y_positions.append(power_list[tick])

        self.ax2.plot(x_positions,y_positions,color = 'black')

    def plotFourthAxs(self):
        ''' Plots the iteration number and "k" variable value in the fourth axs '''
        
        self.ax4.clear() #First clear the old values 
        self.ax4.plot(0.5,0.5,color = 'white')

        itr_num = "Iteration:" + str(self.frame_counter) 

        self.ax4.text(0.49,0.5, itr_num, fontsize = 14, horizontalalignment = 'center') #Plots the iteration number
        self.ax4.text(0.49,0.49, self.k, fontsize = 14, horizontalalignment = 'center') #Plots the k variable value

        self.ax4.axis('off')
        
    def plotNeutrons(self,x_positions,y_positions):
        ''' Recieves data about the new x and y positions of the neutrons, and plots them on the monitor '''
        
        self.plot_neutrons.set_data(x_positions,y_positions)
    
    def plotFuel(self,x_positions,y_positions):
        ''' Recieves data about the new x and y positions of the fuel particles, and plots them on the monitor --> in case a fuel particle was removed by a collision with a neutron '''

        self.plot_fuel.set_data(x_positions,y_positions)

    def plotRods(self,x_positions,y_positions):
        ''' Recieves data about the new x and y positions of the rods, and plots them on the monitor --> in case rods were added/removed'''

        self.plot_rods.set_data(x_positions,y_positions)

    def getFigure(self):
        ''' Returns the figure '''
        
        return self.fig

    def isPause(self, pause):
        ''' Sets the pause value: True/False '''
        
        self.pause = pause

    def frame_passed(self):
        ''' Called upon every iteration, and calls the plot axs methods, as well as returns the plots objects '''
        
        self.plotThirdAxs()
        
        if not self.pause: #If pause is true, pause!
            self.frame_counter += 1
            self.plotFourthAxs()

        return self.plot_neutrons, self.plot_fuel, self.plot_rods #Returns all plot obejcts
        

        
