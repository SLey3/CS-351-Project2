from queue import PriorityQueue
from haversine import haversine, Unit
from ...graph.impl import IVertex

def dijkstra(start: IVertex, goal: IVertex, unit: Unit):
    frontier: PriorityQueue[tuple[float, IVertex]] = PriorityQueue()
    frontier.put((0, start))
    
    explored: set[IVertex] = set()
    edges_evaluated = 0
    path_costs: dict[IVertex, float] = {start: 0.0}
    parent: dict[IVertex, IVertex] = {}
    
    while not frontier.empty():
        current = frontier.get()[1]
        
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
            
            if neighbor not in explored:
                if not any(neighbor == item[1] for item in frontier.queue) or tentative_g < path_costs.get(neighbor, 0):
                    path_costs[neighbor] = tentative_g
                    parent[neighbor] = current
                    
                    neighbor_cords = neighbor.get_cords()
                    goal_cords = goal.get_cords()
                    heuristic = haversine(neighbor_cords, goal_cords, unit=unit)
                    
                    frontier.put((heuristic, neighbor))
        
    return {
    "path": None,
    "vertices_explored": len(explored),
    "edges_evaluated": edges_evaluated,
    "final_path_cost": None
}
