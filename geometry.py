import math
import pandas as pd
from elements import Node, StraightLine, Shell

class World():
    """
    The main class, used to create elemental geometry including nodes, striaght lines, arcs and shells.

    Use the class methods to instantialize and store geometrical information.
    """

    def __init__(self) -> None:
        self.__elements = {'nodes':{}, 'straightLines':{}, 'arcs':{}, 'shells':{}}

    
    def __check(self, element, elementType:str):
        """
        An internal method to check element being created is unique, before updating the internal dictionaries with the element.

        Parameters
        -------------------------
        element : object (required)
            The object being created/checked

        elementType: str (required)
            a string specifying type of element being checked: node, straightline, arc, shell

        
        Example Usage
        -------------------------
        World().__check(arc_object, 'arc')
        
        Checks arc_object.ID() against self.__elements['arcs'] dictionary
        If an arc does not already exist with the same name, the arc is added to the self.__elements['arcs'] dictionary
        Otherwise, the name is incremented with the first available integer and then added.

        Returns
        -------------------------
        The object being checked.
        NOTE if the original ID already exists, the object is returned with a unique ID
        """

        elementList = self.__elements[elementType]

        if element.ID() not in elementList:
            elementList[element.ID()] = element
        else:
            newID = list(elementList.keys())[-1] + 1
            print(f'{elementType} {element.ID()} already exists - node added as Node {newID}')
            element.changeID(newID)
            elementList[newID] = element
        
        return element


    def createNodes(self, IDs:list, positions:list) -> list:
        """
        A method to create nodes.

        Parameters
        -------------------------
        IDs : list (required)
            a list of integers representing the IDs assigned to each node; must be unique to each node
            NOTE length must match positions list

        positions: list (required)
            a list of 3 element lists, where the 3 elements represent the X, Y and Z coordinates of each node
            NOTE length must match IDs list

        
        Example Usage
        -------------------------
        World().createNodes([1, 2], [[0, 0, 0], [1, 0, 0]])
        
        Creates 2 nodes: 
            node 1 with coordinates x: 0 y: 0 z: 0
            node 2 with coordinates x: 1 y: 0 z: 0

        Returns
        -------------------------
        A list of the Node instances created
        """

        nodes = []
        for lbl, pos in zip(IDs, positions):
            node = Node(lbl, pos)
            node = self.__check(node, 'nodes')
            nodes.append(node)
        return nodes
    
    def createStraightLines(self, IDs:list, startNodes:list, endNodes:list) -> list:
        """
        A method to create straight lines.
        NOTE updates start and end node instances with line ID connected to them

        Parameters
        -------------------------
        IDs : list (required)
            a list of integers representing the IDs assigned to each line; must be unique to each node
            NOTE length must match startNodes and endNodes lists

        startNodes: list (required)
            a list containing the start Node instances for each line
            NOTE length must match IDs list
        
        endNodes: list (required)
            a list containing the end Node instances for each line
            NOTE length must match IDs list

        
        Example Usage
        -------------------------
        World().createStraightLines([1, 2], [Node_instance_1, Node_instance_2], [Node_instance_3, Node_instance_3])
        
        Creates 2 straight lines: 
            Straight line 1 between Node 1 and Node 3
            Straight line 2 between Node 2 and Node 3

        Returns
        -------------------------
        A list of the straight line instances created
        """

        lines = []
        for lbl, a, b in zip(IDs, startNodes, endNodes):
            if a.ID != b.ID:
                line = StraightLine(lbl, a, b)
                line = self.__check(line, 'straightLines')
                lines.append(line)
                for node in [a, b]:
                    node._addConnectedElement(line.ID(), line, 'straightLines')
            else:
                print('Cannot create a straight line ending at the same node!')
        
        return lines

    def printElements(self, elementType: str) -> None:
        """
        A method to print all elements of the type specified, and the coordinates of their centers.

        Parameters
        -------------------------
        elementType: str (required)
            options : 'node' 'straightLine' 'arc' 'shell'
        
        Example Usage
        -------------------------
        World().printElements('shell')
        """

        label = elementType + 's'

        print('\n' + '-'*25 + f'\nListing defined {label}:\n' + '-'*25)
        for k, v in self.__elements[label].items():
            print(f'{elementType.capitalize()} {k} - center {v.position()}')

    def listElements(self, elementType: str) -> dict:
        """
        A method which returns a dictionary of all elements of the type specified.

        Parameters
        -------------------------
        elementType: str (required)
            options : 'node' 'straightLine' 'arc' 'shell'
        
        Example Usage
        -------------------------
        all_straight_lines = World().listElements('straightLine')

        Returns
        -------------------------
        A dictionary of all straight line elements
        """

        return self.__elements[elementType + 's']
    
    # add a trickle down feature where all attached elements are deleted given they are not themselves attached to other elements
    def delete(self, IDs: list, elementTypes: list):
        """
        A method to delete elements.
        NOTE if an element is attached to another element, it will not be deleted and a message will be printed to prompt

        Parameters
        -------------------------
        IDs : list (required)
            a list of integers representing the IDs of the elements to be deleted
        
        elementTypes : list (required)
            a list of the element types to be deleted, matching the order the elements are in inside the IDs list
            options : 'node' 'straightLine' 'arc' 'shell'

            NOTE if only one element type is specified in the list e.g. ['node'] ; this element type is assumed for
            all elements in the IDs list
        
        Example Usage
        -------------------------
        World().delete([1, 2, 2], ['straightLine', 'node', 'arc'])
        
        Deletes straight line 1, node 2 and arc 2

        World().delete([1, 4, 8], ['arc'])

        Deletes arcs 1, 4 and 8
        """

        if len(elementTypes) == 1:
            elementTypes *= len(IDs)

        for ID, eleType in zip(IDs, elementTypes):
            code = eleType + 's'
            label = eleType.capitalize()
            if ID in self.__elements[code].keys():
                if any([len(item) for item in self.__elements[code][ID].listConnectedElements().values()]):
                    print(f'\n{label} {ID} connected to other elements, cannot delete!')
                    self.__elements[code][ID].printConnectedElements()
                else:
                    del self.__elements[code][ID]
            else:
                print(f'\n{label} {ID} does not exist')



### do the same for lines, then arcs, then shells
### think about including matrix operations to move things


