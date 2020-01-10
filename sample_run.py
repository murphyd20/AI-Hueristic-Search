
from resources import *
if __name__ == '__main__':
    stationList = []
    stationList.append(Location("Station 0", 0, 12))
    stationList.append(Location("Station 1", 0, 15))
    stationList.append(Location("Depot 0", 1))
    
    DictLocation = {}
    DictLocation["Station 0,Station 1"] = 8
    DictLocation["Station 0,Depot 0"] = 7
    DictLocation["Station 1,Station 0"] = 8
    DictLocation["Station 1,Depot 0"] = 14
    DictLocation["Depot 0,Station 0"] = 6
    DictLocation["Depot 0,Station 1"] = 17
    
    machine = Machine(20, 20, 10, 0, 4, stationList[2])
    
    s = make_init_state(machine, stationList, 10, DictLocation)

    
    se = SearchEngine('astar', 'full')
    se.search(s, resources_goal_fn, heur_min_completion_time)
    se.set_strategy('best_first')
    se.search(s, resources_goal_fn)
