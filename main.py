from geometry import World

def main():
    W = World()    
    W.createNodes([1,1],[[1,0,0],[2,0,0]])
    W.printElements('node')
    W.delete([3,2,7],['node'])
    W.printElements('node')
    W.createNodes([3,5],[[5,2,0],[3,2,1]])
    W.printElements('node')

    allnodes = W.listElements('node')
    W.createStraightLines([1,2,3],[allnodes[1],allnodes[1],allnodes[1]],[allnodes[3],allnodes[5],allnodes[1]])
    for n in allnodes.values():
        n.printConnectedElements()

    W.printElements('straightLine')

    for l in W.listElements('straightLine').values():
        l.Length()


if __name__ == '__main__':
    main()