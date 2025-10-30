# CS-351-Project2

## Part A: Program Usage Instructions
The following contains instructions in installing the required 
packages and running the program using the CLI.

### Installation
run the following command to install the requirements:

```
pip install -r requirements.txt
```

### Running the Program
To start the program run:

```
python -m program
```

The program will ask for the start location and then the 
destination location. Since heuristic distance measurements are 
distance's there are units in which the function calculating the 
distance uses and so the program asks for the desired measurements 
from the following options (in order):

1) Kilometers (km)
2) Miles (mi)
3) Nautical Miles (nm)

Input the number associated with your preferred measurement.

Once you input that, the program in a similar manner will ask to choose the algorithm you want to run in the following options:

1) astar (A*)
2) gbfs (Greedy Best First Search)
3) dijkstra

Select your chosen algorithm and it will run the options you 
selected with the algorithm eventually returning a result in the 
following manner (with types):

```
Path from Start to Destination:  list[string]
Total Vertices explored:  integer
Evaluated edges:  integer
Final Path Distance:  integer
Execution time:  float
```

The program waits 3 seconds before asking if you want to run the program again and input either y or n.

## Algorithm Analysis
### Empirical Observations: Test Cases
Test Case will be performed in the following order:

1) Short Distance: Portland → Salem
2) Medium Distance: Portland → Eugene
3) Long Distance: Portland → Ashland
4) Diagonal Route: Portland → Burns
5) Coastal vs. Inland: Portland → Medford

We will explore in each case the vertices explored, distances calculated, execution time and determine
which of the three algorithms found the optimal path and explored the fewest vertices

The following general option after locations will be used:
Unit: Miles

#### Short Distance
* A* Algorithm
  - Vertices Explored: 1
  - Distance: 47 mi
  - Execution Time: 0.0006319590611383319
* Greedy Best-First Search Algorithm
  - Vertices Explored: 1
  - Distance: 322 mi
  - Execution Time: 0.0001968329306691885
* Dijkstra Algorithm:
  - Vertices Explored: 1
  - Distance: 47 mi
  - Execution Time: 0.00038595800288021564

#### Medium Distance
* A* Algorithm
  - Vertices Explored: 6
  - Distance: 129 mi
  - Execution Time: 0.00047204201109707355
* Greedy Best-First Search Algorithm
  - Vertices Explored: 2
  - Distance: 423 mi
  - Execution Time: 0.0002075409283861518
* Dijkstra Algorithm:
  - Vertices Explored: 2
  - Distance: 111 mi
  - Execution Time: 0.0003730419557541609

#### Long Distance
* A* Algorithm
  - Vertices Explored: 19
  - Distance: 329 mi
  - Execution Time: 0.0018431670032441616
* Greedy Best-First Search Algorithm
  - Vertices Explored: 6
  - Distance: 889 mi
  - Execution Time: 0.0002197920111939311
* Dijkstra Algorithm:
  - Vertices Explored: 6
  - Distance: 412 mi
  - Execution Time: 0.00024337496142834425

#### Diagonal Route
* A* Algorithm
  - Vertices Explored: 21
  - Distance: 351 mi
  - Execution Time: 0.0038559159729629755
* Greedy Best-First Search Algorithm
  - Vertices Explored: 6
  - Distance: 867 mi
  - Execution Time: 0.0002477500820532441
* Dijkstra Algorithm:
  - Vertices Explored: 6
  - Distance: 351 mi
  - Execution Time: 0.0005045420257374644

#### Coastal vs. Inland
* A* Algorithm
  - Vertices Explored: 18
  - Distance: 314 mi
  - Execution Time: 0.0009689999278634787
* Greedy Best-First Search Algorithm
  - Vertices Explored: 5
  - Distance: 799 mi
  - Execution Time: 0.0002477500820532441
* Dijkstra Algorithm:
  - Vertices Explored: 5
  - Distance: 397 mi
  - Execution Time: 0.000722041935659945

### Empirical Observations: Results
**Fewest Vertices:** Greedy Best-First Search consistently 
explored the fewest vertices across all test cases due to its 
heuristic-driven approach that greedily selects the most promising 
node.

