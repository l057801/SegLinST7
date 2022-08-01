class LUCA():
    def __init__(self, ID: int, position: list):
        self.__id = ID
        self._type = None
        self.__connectedElements = {'nodes':{}, 'straightLines':{}, 'arcs':{}, 'shells':{}}
        self.__center = {'x': position[0], 'y': position[1], 'z': position[2], 'w': 1}
        self.__groups = []

    def ID(self) -> int:
        return self.__id

    def Type(self) -> str:
        return self._type

    def changeID(self, newID: int) -> None:
        self.__id = newID
    
    def position(self) -> dict:
        return self.__center

    def _addConnectedElement(self, ID: int, element, elementType: str) -> None:
        if ID not in self.__connectedElements[elementType] and elementType != self.Type():
            self.__connectedElements[elementType][ID] = element
        else:
            print(f'{elementType} {ID} already connected to {self.Type()} {self.ID()}')
    
    def _removeConnectedElement(self, ID: int, elementType: str) -> None:
        if ID not in self.__connectedElements[elementType]:
            print(f'{elementType} {ID} not connected to {self.Type()} {self.ID()}')
        else:
            del self.__connectedElements[elementType][ID]
    
    def printConnectedElements(self) -> None:
        print('\n' + f'{self.Type().capitalize()} {self.ID()}\n' + 25 * '-')
        for eleType, elements in self.__connectedElements.items():
            if eleType != self._type + 's':
                print(f'Connections to {eleType}:')
                for ID, con in elements.items():
                    print(f'\t--> {eleType[:-1]} {ID}')

    def listConnectedElements(self) -> dict:
        return self.__connectedElements


class Node(LUCA):
    def __init__(self, ID: int, position: list):
        super().__init__(ID, position)
        self._type = 'node'


class StraightLine(LUCA):
    def __init__(self, ID: int, startNode, endNode):
        position = self.__findCenter(startNode,endNode)
        super().__init__(ID, position)
        self._type = 'straightLine'
        self.__length = self._findLength(startNode,endNode)

    def __findCenter(self, node1, node2) -> list:
        x = (node1.position()['x'] + node2.position()['x']) / 2
        y = (node1.position()['y'] + node2.position()['y']) / 2
        z = (node1.position()['z'] + node2.position()['z']) / 2
        return [x, y, z]
    
    def _findLength(self, node1, node2) -> float:  
        x = node2.position()['x'] - node1.position()['x']
        y = node2.position()['y'] - node1.position()['y']
        z = node2.position()['z'] - node1.position()['z']
        l = (x**2 + y**2 + z**2)**0.5
        return l

    def Length(self):
        print(f'straightLine {self.ID()} length = {self.__length:0.5f}')



        



class Shell(LUCA):
    def __init__(self, ID: int, edges: list):
        # method to calculate center of shell from center of edges
        position = self.__findCenter(edges)
        super().__init__(ID, position)
        self._type = 'shell'

    def __findCenter(self, lines: list) -> list:
        x, y, z = [0, 0, 0]
        for line in lines:
            x += line.position()['x']
            y += line.position()['y']
            z += line.position()['z']
        x /= len(lines)
        y /= len(lines)
        z /= len(lines)

        return [x, y, z]