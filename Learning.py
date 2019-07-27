class Node:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]

class Edge:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

class WireFrame:
    def __init__(self):
        self.nodes = []
        self.edges = []
    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(Node(node))
    def addEdges(self, edgeList):
        for (start, stop) in edgeList:
            self.edges.append(Edge(self.nodes[start],self.nodes[stop]))
    def outputNodes(self):
        for node in self.nodes:
            print(node)
    
cube_nodes = [(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)]
cube = WireFrame()
cube.addNodes(cube_nodes)
cube.outputNodes()