**Optimal Path:** A* found the optimal path in all cases by 
combining actual cost (g) with heuristic estimation (h), ensuring 
both optimality and efficiency through its $f(n) = g(n) + h(n)$ 
evaluation function.

## Use Case Analysis

### Dijkstra's Superior Performance
**Dense urban networks:** In city grids with many intersections and alternative routes, Dijkstra's exhaustive exploration ensures the truly shortest path when heuristics may mislead.

**Uniform cost environments:** When edge weights are relatively 
similar (highways with consistent speed limits), Dijkstra's 
systematic approach becomes more competitive.

### Greedy Best-First Suboptimal Cases
**Obstacle avoidance:** When direct routes are blocked by 
geographic barriers, GBFS may choose longer detours by focusing 
solely on straight-line distance.

**Traffic considerations:** Real-world factors like congestion 
aren't captured in heuristic distance, leading to suboptimal route 
selection.

### A* Greatest Advantages
**Large-scale routing:** Cross-state or cross-country routes where 
A* balances exploration efficiency with optimality guarantees.

**Mixed terrain:** Complex topography where both actual distance 
and heuristic guidance are crucial for finding optimal paths.

### Real-World Application Selection
**Choose Dijkstra's** for mission-critical applications requiring 
guaranteed shortest paths regardless of computation time, such as 
emergency services or delivery optimization with strict cost 
constraints.

**Choose Greedy Best-First** for real-time applications 
prioritizing speed over optimality, like preliminary route 
suggestions or resource-constrained mobile devices.

**Choose A*** for general-purpose navigation systems where users 
expect both reasonable performance and optimal routes, making it 
ideal for consumer GPS applications and route planning services.

## Runtime Complexity Analysis
### Theoretical Complexity Analysis

**Time Complexity:**
- **Dijkstra's Algorithm:** $O(n \log n)$ using a priority queue
- **A\* Algorithm:** $O(n \log n)$ where n is the number of vertices
- **Greedy Best-First Search:** $O(n)$ where n is the number of vertices

**Space Complexity:**
- **Dijkstra's Algorithm:** $O(n)$ for distance array and priority queue
- **A\* Algorithm:** $O(n)$ for storing frontier nodes in practice  
- **Greedy Best-First Search:** $O(n)$ for frontier storage

### Performance Impact of Oregon Map Size
With |V| = 22 and |E| = 52, all algorithms perform efficiently due to the small graph size. The logarithmic factors in Dijkstra's and A* complexities (log 22 ≈ 4.46) provide minimal overhead. GBFS benefits most from the limited branching factor, while A* and Dijkstra's systematic approaches show similar performance on this scale.

### Scaling to Larger Maps
For a US highway system with ~170,000 intersections and ~240,000 road segments:
- **Dijkstra's:** Performance degrades significantly due to exhaustive exploration
- **A\*:** Maintains efficiency through heuristic guidance, scaling better than Dijkstra's
- **GBFS:** Fastest execution but optimality becomes increasingly compromised

### Optimality vs. Efficiency Trade-offs
A* provides optimal solutions with reasonable efficiency through heuristic guidance. Dijkstra's guarantees optimality but sacrifices speed through exhaustive search. GBFS maximizes speed but compromises path quality, potentially finding routes 2-3x longer than optimal. The choice depends on application requirements: mission-critical systems favor optimality (Dijkstra's/A*), while real-time applications prioritize speed (GBFS). A* represents the best balance for most practical navigation scenarios.

## Heuristic Discussion
**Haversine Distance Admissibility:** The Haversine distance is admissible for A* because it calculates the straight-line distance between two points on Earth's surface, which represents the theoretical minimum distance possible. Since roads cannot be shorter than this direct path, the heuristic never overestimates the actual cost, satisfying A*'s admissibility requirement and guaranteeing optimal solutions.

**Greedy Best-First with Heavy Underestimation:** When the heuristic severely underestimates, GBFS becomes increasingly suboptimal by selecting paths that appear promising locally but lead to globally poor solutions. Heavy underestimation reduces the heuristic's guidance effectiveness, causing GBFS to make poor directional choices and potentially explore dead ends.

**Improved Heuristic Design:** A better heuristic could incorporate road network topology and speed limits, estimating travel time rather than just distance. However, this increases computational complexity and storage requirements. For this problem.