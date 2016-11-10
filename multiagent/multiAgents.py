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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        if successorGameState.isWin():
            return float("inf")
        c_ghost = 100
        for ghost in currentGameState.getGhostPositions():
            dist = util.manhattanDistance(ghost, newPos)
            if(dist < c_ghost):
                c_ghost = dist
        score = successorGameState.getScore() + c_ghost
        if c_ghost == 3:
            score += float("-inf")
        c_food = 100
        for food in newFood.asList():
            dist = util.manhattanDistance(food, newPos)
            if(dist < c_food):
                c_food = dist
        score -= c_food

        if currentGameState.getNumFood() > successorGameState.getNumFood():
            score += 200
        if action == Directions.STOP:
            score -= 200
        return score

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
        """
        "*** YOUR CODE HERE ***"
        def maximize(gameState, agent, depth):
            maxV = float("-inf")
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            for action in gameState.getLegalActions(0):
                successorGameState = gameState.generateSuccessor(0, action)
                value = minimize(successorGameState, 1, depth)

                if value > maxV:
                    maxAction = action
                    maxV = value

            if depth == 1:
                return maxAction
            else:
                return maxV

        def minimize(gameState, agent, depth):
          minV= float("inf")
          numGhosts = gameState.getNumAgents() - 1

          if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

          for action in gameState.getLegalActions(agent):
            successorGameState = gameState.generateSuccessor(agent, action)

            if agent == numGhosts:
              if depth == self.depth:
                value = self.evaluationFunction(successorGameState)
              else:
                value = maximize(successorGameState, 0, depth+1)
            else:
              value = minimize(successorGameState, agent+1, depth)
            minV = min(value, minV)
          return minV

        return maximize(gameState, 0, 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_pruning(gameState, agent, depth, a, b):
            maxV = float("-inf")
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            for action in gameState.getLegalActions(0):
                successorGameState = gameState.generateSuccessor(0, action)
                value = min_pruning(successorGameState, 1, depth, a, b)
                if value > b:
                    return value
                if value > maxV:
                    maxV = value
                    maxAction = action
                a = max(a, maxV)
            if depth == 1:
                return maxAction
            else:
                return maxV

        def min_pruning(gameState, agent, depth, a, b):
            minV = float("inf")
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            numGhosts = gameState.getNumAgents() - 1

            for action in gameState.getLegalActions(agent):
                successorGameState = gameState.generateSuccessor(agent, action)
                if agent == numGhosts:
                    if depth == self.depth:
                        value = self.evaluationFunction(successorGameState)
                    else:
                        value = max_pruning(successorGameState, 0, depth+1, a, b)
                else:
                    value = min_pruning(successorGameState, agent+1, depth, a, b)

                if value < a:
                    return value
                if value < minV:
                    minV = value
                    minAction = action
                b = min(b, minV)
            return minV

        return max_pruning(gameState, 0, 1, float('-inf'), float("inf"))

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maximize(gameState, agent, depth):
            maxV = float("-inf")
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            for action in gameState.getLegalActions(0):
                successorGameState = gameState.generateSuccessor(0, action)
                value = minimize(successorGameState, 1, depth)
                if value > maxV:
                    maxV = value
                    maxAction = action
            if depth == 1:
                return maxAction
            else:
                return maxV

        def minimize(gameState, agent, depth):
            minV = 0
            numGhosts = gameState.getNumAgents() - 1

            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            legalActions = gameState.getLegalActions(agent)
            probability = 1.0/len(legalActions)
            for action in legalActions:
                successorGameState = gameState.generateSuccessor(agent, action)
                if agent == numGhosts:
                    if depth == self.depth:
                        value = self.evaluationFunction(successorGameState)
                    else:
                        value = maximize(successorGameState, 0, depth+1)
                else:
                    value = minimize(successorGameState, agent+1, depth)
                minV += value * probability
            return minV

        return maximize(gameState, 0, 1)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    pos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    curFood = currentGameState.getFood()

    if currentGameState.isLose():
        return -float("inf")

    if currentGameState.isWin():
        return float("inf")

    c_food = float("inf")
    for food in curFood.asList():
        dist = util.manhattanDistance(food, pos)
        if(dist < c_food):
            c_food = dist


    capsules = len(currentGameState.getCapsules())
    numFoods = currentGameState.getNumFood()

    scaredGhosts, activeGhosts = [], []
    for ghost in currentGameState.getGhostStates():
        if not ghost.scaredTimer:
            activeGhosts.append(ghost)
        else:
            scaredGhosts.append(ghost)

    c_AGhost = c_SGhost = float("inf")

    if activeGhosts:
        for ghost in activeGhosts:
            ghostPosition = (int(ghost.getPosition()[0]), int(ghost.getPosition()[1]))
            dist = util.manhattanDistance(ghostPosition, pos)
            if(dist < c_AGhost):
                c_AGhost = dist
    else:
        c_AGhost = 5

    if scaredGhosts:
        for ghost in scaredGhosts:
            ghostPosition = (int(ghost.getPosition()[0]), int(ghost.getPosition()[1]))
            dist = util.manhattanDistance(ghostPosition, pos)
            if(dist < c_SGhost):
                c_SGhost = dist
    else:
        c_SGhost = 0
        
    return score - 1.5 * c_food - 2 * (1.0/c_AGhost) - 2 * c_SGhost - 30 * capsules - 5 * numFoods

# Abbreviation
better = betterEvaluationFunction
