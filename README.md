# AI-Hueristic-Search
This project involves the implementation of Hueristic Search, through a machine and its ability to efficiently gather materials from any given map within a time limit.

Note: this project was a collaborative project for an AI Course in 2015 with another programmer, Denise Lau.

### The Map:
A map is a complete graph, so the machine can get from any distinct station to another distinct station in one action. In addition, the time it takes to get from one station to another is not necessarily the same as the time it takes to go back (perhaps the area is mountainous, or slippery). 
Each node is a station or a depot:<br/>
● A station is a place where our machine can harvest materials (an ore, for example). A station’s value represents how much material can be harvested from that station. Once it runs out of material, it does not refill. In addition should a machine harvest material from station that has less than the Harvest Rate, the machine extracts the remaining ore.<br/>
● Every map has at least one depot. A depot is a place where our machine can refill on fuel and drop off any materials it has harvested.

### The Machine:
The machine is defined by the following features:
<br/>● Fuel: Traveling between points on the map consumes fuel. The machine can only hold so much fuel and must refuel at depots. In our example, it would take 7 time units to go from Station 0 to the depot and 6 time units to go from the depot to Station 0.
<br/>● Harvest: The machine can only hold a certain amount of material and must drop off material at depots if it harvests its maximum carry amount. 
<br/>● Harvest Rate: The machine harvests material at a certain rate. In one time unit, the machine can harvest its rate in materials.
<br/>● Location: The nodes on the map represent where the machine can be located in any state. The robot cannot stop in between nodes.
<br/>*Note that the machine automatically refuels and drops off its harvest when it travels to a depot. This does not take time and is therefore not considered an action. Harvested material must also be dropped off at a depot for it to count towards the total harvest amount. Materials still on the robot after time runs out are discarded.*

### Heuristic Search:
Using search to solve this problem was due to the fact that there are many ways to harvest the materials on a map, but the order in which we harvest can greatly affect the total material gathered. Search allows us to explore the many ways in which the machine can utilize its two possible actions: harvest or travel.
The goal of our search is to find the most efficient way to extract an amount of equal or greater the minimum desired amount of resources in as little time as possible. This implementation can be used in the  real world example of a community of farmers needing to harvest and bring to market a certain number of crops, with each station a farm containing crops and depots functioning as markets, but are only able to afford 1 machine. Thus, using the algorithm, farmers will be able to efficiently use the machine to harvest and sell their crop in the shortest amount of time.

### Discussion and Conclusion: 
If we had more time to further expand on this project, we would have put in more features that could be considered both realistic and useful. The first would be the inclusion of multiple machines, so that resources could be extracted in parallel, but could not drill in the same location. Another would be that the expenditure of fuel could become an additional constraint, forcing the machine to make more energy efficient decisions.  
What we found most difficult about this assignment was finding an admissible heuristic for A* Search, with the aim to drill and deliver at least given amount of resources in as short as possible. Thus, finding the estimated cost of achieving the end goal, without overestimating it, is difficult for at any given state, we need to find the shortest estimated time between a location to drill and a depot, in addition to the time to drill the remaining amount. 
