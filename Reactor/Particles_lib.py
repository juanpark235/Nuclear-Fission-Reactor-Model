'''
AUTHOR: OMER HEN
PURPOSE: class: Particles for my Hemda Final Project 2017-2018: Nuclear Fission Reactor

This class handles all the different kinds of "particles" in the system:
- Fuel particles (Uranium)
- Neutrons
- Rods (Br, etc.)

All subclass: Fuel, Neutron, Rod, inherit from the superclass: Particles basic and elemantry methods
as they are generally used in all three classes. 

'''

import random
import math

class Particles:
    ''' Super Class --> defines essential methods for spesfic classes to inherit '''
    
    def __init__(self,size,bounds,length):
        ''' Constractor:
            size = size of particles on the monitor (related to the graphics of the simulation)
            bounds = bounds of the core, everything happens within the bounds
            length = number of particles desired. Generates "length" number of particles into the system.
        '''
        self.array = []
        self.size = size
        self.bounds = bounds
        self.length = length

    def getParticles(self):
        ''' Returns the particles array
        Fuel: [ [x,y] <-- one fuel particle ]
        Rod: [ [x,y] <-- one rod ]
        Neuton: [ [x,y,angle] <-- one neutron particle ]
        '''
        return self.array

    def setParticles(self,array):
        ''' Sets the particles array -> Receives information from Reactor() '''
        self.array = array

    def getLength(self):
        ''' Returns the length of the particles array: returns the number of particles '''
        return len(self.array)

    def getXPositions(self):
        ''' Returns an array with the x positions of all particles '''
        return [particle[0] for particle in self.array]

    def getYPositions(self):
        ''' Returns an array with the y positions of all particles '''
        return [particle[1] for particle in self.array]

    def printParticles(self):
        ''' Prints the array to the console --> this is used to debugging ''' 
        print(self.array)



class Fuel(Particles):
    ''' Subclass: Fuel, inherits from Particles and handles the fuel particles ''' 
    
    def __init__(self,size,bounds,particle_percent,touch_distance):
        ''' Constractor:
            particle_percent: same function as "length" in the Particles constractor
            touch_distance: distance in which the particles are able to interact with one another
        '''
        fuel_length = int((bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) * (particle_percent / 100)) #Calculates the number of fuel particles according to the particle_percent, or the percent of fuel particles desired
        super().__init__(size,bounds,fuel_length) #Passes appropriate variables back to the super constractor
        self.touch_distance = touch_distance

    def setup(self):
        ''' Sets up the fuel particles randomly within the bounds '''
        for particle in range(self.length):
            x = random.randint(self.bounds[0] + self.size,  #bounds[0] = left boundary of the core
                               self.bounds[1] - self.size)  #bounds[1] = right boundary of the core
            y = random.randint(self.bounds[2] + self.size,  #bounds[2] = bottom boundary of the core
                               self.bounds[3] - self.size)  #bounds[3] = top boundary of the core
            self.array.append([x,y])


    def removeParticle(self,particle):
        ''' Removes a spesific particle from the fuel particles array --> mostly after collision with a neutron '''
        x_pos = particle[0]
        y_pos = particle[1]
        
        for particle in self.array:
            if (self.touch_distance >= (particle[0]-x_pos)**2 + (particle[1]-y_pos)**2):
                self.array.remove(particle)
                break
    

class Neutron(Particles):
    ''' Subclass: Neutron, inherits from Particles and handles the neutron particles ''' 
    
    def __init__(self,size,bounds,startNumber,dx):
        ''' Constractor:
            startNumber: same function as "length" in the Particles constractor
            dx = distance that neutrons move in one iterration
        '''
        super().__init__(size,bounds,startNumber) #Passes appropriate variables back to the super constractor
        self.dx = dx
        
    def incrementStep(self,particle):
        ''' Moves a neutron one step forward according to self.dx --> called upon every iterration '''
        
        x_pos = particle[0]
        y_pos = particle[1]
        angle = particle[2]

        x = self.dx * math.sin(angle) #Distance passed in x grid
        y = self.dx * math.cos(angle) #Distance passed in y grid

        return [x_pos + x, y_pos + y, particle[2]] #Angle stays the same
    
    def applyBounds(self,particle):
        ''' Returns True: if a particle in within the bounds, returns False: if particle is not within the bounds '''
        
        x_pos = particle[0]
        y_pos = particle[1]

        if (x_pos < self.bounds[0] + self.size or
            x_pos > self.bounds[1] - self.size or
            y_pos < self.bounds[2] + self.size or
            y_pos > self.bounds[3] - self.size):
            return False
        return True

    def spawnParticles(self,particle_number,origins):
        ''' Generates neutrons according to an origins location and an amount: particle_number '''
        
        x_pos = origins[0] #X position started
        y_pos = origins[1] #Y position started
        
        for particle in range(particle_number): #Generates "particle_number" neutrons
            angle = random.randint(0,360)
            neutron = self.incrementStep([x_pos,y_pos,angle])
            self.array.append(neutron)

    def removeParticles(self,dead_neutrons):
        ''' Removes all neutrons that are in "dead_neutrons" array from the Neutron particles array '''
        
        self.array = [neutron for neutron in self.array if not(neutron in dead_neutrons)] 
        
    def setup(self):
        ''' Injects the system with the intiall neutron to start the chain reaction '''
        
        for particle in range(self.length):
            x = random.randint(self.bounds[0]/2 , self.bounds[1]/2) #x position is centered in the middle of the core, so that the neutron won't escape from the core too quickly
            y = random.randint(self.bounds[2]/2 , self.bounds[3]/2) #y position is centered in the middle of the core, so that the neutron won't escape from the core too quickly
            angle = random.randint(0,360)
            self.array.append([x,y,angle])



class Rod(Particles):
    ''' Subclass: Rod, inherits from Particles and handles the rods ''' 

    def __init__(self,size,bounds,rods_number):
        ''' Constractor:
            rods_number: a constant number to add and remove rods. Always increases and decreases the amount of rods in the system by this value
        '''
        super().__init__(size,bounds,rods_number) #Passes appropriate variables back to the super constractor
        self.rods_number = rods_number

    def addRods(self,fuel):
        ''' Inserting rods to the system according to self.rods_number '''
        
        fuel_list = fuel.getParticles()
        
        for particle in range(self.rods_number):
            placed = False #Will be true once the rod was successfully placed in the core

            while not(placed):
                x = random.randint(self.bounds[0]+self.size,self.bounds[1]-self.size)
                y = random.randint(self.bounds[2]+self.size,self.bounds[3]-self.size)

                if not([x,y] in fuel_list):
                    self.array.append([x,y])
                    placed = True

    def removeRods(self):
        ''' Removes rods from the system according to self.rods_number '''
        
        if (self.getLength() > self.rods_number): #Checks that they are indeed enough rods to be removed --> error handling
            for particle in range(self.rods_number):
                self.array.pop(random.randint(0,self.getLength()-1)) #Removes a random rod from the system
