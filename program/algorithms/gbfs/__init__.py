from queue import PriorityQueue
from haversine import haversine, Unit
from ...graph.impl import IVertex

def gbfs(start: IVertex, goal: IVertex, unit: Unit):
    frontier: PriorityQueue[tuple[int, IVertex]] = PriorityQueue()
    frontier.put((0, start))
    

    explored: set[IVertex] = set()
    edges_evaluated = 0
    path_cost = 0
    parent_map: dict[IVertex, IVertex] = {}

    while not frontier.empty():
        current = frontier.get()[1]

        if current == goal:
            path = []

            for vertice in parent_map:
                path.append(vertice.get_name())
                
            path.reverse()
            return {
                "path": path,
                "vertices_explored": len(explored),
                "edges_evaluated": edges_evaluated,
                "final_path_cost": path_cost
            }

        explored.add(current)

        for edge in current.get_edges():
            edges_evaluated += 1
            neighbor = edge.get_destination()

            if neighbor not in explored:
                neighbor_coords = neighbor.get_cords()
                goal_coords = goal.get_cords()

                heuristic = haversine(neighbor_coords, goal_coords, unit=unit)
                frontier.put((heuristic, neighbor))
                parent_map[neighbor] = current

                path_cost += edge.get_weight()
    return {
        "path": None,
        "vertices_explored": len(explored),
        "edges_evaluated": edges_evaluated,
        "final_path_cost": None
    }