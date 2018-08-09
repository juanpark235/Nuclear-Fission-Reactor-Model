'''
AUTHOR: OMER HEN
PURPOSE: class: Reactor for my Hemda Final Project 2017-2018: Nuclear Fission Reactor

This is the main class of this application where the user can define a large scale of parameters according to his/her experiment.
This class also utilizes both of the Particles and Display classes.

Changeable parameters: all such parameters are defined in capital letters before the declartion of the Reactor class.

BOUNDS =               Bounds of the simulation, doesn't have to be a square, but it is more convenient if it is.
SIZE =                 Physical size representation of the particles on the monitor will be according to this parameter, set to 1 / 2 for best view. 
FUEL_PERCENT =         Percent of fuel particles out of the totall area (not volume, since it is only in 2D) of the core, set to 10 / 15 / 20 to normal amount of fuel particles
USE_FUEL =             If true, fuel particle will be spent once a neutron collided into them, if False: reusable fuel, unlimited supply.
POWER_DESIRED:         A power value to be achieved and preserved by the reactor. Set to <= 100 for best and realistic performance
RODS_NUM:              A number by which increaments/decrements of rods are made. Set to <= 150 for best performance.
DX  =                  Distance that neutrons travel each iteration
NSTART =               Number of initial neutron to be injected into the simulation to start the chain reaction. The higher this value is, the faster the chain reaction will start
TOUCH_DISTANCE =       Distance in which particles are able to interact with one another. 

Also includes a pause feature, in which the user can click on the screen of the simulation and pause it for unlimited time, then click on the screen again
to continue the simulation
'''

import Particles_lib  #Imports the Particles class 
import Display_lib    #Imports the Display class
import Data_lib

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random

### USER DEFINED PARAMETERS ###

BOUNDS = [-50,50,-50,50]
SIZE = 1
FUEL_PERCENT = 15
USE_FUEL = False
POWER_DESIRED = 100
RODS_NUM = 250
DX = 0.5
NSTART = 100
TOUCH_DISTANCE = 0.075

###############################

