# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        false = 0 #This variable represents the total number of non-food blocks in the gamestate, the less there the better since that means that pacman has eaten some
        minfood = -1 #The distance to the closest availiable food dot, the closest pacman is to a food-dot the better
        for i in range(0,newFood.width): #For all the blocks of the game state
            for j in range(0,newFood.height):
                if newFood[i][j]==False:
                    false += 1 #if there is no food in this block, the counter value is increased
                else: #If there is food in the block,
                    m = manhattanDistance((i,j),(newPos[0],newPos[1])) #the distance from the pacman is estimated using manhattan distance
                    if minfood == -1 or m < minfood: #If the distance has not been initialized, or the new estimation shows that we found a closer food dot...
                        minfood = m #... The min distance is updated

        minGhostDistance = -1 #The distance to the closest availiable food dot, the farther the better
        for ghost in newGhostStates: #For all the ghosts 
            m = manhattanDistance((ghost.configuration.pos[0],ghost.configuration.pos[1]),(newPos[0],newPos[1])) #Calculating the estimation of the real distance
            #If this ghost is closer or the ghost distance has not been initialized AND the ghost is a threat because it can not be eaten
            if (minGhostDistance == -1 or m < minGhostDistance) and newScaredTimes[0]<1:
                minGhostDistance = m #The min distance is updated

        if minGhostDistance > 4  or minGhostDistance == -1: #If there are ghosts that can not be eaten and are not far enough not to pose a threat
            return successorGameState.getScore() + false + 1.0/float(minfood) #The evalution value is the gamescore + a value to reward the distance from the closest food
            #*Note: we want to reward the closest (smallest) food distance, but the higher values are better so the use of 1/closest food increases the value as the food gets closer
        else:
            #If the ghost poses a threat, pacman needs to escape from it, so he is rewarded for the choices that get him away from the ghost and may also increase the score
            return successorGameState.getScore() + minGhostDistance

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    #The whole minimax algorithm is implemented using this function, it returns the move and the minimax value in a tuple
    def minimax(self,gameState,agentIndex=0,depth=0):
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            #Terminal node of the minimax tree, only the minimax value is returned, there is not any other possible move to be made
            return (self.evaluationFunction(gameState),None)

        if agentIndex == gameState.getNumAgents() - 1:
            depth += 1 #If the ghosts and pacman will all have "played" after this minimax node, the depth of the tree is increased
        elif agentIndex >= gameState.getNumAgents():
            agentIndex = 0 #If everyone has "played", the turn is restarted with pacman first

        actions = gameState.getLegalActions(agentIndex)
        bestNum = None #Best value for max (or min) to chose

        if agentIndex == 0: #If it is the Max players turn (aka pacman), the best option is calulated using the max part of the minimax algorithm
            for action in actions:
                v = self.minimax(gameState.generateSuccessor(agentIndex, action),agentIndex+1,depth) #Calculation of all the values of the nodes recursively
                if bestNum != None:
                    if bestNum < v[0]: #If a better-bigger value for max is found, it is kept along with it's action
                        bestNum = v[0]
                        bestAction = action
                else: #If the best value has not been initialized, there is nothing to compare it, and it is initialized with the first V value and action
                    bestNum = v[0]
                    bestAction = action

        else: #If it is the Min players turn (aka ghosts), the best option is calulated using the min part of the minimax algorithm (same as above but for min)
            for action in actions:
                v = self.minimax(gameState.generateSuccessor(agentIndex, action),agentIndex+1,depth)
                if bestNum != None:
                    if bestNum > v[0]:
                        bestNum = v[0]
                        bestAction = action
                else:
                    bestNum = v[0]
                    bestAction = action

        return (bestNum,bestAction) #The best value (min value for min/ghosts, max value for max/pacman), along with the action that leads to this value is returned

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #The best action of the minimax tree is calculated recursively with the above function (the recursion starts by default with pacman and depth=0)
        return self.minimax(gameState)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    #The code is the same as in the above MinimaxAgent.minimax(), with only the necessary changes to implement alpha-beta pruning. Thus only the alpha beta pruning code is explained
    def minimaxAlphaBeta(self,gameState,agentIndex=0,depth=0,a=None,b=None):
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return (self.evaluationFunction(gameState),None)

        if agentIndex == gameState.getNumAgents() - 1:
            depth += 1
        elif agentIndex >= gameState.getNumAgents():
            agentIndex = 0

        actions = gameState.getLegalActions(agentIndex)
        bestNum = None

        if agentIndex == 0: #Max turn (aka pacman)
            for action in actions:
                v = self.minimaxAlphaBeta(gameState.generateSuccessor(agentIndex, action),agentIndex+1,depth,a,b)
                if bestNum != None:
                    if bestNum < v[0]:
                        bestNum = v[0]
                        bestAction = action
                else:
                    bestNum = v[0]
                    bestAction = action

                #Alpha-beta pruning, as shown in lecture
                #If b is initialized the pruning condition is checked. The same behavior as in the lecture slides where b would be infinity and the pruning case would never be fulfilled
                if b != None:
                    if bestNum > b:
                        return (bestNum,bestAction)

                #The same goes for a, in the slides it would be initialized with -infinity, here the initialization case is checked separately
                if a == None:
                    a = bestNum
                elif bestNum > a:
                    a = bestNum

        else: #Min turn (aka ghosts)
            for action in actions:
                v = self.minimaxAlphaBeta(gameState.generateSuccessor(agentIndex, action),agentIndex+1,depth,a,b)
                if bestNum != None:
                    if bestNum > v[0]:
                        bestNum = v[0]
                        bestAction = action
                else:
                    bestNum = v[0]
                    bestAction = action

                #Alpha-beta pruning, as shown in lecture
                #The approach for the a value and its initialization is the same as for b in the max case
                if a != None:
                    if bestNum < a:
                        return (bestNum,bestAction)
                #Respectively the approach for the b initialization
                if b == None:
                    b = bestNum
                elif bestNum < b:
                    b = bestNum

        return (bestNum,bestAction)

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxAlphaBeta(gameState)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    #The expectimax function code is the same as in the above MinimaxAgent.minimax for the max (pacman) part, only the min (ghosts) part which is different is explained
    def expectimax(self,gameState,agentIndex=0,depth=0):
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return (self.evaluationFunction(gameState),None)

        if agentIndex == gameState.getNumAgents() - 1:
            depth += 1
        elif agentIndex >= gameState.getNumAgents():
            agentIndex = 0

        actions = gameState.getLegalActions(agentIndex)
        bestNum = None

        if agentIndex == 0: #Max turn (aka pacman)
            for action in actions:
                v = self.expectimax(gameState.generateSuccessor(agentIndex, action),agentIndex+1,depth)
                if bestNum != None:
                    if bestNum < v[0]:
                        bestNum = v[0]
                        bestAction = action
                else:
                    bestNum = v[0]
                    bestAction = action
            return (bestNum,bestAction)

        else: #Min turn (aka ghosts)
            #For the estimation of the ghost moves, which can be non-ideal for them, the average value of the all the possible next ghost choices is returned
            s = 0 #Sum of values for next options
            for action in actions:
                s += self.expectimax(gameState.generateSuccessor(agentIndex, action),agentIndex+1,depth)[0]
            if len(actions) > 0: #If there were any possible  moves (there always are, but since division is used the check is needed)
                #The average value is returned in order to simulate non ideal choises with a none (empty) action since  the actions of non-ideal ghost will never be used
                return (s/len(actions),None)
            else:
                return (0,None) #If there were not possible moves, there is also no posible min value (unreachable code for the inputs of exercise)

        
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState)[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: To evaluate a given state all the following parameters are taken into consideration:
                 Similarly to the evaluationFunction of Q1:
                    The distance from the closest ghost, the farther the better
                    The distance from the closest food, the closest the better
                    The number of blocks that do not contain any food, the more the better since that means that pacman has eaten food from blocks
                 Additionally:
                    The distance from the closest capsule (big white dots), only if it is in the best interest of pacman to eat the capsule for the given state
                    The distance to the closest ghost that can be eaten and increase the score (if there are any)
    """
    "*** YOUR CODE HERE ***"

    #The above parameters are not taken intro consideration if pacman is to lose or to win in the given state
    if currentGameState.isWin():
        return 1000000*currentGameState.getScore() #If he is to win, this is the best possible state and it is heavily rewarded
    elif currentGameState.isLose():
        return 1000000*currentGameState.getScore() #If pacman is to lose, this is the worst possible state, and the negative score is multiplied to reflect how bad the state is

    #If the pacman is not to lose or win, the evaluation value is calculated
    pacmanP = currentGameState.getPacmanPosition() #Getting the position of the pacman in the given state
    foodGrid = currentGameState.getFood() #Getting the matrix to know in which the blocks there is food

    #false and minFood represent the same value as in the evaluationFunction of Q1
    false = 0
    minfood = -1
    for i in range(0,foodGrid.width):
        for j in range(0,foodGrid.height):
            if foodGrid[i][j]==False:
                false += 1
            else:
                m = manhattanDistance((i,j),(pacmanP[0],pacmanP[1]))
                if minfood == -1 or m < minfood:
                    minfood = m

    minCapsule = -1 #The distance to the capsule is the closest 
    capsules = currentGameState.getCapsules() #All the capsules possitions
    for capsule in capsules:
        m = manhattanDistance(capsule,(pacmanP[0],pacmanP[1])) #manhattan distance from pacman is calculated for each capsule
        if minCapsule == -1 or m < minCapsule: #If this is the distance or the new closest
            minCapsule = m #The closest capsule distance is updated

    minGhostDistance = -1 #Closest ghost
    eatableGhostDistance = -1 #Closest ghost that can be eaten (aka scared ghost)
    for ghost in currentGameState.getGhostStates():
        m = manhattanDistance(ghost.getPosition(),(pacmanP[0],pacmanP[1]))
        #If this ghost is closer or the ghost distance has not been initialized AND the ghost is a threat because it can not be eaten
        if (minGhostDistance > m  or minGhostDistance == -1) and ghost.scaredTimer < 1:
            minGhostDistance = m
        elif ghost.scaredTimer >= 1: #If there are any ghosts that can be eaten, the distance to the closest one is saved
            m = manhattanDistance(ghost.getPosition(),(pacmanP[0],pacmanP[1]))
            if m < eatableGhostDistance:
                eatableGhostDistance = m

    score = currentGameState.getScore()
    if minGhostDistance > 4 or minGhostDistance == -1: #If the ghost is not a threat, all the calculated values are taken into consideration
        score += false - minGhostDistance/4 #Number of blocks without food + closest ghost, but since it does not pose a threat in a small percentage
        if eatableGhostDistance !=-1: #If there are any ghosts that can be eaten
            score += 1.0/float(eatableGhostDistance) #They are also taken into consideration in order to properly evaluate the state
        if minCapsule !=-1 and len(capsules) > currentGameState.getNumFood(): #If there are capsules, and it is in the interest of pacman to eat them...
            #...(if there are not many food dots left to eat, pacman is close to win and there is no point in going for the capsules)...
            score += 1.0/float(minCapsule) #The capsule distance is also taken into consideration
        if minfood != -1: #If there is any food left to eat
            score += 1.0/float(minfood) #The distance to the closest is also taken into consideration
    else: #Otherwise, if a ghost poses a threat
        score += minGhostDistance #Only the score and the distance from the ghost evaluate the state, since pacman has to escape from death
    return score

# Abbreviation
better = betterEvaluationFunction
