from .algorithms import astar, dijkstra, gbfs
from .graph import Graph, Vertex, Edge
from .graph import IVertex
from haversine import Unit
from pathlib import Path
from typing import Optional, Callable, Any
from time import perf_counter, sleep

import pandas as pd
import click
import string


# basic vars
path = Path(__file__).parent

# timer
def time_algorithm(algo: Callable[[IVertex, IVertex, Unit], dict[str, Any]], start_vert: IVertex, dest_vert: IVertex, unit: Unit) -> tuple[float, dict[str, Any]]:
    start = perf_counter()
    result = algo(start_vert, dest_vert, unit)

    return (perf_counter() - start, result,)

# parser
def parse_graph():
    graph_df = pd.read_csv(
        path / "data" / "graph_v2.txt",
        dtype={"source": str, "destination": str, "highway": str, "distance": int}
    )
    vertices_df = pd.read_csv(
        path / "data" / "vertices_v1.txt",
        dtype={"name": str, "latitude": float, "longitude": float}
    )
    
    graph = Graph()
    vertices: dict[str, Vertex] = {}

    def ensure_vertex(name: str) -> Vertex:
        if name not in vertices:
            v = Vertex(name)
            vertices[name] = v
            filtered_vertices = vertices_df[vertices_df['vertex'] == name]

            if filtered_vertices.empty:
                raise ValueError(f"Vertex '{name}' not found in the vertices data.")

            vertex_cords = filtered_vertices[['latitude', 'longitude']].iloc[0]
            v.add_cords(vertex_cords['latitude'], vertex_cords['longitude'])
            graph.add_vertex(v)
        return vertices[name]
    
    for _, row in graph_df.iterrows():
        src_name = row['source'].strip()
        dst_name = row['destination'].strip()
        hwy = row['highway'].strip()
        distance = row['distance']
        
        if src_name == "" or dst_name == "":
            continue
        
        src_v = ensure_vertex(src_name)
        dst_v = ensure_vertex(dst_name)
        
        edge = Edge()
        edge.set_name(hwy)
        edge.set_weight(distance)
        edge.set_destination(dst_v)
        src_v.add_edge(edge)
    return (graph, vertices_df)    

@click.command()
def main():
    # parse graph
    graph, vertex_df = parse_graph()
    
    run = True
    
    while run:
        # user inputs
        start_loc = input("Start Location: ").strip()
        check = start_loc in vertex_df['vertex'].values
        
        if not check:
            while check not in vertex_df['vertex'].values:
                print("Not a Valid Location. Try again")
                check = start_loc = input("Start Location: ")

        dest_loc = input("Destination Location: ").strip()
        check = dest_loc in vertex_df['vertex'].values
        
        if not check:
            while check not in vertex_df['vertex'].values:
                print("Not a Valid Location. Try again")
                check = dest_loc = input("Destination Location: ")
        
        # ask for a unit
        print("Choose a unit for heuristic distance measurement:")
        print("1) KILOMETERS")
        print("2) MILES")
        print("3) NAUTICAL_MILES")
        
        unit_map = {
            1 : Unit.KILOMETERS,
            2 : Unit.MILES,
            3 : Unit.NAUTICAL_MILES
        }
        
        unit_choice = input("Enter the number corresponding to your choice: ").strip()
            
        while unit_choice not in unit_map:
            if not str(unit_choice) in string.printable[0:10] or len(str(unit_choice)) != 1:
                print("Choice cannot be any letters or special characters nor be greater than or less than the length of 1\n\n")
            
            if int(unit_choice) in unit_map:
                unit_choice = int(unit_choice)
                continue
            else:
                print("Invalid choice. Please try again.")
                
            unit_choice = input("Enter the number corresponding to your choice: ")
        
        chosen_unit = unit_map[unit_choice]
        
        # ask for the algorithm
        print("Choose an algorithm to run the analysis:")
        print("1) astar (A*)")
        print("2) gbfs (Greedy Best First Search)")
        print("3) dijkstra")
        
        algo_map = {
            1 : "astar",
            2 : "gbfs",
            3 : "dijkstra"
        }
        
        algo_choice = input("Enter the number corresponding to your choice: ").strip()
        
        while algo_choice not in algo_map:
            if not str(algo_choice) in string.printable[0:10] or len(str(algo_choice)) != 1:
                print("Choice cannot be any letters or special characters nor be greater than or less than the length of 1\n\n")
            
            if int(algo_choice) in algo_map:
                algo_choice = int(algo_choice)
                continue
            else:
                print("Invalid choice. Please try again.")
                
            algo_choice = input("Enter the number corresponding to your choice: ").strip()
        
        chosen_algo = algo_map[algo_choice]
        
        # get and check the vectors
        
        start_vertex: Optional[IVertex] = next((v for v in graph.get_vertices() if v.get_name() == start_loc), None)
        dest_vertex: Optional[IVertex] = next((v for v in graph.get_vertices() if v.get_name() == dest_loc), None)
        
        if start_vertex is None or dest_vertex is None:
            print("either start or destination location does not exist")
            return
        
        # run the chosen algorithm
        match chosen_algo:
            case "astar":
                time_executed, result = time_algorithm(astar, start_vertex, dest_vertex, chosen_unit)
            case "gbfs":
                time_executed, result = time_algorithm(gbfs, start_vertex, dest_vertex, chosen_unit)
            case "dijkstra":
                time_executed, result = time_algorithm(dijkstra, start_vertex, dest_vertex, chosen_unit)
            case _:
                time_executed = result = None
        
        # print out results
        print("Results: ")
        
        if (
            result is None or 
            result.get("path") is None or 
            result.get("final_path_cost") is None
            or time_executed is None
        ):
            print(f"{chosen_algo} algorithm failed to correctly perform the graph search")
            return
            
        print("Path from Start to Destination: ", result["path"])
        print("Total Vertices explored: ", result["vertices_explored"])
        print("Evaluated edges: ", result["edges_evaluated"])
        print("Final Path Distance: ", result["final_path_cost"])
        print("Execution time: ", time_executed)
        
        sleep(3)
        
        rerun_req = True
        
        while rerun_req:
            res = input("Want to run another query (y/n)? ").strip()
            
            match res.lower():
                case "y":
                    break
                case "n":
                    run = False
                    break
                case _:
                    print('Answer has to be either "y" or "n"')
        
        

if __name__ == '__main__':
    main()