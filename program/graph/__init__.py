from typing import List, Optional, Union
from .impl import IEdge, IGraph, IVertex
from itertools import chain

# Implementation definitions
class Graph(IGraph):    
    def __init__(self):
        self._vertices: List[IVertex] = []
        
    def get_vertices(self) -> List[IVertex]:
        return self._vertices
    
    def get_edges(self) -> List[IEdge]:
        return list(chain.from_iterable(x.get_edges() for x in self._vertices))
    
    def add_vertex(self, vertex: IVertex) -> None: 
        self._vertices.append(vertex)
        
    def remove_vertex(self, vertex_name: str) -> None:
        vertex_to_remove = next((vertex for vertex in self._vertices if vertex.get_name() == vertex_name), None)
        
        if vertex_to_remove:
            self._vertices.remove(vertex_to_remove)
        else:
            raise IndexError(f'{vertex_name} is not a valid vertex')
        
    def add_edge(self, edge: IEdge) -> None:
        destination = edge.get_destination()
        
        if destination is None:
            return
        
        vertex_i = self._vertices.index(destination)
        vertex = self._vertices[vertex_i]
        
        vertex.add_edge(edge)
        
    def remove_edge(self, edge_name: str) -> None:
        for vertex in self._vertices:
            # check ever edge in the current vertex if the edge name matches the edge to remove
            edge_match = list(filter(lambda x: x.get_name() == edge_name, vertex.get_edges())) != []
            
            if edge_match:
                vertex.remove_edge(edge_name)
                break
            

class Vertex(IVertex):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name or ""
        self._edges: List[IEdge] = []
        self.visited = False
        self.lat = 0.0
        self.long = 0.0
        
    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name: str) -> None:
        self.name = name
        
    def add_edge(self, edge: IEdge) -> None:
        self._edges.append(edge)
    
    def remove_edge(self, edge_name: str) -> None:
        edge_to_remove = next((edge for edge in self._edges if edge.get_name() == edge_name), None)
        if edge_to_remove:
            self._edges.remove(edge_to_remove)
        else:
            raise IndexError(f'{edge_name} is not a valid edge')
        
    def get_edges(self) -> List[IEdge]:
        return self._edges
    
    def add_cords(self, lat: float, long: float) -> None:
        self.lat = lat
        self.long = long
        
    def get_cords(self) -> tuple[float, float]:
        return (self.lat, self.long,)
    
    def remove_cords(self) -> None:
        self.lat = 0.0
        self.long = 0.0
    
    def set_visited(self, visited: bool) -> None:
        self.visited = visited
        
    @property
    def is_visited(self) -> bool:
        return self.visited
    
    def __str__(self):
        return f"<Vertex name={self.name}>"
    def __repr__(self):
        return f"<Vertex name={self.name}>"
    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, IVertex):
            return (
                self.name == obj.get_name() and
                self._edges == obj.get_edges() and
                self.get_cords() == obj.get_cords() and
                self.visited == obj.is_visited
            )
            
        return False
    def __hash__(self) -> int:
        return hash(self.name)

class Edge(IEdge):
    def __init__(self):
        self.name = ""
        self.weight = 0.0
        self.destination = Vertex()
        
    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name: str) -> None:
        self.name = name
        
    def set_destination(self, dest: IVertex) -> None:
        self.destination = dest
        
    def get_destination(self) -> IVertex:
        return self.destination
    
    def get_weight(self) -> float:
        return self.weight
    
    def set_weight(self, weight: float) -> None:
        self.weight = weight
        
    def __str__(self):
        return f"<Edge name={self.name} weight={self.weight} destination={repr(self.destination)}>"
    def __repr__(self):
        return f"<Edge name={self.name} weight={self.weight} destination={repr(self.destination)}>"
        