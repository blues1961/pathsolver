import numpy as np
import  random
'''
********************************************************************************
Class Node
*******************************************************************************
'''
class Node:

    position=None  #Position
    previous=None #previous Position

    f=0  #distance from starting position + distance estimate to the ending position
    g=0  #distance from startingf position
    h=0  #Estimated distance to the ending position (Manathan distance)

    def __init__(self,position=None,previous=None):
        self.position=position
        self.previous=previous
        self.f=0
        self.g=0
        self.h=0

    def print(self):
        print (self.position,self.f,self.g,self.h,self.previous)

'''
*******************************************************************************
Class AStar
*******************************************************************************
'''
class AStar():

    #Global constants

    WALKABLE=0

    #Attributes
    map=[]
    startPos=None
    endPos=None

    startNode=None
    currentNode = None

    openNodes=[]
    closedNodes=[]

    path=[]


    #Init with an existing map
    def __init__(self,map=[],start=None,end=None):

        self.map = map
        self.opennodes=[]
        self.closednodes=[]
        self.path=[]

        self.startPos=[0,0]
        self.map[startpos]=0
        if start!=None: self.startPos=start

        self.endPos=[self.mapRows()-1,self.mapCols()-1]
        if end !=None: self.endPos=end

        #init nodes

        self.startNode=Node(self.startPos)
        self.startNode.g=0
        self.startNode.h=self.heuristicDistance(self.startNode.position)
        self.startNode.f=self.startNode.g+self.startNode.h
        self.currentNode=self.startNode
        self.map[self.startPos[0]][self.startPos[1]]=1
        self.opennodes.append(self.currentNode)

        print('instantiate')
        print(self.currentNode.position)
        print(self.opennodes)

    #init by generating random map
    def __init__(self,mapWidth=20,mapHeight=15):

        self.init_map(mapWidth,mapHeight)

        self.opennodes=[]
        self.closednodes=[]
        self.path=[]

        self.startPos=[0,0]
        self.endPos=[self.mapRows()-1,self.mapCols()-1]

        #Make sure start pos and end pos are WALKABLE
        self.map[self.startPos[0]][self.startPos[1]]=self.WALKABLE
        self.map[self.endPos[0]][self.endPos[1]]=self.WALKABLE

        #init nodes

        self.startNode=Node(self.startPos)
        self.startNode.g=0
        self.startNode.h=self.heuristicDistance(self.startNode.position)
        self.startNode.f=self.startNode.g+self.startNode.h
        self.currentNode=self.startNode
        self.opennodes.append(self.currentNode)
        self.map[self.startPos[0]][self.startPos[1]]=1
        print('instantiate')
        print(self.currentNode.position)
        print(self.opennodes)




    def mapRows(self): return len(self.map)
    def mapCols(self): return len(self.map[0])

    def init_map(self,cols,rows):

        #create map without obstacle
        self.map=[[0]*cols for i in range(rows)]

        #Add random obstacle
        for i in range(rows):
            for j in range(cols-1):
                if j >= cols-6 and i >= rows-6:
                    self.map[i][j]=0
                else:
                    a=random.random()
                    if a <= 0.3:
                        self.map[i][j]=1
                    else:
                        self.map[i][j]=0

        for i in range(int(rows/2-10),int(rows/2+5)):
            for j in range(int(cols/2-20),int(cols/2+20)):
                self.map[i][j]=1

        for i in range(int(rows/2+10),int(rows/2+15)):
            for j in range(int(cols/2-20),int(cols/2+20)):
                self.map[i][j]=1

        for i in range(int(rows-20),int(rows)):
            for j in range(int(cols-20),int(cols-5)):
                self.map[i][j]=1
        for c in range(cols):
            self.map[rows-1][c]=0
    def heuristicDistance(self,position):
       a=abs(self.endPos[0]-position[0])
       b=abs(self.endPos[1]-position[1])
       return (a+b)

    def getNeighbors(self,position):
        r=position[0]
        c=position[1]
        neighbors=[]
        nlist=[[r-1,c-1],[r-1,c],[r-1,c+1],[r,c-1],[r,c+1],[r+1,c-1],[r+1,c],[r+1,c+1]]
        #nlist=[[r-1,c],[r,c-1],[r,c+1],[r+1,c]]
        for item in nlist:
            if item[0]>=0 and item[1] >= 0 and item[0]<self.mapRows() and item[1]<self.mapCols():
                if self.map[item[0]][item[1]]==self.WALKABLE:
                    neighbors.append(item)
        return neighbors

    def buildPath(self,node):
        path=[]
        path.append(node.position)
        while node != None:
            node=next((n for n in self.closednodes if n.position==node.previous),None)
            if node != None:
                path.append(node.position)
        return list(reversed(path))



    def solverStep(self):
        #self.currentNode.print()
        self.path=self.buildPath(self.currentNode)

        for position in self.getNeighbors(self.currentNode.position):
            if next((n for n in self.closednodes if n.position==position),None)==None:

                neighbornode= next((n for n in self.opennodes if n.position==position),None)
                if neighbornode==None:
                    neighbornode=Node(position,self.currentNode.position)
                    neighbornode.g=self.currentNode.g+1
                    neighbornode.h=self.heuristicDistance(position)
                    neighbornode.f=neighbornode.g+neighbornode.h
                    self.opennodes.append(neighbornode)
                else:
                    g=self.currentNode.g+1
                    h=self.heuristicDistance(position)
                    f=g+h
                    if neighbornode.f>f:
                        neighbornode.f=f
                        neighbornode.g=g
                        neighbornode.h=h
                        neighbornode.previous=self.currentNode.position

        self.closednodes.append(self.currentNode)
        self.opennodes.remove(self.currentNode)
        self.currentNode = min(self.opennodes ,key=lambda node:node.f)


    def solve(self):
        while len(self.opennodes) > 0:
            if self.currentNode.position==self.endPos:
                self.path=self.buildPath(self.currentNode)
                return self.path
            self.solverStep()
        #print(self.currentPath)
        return self.path

    def print_map(self):
        for r in range(self.mapRows()):
            line=''
            for c in range(self.mapCols()):
                position=[r,c]
                if position==self.endPos:
                    line+='X'
                elif next((n for n in self.opennodes if n.position==position),None) != None:
                    line+='O'
                elif next((n for n in self.closednodes if n.position==position),None) != None:
                    line+='*'
                elif self.map[r][c]==0:
                    line += str(' ')
                else:
                    line += str(self.map[r][c])
            print(line)

    def print_opennodes(self):
        for item in self.opennodes:
            print (item.position,item.f,item.g,item.h,item.previous)

    def print_closednodes(self):
        for item in self.closednodes:
            print (item.position,item.f,item.g,item.h,item.previous)

def main():

    astar = AStar(30,20) #  Width,Height
    astar.print_map()
    astar.currentNode.print()
    print(astar.solve())



if __name__ == "__main__":
    main()
