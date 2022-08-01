# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    visited = set() #The visited nodes are keept in a set in order have O(1) access
    stack = util.Stack() #in dfs a stack is used to save the nodes
    pathToHere = []
    position = problem.getStartState()
    firstLoop = True

    while (not stack.isEmpty()) or firstLoop: #While there are nodes to explore in the stack (or we are in the first iteration and the stack has not nodes yet)
        if firstLoop:
            firstLoop = False
        else:
            nextState = stack.pop()
            position = nextState[0] #Next position to explore new nodes
            pathToHere = nextState[1] #The path in WEST,SOUTH.... form up to this node
        if problem.isGoalState(position):
            return pathToHere #If the position is the goal, the path to this possition is returned

        if not position in visited: #If the position has not been visited 
            visited.add(position) #It is added to the visited positions
            for option in problem.getSuccessors(position): #The new positions that can be reached from here
                #Are all pushed to the stack along with their paths in SOUTH,WEST... form
                newPath = pathToHere.copy()
                newPath.append(option[1]) 
                stack.push((option[0],newPath)),#The path to the node, and it's possition are pushed to the stack to be later explored

    return None #If the goal was not found in the loop, the goal could never been reached with the given problem
    util.raiseNotDefined() #Unreachable code as intended since the function is properly defined

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    """The exact same procedure as above (depthFirstSearch), 
       but as the breadth first search algorithm defines
       we use a queue instead of a stack"""

    visited = set()
    queue = util.Queue() #queue instead of a stack
    pathToHere = []
    position = problem.getStartState()
    firstLoop = True

    while (not queue.isEmpty()) or firstLoop:
        if firstLoop:
            firstLoop = False
        else:
            nextState = queue.pop()
            position = nextState[0]
            pathToHere = nextState[1]
        if problem.isGoalState(position):
            return pathToHere

        if not position in visited:
            visited.add(position)
            for option in problem.getSuccessors(position):
                newPath = pathToHere.copy()
                newPath.append(option[1]) 
                queue.push((option[0],newPath))

    return None
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """The exact same procedure as above (depthFirstSearch), 
       but as the uniform cost search algorithm defines
       we use a priority queue instead of a stack.
       where the priority of a position is the sum of nodes that have been traversed until this position"""

    visited = set()
    PQ = util.PriorityQueue()
    pathToHere = []
    position = problem.getStartState()
    firstLoop = True
    cost = 0 #Initial priority is 0, since  pacman is first placed on the starting position

    while (not PQ.isEmpty()) or firstLoop:
        if firstLoop:
            firstLoop = False
        else:
            nextState = PQ.pop()
            cost = nextState[2] #Priority of node
            position = nextState[0]
            pathToHere = nextState[1]
        if problem.isGoalState(position):
            return pathToHere

        if not position in visited:
            visited.add(position)
            for option in problem.getSuccessors(position):
                newPath = pathToHere.copy()
                newPath.append(option[1]) 
                #The priority is calculated as the cost until this position + the cost returned from problem.set Successors(position) (option[2])
                PQ.push((option[0],newPath,cost + option[2]),cost + option[2])

    return None
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """The exact same procedure as above (uniformCostSearch), 
       but as the A* algorithm defines
       a heuristic is used to calculate the priority/cost of a node"""
    visited = set()
    PQ = util.PriorityQueue()
    pathToHere = []
    position = problem.getStartState()
    firstLoop = True
    cost = 0

    while (not PQ.isEmpty()) or firstLoop:
        if firstLoop:
            firstLoop = False
        else:
            nextState = PQ.pop()
            estimate = nextState[3] #Estimate is the heuristic value of this node
            cost = nextState[2]
            position = nextState[0]
            pathToHere = nextState[1]
        if problem.isGoalState(position):
            return pathToHere

        if not position in visited:
            visited.add(position)
            for option in problem.getSuccessors(position):
                newPath = pathToHere.copy()
                newPath.append(option[1]) 
                newEstimate = heuristic(option[0],problem) #Calculating the heuristic value to this new node
                #The heuristic value is saved seperatly from the cost, since acces to only this value may be needed
                PQ.push((option[0],newPath,cost + option[2],newEstimate),cost + option[2] + newEstimate)
        elif heuristic(position,problem)<estimate:
            #If the node has been visited before but the heuristic now calculates a smaller value
            #The new smaller value replaces the old one
            PQ.push((position,pathToHere,cost,heuristic(position,problem)),cost+heuristic(position,problem))

    return None
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
