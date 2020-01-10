
from search import *
from math import *
from random import randint

class Location:
    def __init__(self, name, DepotBool, value = 0):
        #name of location
        self.name = name

        #The value(or resources at a station)
        self.value = value

        ##if isDepot is true, it is a Depot Station
        ##else, isDepot is false, and is a Mining station
        self.isDepot = DepotBool

    def print_state(self):
        if(self.isDepot != True):
            print("Name = {}, value = {}, type = Mining Station".format(self.name, self.value))
        else:
            print("Name = {}, type = Depot Refinary".format(self.name))



    
def getDist(StartLocation,EndLocation,DictLocation):
    ''' Return the distance going from StartLocation to EndLocation using
    information stored in DictLocation'''
    s = StartLocation.name + "," + EndLocation.name
    return DictLocation[s]

class Machine():
    '''Class to keep information about a machine that harvests resources.'''
    
    def __init__(self, fuelCap, fuelRem, harvestCap, harvestCount, harvestRate, curLocation):
        '''
        int fuelCap (fuel capacity), fuelRem (fuel remaining)
        int harvestCap (harvest holding capacity)
        int harvestRate (rate at which the machine can harvest resources from any location)
        Location curLocation (this machine's current location)
        '''
        self.fuelCap = fuelCap
        self.fuelRem = fuelRem
        self.harvestCount = harvestCount
        self.harvestCap = harvestCap
        self.harvestRate = harvestRate
        self.curLocation = curLocation
    def print_state(self):
        print("Machine is at {}, {}/{} fuel remaining, {}/{} harvest capacity".format(self.curLocation.name, self.fuelRem, self.fuelCap, self.harvestCount, self.harvestCap))
        
