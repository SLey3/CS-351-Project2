from queue import PriorityQueue
from haversine import haversine, Unit
from ...graph.impl import IVertex

def astar(start: IVertex, goal: IVertex, unit: Unit):
    frontier: PriorityQueue[tuple[float, int, IVertex]] = PriorityQueue()
    
    i = 0
    explored: set[IVertex] = set()
    edges_evaluated = 0
    path_costs: dict[IVertex, float] = {start: 0.0}
    parent: dict[IVertex, IVertex] = {}
    h: dict[IVertex, float] = {}
    f: dict[IVertex, float] = {}
    
    
    start_cords = start.get_cords()
    goal_cords = goal.get_cords()
    h[start] = haversine(start_cords, goal_cords, unit=unit)
    f[start] = path_costs[start] + h[start]
    
    frontier.put((f[start], i, start))
    
    while not frontier.empty():
        current = frontier.get()[2]
        
        if current == goal:
            path = []

            for vertice in parent:
                path.append(vertice.get_name())
                
            path.reverse()
            return {
                "path": path,
                "vertices_explored": len(explored),
                "edges_evaluated": edges_evaluated,
                "final_path_cost": path_costs[goal]
            }
        
        explored.add(current)
        
        for edge in current.get_edges():
            edges_evaluated += 1
            neighbor = edge.get_destination()
            
            tentative_g = path_costs[current] + edge.get_weight()
            
            if not any(neighbor == item[1] for item in frontier.queue) or tentative_g < path_costs.get(neighbor, 0):
                path_costs[neighbor] = tentative_g
                
                neighbor_cords = neighbor.get_cords()
                goal_cords = goal.get_cords()
                heuristic = haversine(neighbor_cords, goal_cords, unit=unit)
                h[current] = heuristic
                
                f[neighbor] = path_costs[neighbor] + h.get(neighbor, 0.0)
                parent[neighbor] = current
                
                i += 1
                frontier.put((f[neighbor], i,  neighbor))
                
    return {
    "path": None,
    "vertices_explored": len(explored),
    "edges_evaluated": edges_evaluated,
    "final_path_cost": None
}
    