class Reactor:
    pause = False #If true, the simulation will pause
    
    f_length = NSTART         #Number of neutrons in the system in the former iteration
    k = 1                     #K variable

    dtime = 0                 #Counts iterations/ticks/frames
    
    power = 0                 #Current power output
    old_power = [0,0,0,0,0]   #Saves the power output of five former iteration
    power_change = 0          #Power change since last iteration
    average_power = 0         #Power average -- calculated using the values from "old_power"
    power_list = []           #A list that contains all of the power outputs 


    def __init__(self):
        '''Constractor: sets up the simulation by defining objects from other classe and calling the setup methods '''
        
        self.display = Display_lib.Display(BOUNDS,SIZE,POWER_DESIRED) #Display object
        self.fig = self.display.getFigure()
        self.fig.canvas.mpl_connect('button_press_event', self.onClick) 
    
        self.neutrons = Particles_lib.Neutron(SIZE,BOUNDS,NSTART,DX)             #Neutron object
        self.fuel = Particles_lib.Fuel(SIZE,BOUNDS,FUEL_PERCENT,TOUCH_DISTANCE)  #Fuel object
        self.rods = Particles_lib.Rod(SIZE,BOUNDS,RODS_NUM)                      #Rods object

        self.data = Data_lib.Data() #Data object

        self.neutrons.setup() #Settings up the first initial neutrons
        self.fuel.setup()     #Settings up the first initial fuel particles  

        self.neutron_list = self.neutrons.getParticles() #Getting Neutron()'s array
        self.fuel_list = self.fuel.getParticles()        #Getting Fuel()'s array
        self.rods_list = self.rods.getParticles()        #Getting Rod()'s array

        
        

    def auto_react(self):
        ''' Defines the authomatic system by which the reactor works to maintain a certain power level '''

        if (self.power_change >= 0):
            if (POWER_DESIRED <= self.power):
                self.rods.addRods(self.fuel)
        else:
            if (self.power < POWER_DESIRED):
                self.rods.removeRods()
    
        self.rods_list = self.rods.getParticles() #Updates the rods list for possible new/removed rods
        self.step()

    def step(self):
        ''' Performed the step done in each iteration by every neutron '''

        self.power = 0
        dead_neutrons = []
        self.f_length = self.neutrons.getLength()
        
        for neutron in range(self.neutrons.getLength()):
            if not self.pause: 
                self.neutron_list[neutron] = self.neutrons.incrementStep(self.neutron_list[neutron]) #The neutron has moved forward from his former position
                dead = False
                
                particle = self.neutron_list[neutron]
                x_pos = particle[0]
                y_pos = particle[1]

                if not(self.neutrons.applyBounds(particle)): #Checks for bounds 
                    dead_neutrons.append(particle) #If outside of bounds, add to dead_neutrons
                    dead = True

                for rod in self.rods_list:
                    if (TOUCH_DISTANCE >= (rod[0]-x_pos)**2 + (rod[1]-y_pos)**2): #Checks for possible hit with a rod
                        dead_neutrons.append(particle) #If collided with a rod, add to dead_neutrons 
                        dead = True
                        break

                if (dead): #If dead by this point, continue to the next neutron 
                    continue 

                for particle in self.fuel_list: #If not dead, check for collision with a fuel particle
                    if (TOUCH_DISTANCE >= (particle[0]-x_pos)**2 + (particle[1]-y_pos)**2):
                        self.collision(neutron)
                        break
        
        if not self.pause:
            self.modifyPower() #Call modifyPower() after all neutrons were iterated and accounted for
            self.k = self.neutrons.getLength() / self.f_length #New k value for this iteration
        
        self.display.plotPower(self.power,self.power_change,self.k) #Sends the current power output, power change, and k value to be displayed

        self.neutrons.removeParticles(dead_neutrons) #Removes all the dead neutrons -- using the removeParticles() method
        self.neutron_list = self.neutrons.getParticles() #Updates the neutrons list after dead neutrons were remoed 
        
        
    def collision(self, index):
        ''' This method is called upon in case a neutron collided with a fuel particle '''

        if (USE_FUEL): #If USE_FUEL is true, remove the fuel particle
            self.fuel.removeParticle(self.neutron_list[index])
            self.fuel_list = self.fuel.getParticles()

        new_neutrons = random.uniform(1,3) #Randomly generate a value 

        '''
        
        It is curcial to mention that in order to get the real number of the newly generated neutrons, the the new_neutrons variable
        should be incremented by 1, due to the fact that the neutron that was used to induce the fission is still alive, and is used as it was just produced, see comments below. 
        '''
        
        if (new_neutrons < 1.5):
            new_neutrons = 0 #Plus the neutron that induced the fission
        elif ((1.5 <= new_neutrons) and (new_neutrons <= 2.5)):
            new_neutrons = 1 #Plus the neutron that induced the fission
        else:
            new_neutrons = 2 #Plus the neutron that induced the fission

        self.neutron_list[index][2] = random.randint(0,360) #Giving the neutron that was used to induce the fission a new angle, like it is a new neutron
        self.neutron_list[index] = self.neutrons.incrementStep(self.neutron_list[index]) 
        
        self.neutrons.spawnParticles(new_neutrons,[self.neutron_list[index][0],self.neutron_list[index][1]]) #Spawns new neutrons 

        '''
        Since this is a closed system and the model ignores the mass of atoms and neutrons, veloicty of neutrons, temperature and pressure of the core,
        the power output of each individual fission reaction can be defined by the user. Set to about 10 for best performance.
        '''
    
        self.power += 10 #Can be changed by the user

    def modifyPower(self):
        ''' Modifies the power variables and keeps them up to date with the current iteration '''
        
        self.power_change = self.power - self.old_power[len(self.old_power)-1]
        self.old_power.pop(0)
        self.old_power.append(self.power)
        self.average_power = sum(self.old_power) / len(self.old_power)
        self.power_list.append(self.average_power)

    def onClick(self,event):
        ''' Called upon when the user clicks the screen, and changes the boolean value of self.pause '''
        
        self.pause ^= True
        
    def animate(self,dt):
        ''' Called upon every iteration and updates the information on all sectors to be displayed in the monitor '''

        if not self.pause:
            self.dtime +=1
            
            if (self.dtime % 5 == 0): #Average is ploted every five iteration as it is the average of five former power outputs
                self.display.plotSecondAxs(self.power_list)

            self.data.update_k_factor(self.k)

        self.auto_react()

        self.display.isPause(self.pause) #Passes the self.pause value to the Display class
        
        self.display.plotNeutrons(self.neutrons.getXPositions(),self.neutrons.getYPositions()) #Plots the fuel, neutrons and rods
        self.display.plotFuel(self.fuel.getXPositions(),self.fuel.getYPositions())
        self.display.plotRods(self.rods.getXPositions(),self.rods.getYPositions())

        return self.display.frame_passed() #Matplotlib.animation requires that the animate class will return plot objectives, and it does from the frame_passed() method


if __name__ == "__main__":
    reactor = Reactor()
    ani = animation.FuncAnimation(reactor.fig,reactor.animate,interval = 30, repeat = True)
    plt.show()