class Resources(StateSpace):
    def __init__(self, action, gval, parent, machine, currentTime, harvestGoal, locations, locDic, totalHarvested = 0):
        '''Problem specific state space objects must always include the data items
           -actions = [harvest, travel, refill]
           -Machine machine
           -int currentTime
           -int totalHarvested, harvestGoal how much we have harvested and how much we need to be in a goal state
           -List<Location> station_list, depot_list
           -Dictionary<[Location1, Location2], int> locDic returns the time it takes to get from Location1 to Location2 given [Location1, Location2] as a key
           
        '''
        self.action = action
        self.gval = gval
        self.parent = parent
        self.index = StateSpace.n
        StateSpace.n = StateSpace.n + 1
        
        self.machine = machine
        self.locations = locations
        self.locDic = locDic
        self.currentTime = currentTime
        self.harvestGoal = harvestGoal
        self.totalHarvested = totalHarvested
        

    def successors(self):
        '''This method when invoked on a state space object must return a
           list of successor states, each with the data items "action"
           the action used to generate this successor state, "gval" the
           gval of self plus the cost of the action, and parent set to self.
           Also any problem specific data must be specified property.
           
           If a machine is at a mining area, it can either:
           => harvest: take 1 unit of time to harvest its harvest rate in materials
           => move to another location, taking getDist(StationA, StationB) units of time to complete the action.
           If the machine is at a depot, it can only
           => move to another location
           When a machine goes to a depot, it is assumed that its fuel is refilled and its harvest is dropped off. This does not take time. 
           
           If doing an action causes a machine to:
           => run out of fuel,
           => harvest when the machine cannot hold any more harvest,
           => run out of time,
           the state the action creates is not considered.
           '''
        
        States = []
        #Resource: action, gval, parent, machine, currentTime, totalHarvested, harvestGoal, locations, locDic
        #Machine: fuelCap, fuelRem, harvestCap, harvestCount, harvestRate, curLocation
     
        #if the machine is at a mining locatio, try to harvest
        # the most it can harvest is what remains at the location, or what the robot can harvest + carry
        if (not self.machine.curLocation.isDepot):
            harvest_allowed = min(self.machine.harvestRate, 
                                  min(self.machine.harvestCap - self.machine.harvestCount, self.machine.curLocation.value))

            newLocations = self.locations[:]
            newLocations.remove(self.machine.curLocation)
            DepletedLocation = Location(self.machine.curLocation.name,
                                        self.machine.curLocation.isDepot,
                                        self.machine.curLocation.value - harvest_allowed)
            newLocations.append(DepletedLocation)
            
            new_machine = Machine(self.machine.fuelCap, self.machine.fuelRem, 
                                  self.machine.harvestCap, 
                                  self.machine.harvestCount + harvest_allowed,
                                  self.machine.harvestRate, DepletedLocation)
            
            #(self, action, gval, parent, machine, currentTime, harvestGoal, locations, locDic, totalHarvested = 0)
            new_resource = Resources("harvest", self.gval + 1, self, new_machine,
                                     self.currentTime + 1,
                                     self.harvestGoal,  
                                     newLocations, 
                                     self.locDic,
                                     self.totalHarvested)
            # do not add state where robots harvests and gets nothing
            # do not add if state goes overtime
            if (harvest_allowed != 0):
                States.append(new_resource)
            
        # Move to a different location
        # if it moves to a depot, refill and drop off harvest automatically
        for location in self.locations:
            if (location != self.machine.curLocation):
                # if the new location is a depot, drop off harvest + update fuel
                distance = getDist(self.machine.curLocation, location, self.locDic)
                if location.isDepot:
                    fuelRem = self.machine.fuelCap
                    totalHarvest = self.totalHarvested + self.machine.harvestCount
                    harvestCount = 0
                # else the location is a mining point; deduct fuel
                else:
                    fuelRem = self.machine.fuelRem - distance
                    totalHarvest = self.totalHarvested
                    harvestCount = self.machine.harvestCount
                # make a new Machine
                new_machine = Machine(self.machine.fuelCap, 
                                      fuelRem, 
                                      self.machine.harvestCap, 
                                      harvestCount, 
                                      self.machine.harvestRate, location)
                
                # make a new Resource
                #(self, action, gval, parent, machine, currentTime, harvestGoal, locations, locDic, totalHarvested = 0)
                new_resource = Resources("move_location",
                                         self.gval + distance, 
                                         self,
                                         new_machine, 
                                         self.currentTime + distance,
                                         self.harvestGoal,
                                         self.locations, self.locDic, totalHarvest)
                # do not add the state if the machine runs out of fuel doing this move
                # do not add if the state goes overtime
                if (new_machine.fuelRem != 0):
                    States.append(new_resource)      
        return States
    def hashable_state(self):
        '''This method must return an immutable and unique representation
           of the state represented by self. The return value, e.g., a
           string or tuple, will be used by hashing routines. So if obj1 and
           obj2, both StateSpace objects then obj1.hashable_state() == obj2.hashable_state()
           if and only if obj1 and obj2 represent the same problem state.'''
        tuplemachine = (self.machine.fuelCap,
                        self.machine.fuelRem,
                        self.machine.harvestCount,
                        self.machine.harvestCap,
                        self.machine.harvestRate,
                        self.machine.curLocation.name)

        LocationList = []
        for j in self.locations:
            LocationList.append((j.name, j.value, j.isDepot))
        tupleLocations = tuple(LocationList)
            
        return(self.currentTime, self.totalHarvested, tuplemachine, tupleLocations)

    def print_state(self):
        '''Print a representation of the state'''
        if self.parent:
            print("Action = \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
        print("Time = {}, Total Harvested = {}, Harvest Goal = {}".format(self.currentTime, self.totalHarvested, self.harvestGoal))
        self.machine.print_state()
        
    def print_path(self):
        '''print the sequence of actions used to reach self'''
        #can be over ridden to print problem specific information
        s = self
        states = []
        while s:
            states.append(s)
            s = s.parent
        states.pop().print_state()
        while states:
            print(" ==> ", end="")
            states.pop().print_state()
        print("")
 
    def has_path_cycle(self):
        '''Returns true if self is equal to a prior state on its path'''
        s = self.parent
        hc = self.hashable_state()
        while s:
            if s.hashable_state() == hc:
                return True
            s = s.parent
        return False
def heur_min_completion_time(state):
    # if it already has enough harvest 
    if (state.machine.harvestCount + state.totalHarvested >= state.harvestGoal):
        # find nearest time to depot
        depots = []
        for location in state.locations:
            if location.isDepot and state.machine.curLocation != location:
                depots.append(getDist(state.machine.curLocation, location, state.locDic))
                #robot is at a depot
                if (location.name == state.machine.curLocation.name):
                    depots.append(0)
        if len(depots) == 0 and state.machine.curLocation != location:
            return 0
        return min(depots)
    
    # else what is the minimum time to harvest enough
    min_to_harvest = ceil((state.harvestGoal - state.totalHarvested)/state.machine.harvestRate)
    depots = []
    for location in state.locations:
        if location.isDepot and state.machine.curLocation != location:
            depots.append(getDist(state.machine.curLocation, location, state.locDic)) 
    stations = []    
    if (len(depots) == 0):
        for location in state.locations:
            if not location.isDepot:
                stations.append(getDist(location, state.machine.curLocation, state.locDic))
        return min(stations) + min_to_harvest
    return min(depots) + min_to_harvest
        
def resources_goal_fn(state):
    if(state.machine.curLocation.isDepot == 1 and state.harvestGoal <= state.totalHarvested):
            return True
    return False                        
                
def make_init_state(machine, locations, harvestGoal, locDic):
    #(self, action, gval, parent, machine, currentTime, harvestGoal, locations, locDic, totalHarvested = 0)
    return Resources("START", 0, None, machine, 0, harvestGoal, locations, locDic)

def make_rand_locations(nDepots, nMines, maxExtract, minExtract,maxDist):
    ''' For testing purposes; makes nDepots amount of depots, nMines amount of 
    mines, and allows range(minExtract, maxExtract) value and a distance between
    1 and maxDist.
    
    The keys of DictLocation are formatted as follows:
    "Station X,Station Y"
    >>>print(dict["Station 0,Station 1"])
    6 
    >>>print(dict["Station 1,Station 0"])
    The value is the distance from Station X to Station Y; the time it takes to go one way is not necessarily the same as the time it takes to go back.
    '''
    DictLocation = {}
    stationList = []
    for d in range(nDepots):
        s = "Depot " + str(d)
        stationList.append(Location(s,True))
    for m in range(nMines):
        s = "Station " + str(m)
        v = randint(minExtract,maxExtract)
        stationList.append(Location(s,False,v))
    DictLocation = {}
    for a in stationList:
        for b in stationList:
            s = a.name + "," + b.name
            if(a != b):
                DictLocation[s] = randint(2,maxDist)
    return DictLocation, stationList
