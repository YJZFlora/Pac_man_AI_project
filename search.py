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
    start_state = problem.getStartState()
    # each tuple is (position, action list)
    start_tuple = (start_state, [])
    # OPEN: stack with states
    OPEN = util.Stack()
    OPEN.push(start_tuple)
    visited = []

    while not OPEN.isEmpty():
        cur_tuple = OPEN.pop()
        cur_position = cur_tuple[0]
        cur_path = cur_tuple[1]

        if problem.isGoalState(cur_tuple[0]):
            return cur_tuple[1]

        if cur_position not in visited:
            visited.append(cur_position)
            successors = problem.getSuccessors(cur_position)
            for successor in successors:
                suc_position = successor[0]
                step_action = successor[1]
                OPEN.push((suc_position, cur_path + [step_action]))

    return []


def get_movements(problem, parentMap, cur_tuple, start_tuple):
    path = []
    movements = []
    path.append(cur_tuple[1])
    parent = parentMap[cur_tuple]
    while parent is not start_tuple:
        path.insert(0, parent[1])
        parent = parentMap[parent]

    for step in path:
        movements.append(step)

    return movements


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    start_state = problem.getStartState()
    start_tuple = (start_state, [])
    OPEN = util.Queue()
    OPEN.push(start_tuple)
    visited = []

    while not OPEN.isEmpty():
        cur_tuple = OPEN.pop()
        cur_position = cur_tuple[0]
        cur_path = cur_tuple[1]

        if problem.isGoalState(cur_position):
            return cur_path

        if cur_position not in visited:
            visited.append(cur_position)
            successors = problem.getSuccessors(cur_position)
            for successor in successors:
                suc_position = successor[0]
                step_action = successor[1]
                OPEN.push((suc_position, cur_path + [step_action]))

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    start_state = problem.getStartState()
    start_tuple = (start_state, 0, [])

    OPEN = util.PriorityQueue()
    # PriorityQueue.push(tuple, priority)
    OPEN.push(start_tuple, 0)
    visited = []

    while not OPEN.isEmpty():
        cur_position, cur_cost, cur_path = OPEN.pop()

        if problem.isGoalState(cur_position):
            return cur_path

        if cur_position not in visited:
            visited.append(cur_position)
            for successor in problem.getSuccessors(cur_position):
                suc_state, step_action, step_cost = successor
                successor_tuple = (suc_state, step_cost, cur_path + [step_action])
                OPEN.push(successor_tuple, problem.getCostOfActions(cur_path + [step_action]))

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    start_state = problem.getStartState()
    start_tuple = (start_state, 0, [])

    OPEN = util.PriorityQueue()
    # PriorityQueue.push(tuple, priority)
    OPEN.push(start_tuple, 0)
    visited = []

    while not OPEN.isEmpty():
        cur_position, cur_cost, cur_path = OPEN.pop()

        if problem.isGoalState(cur_position):
            return cur_path

        if cur_position not in visited:
            visited.append(cur_position)
            for successor in problem.getSuccessors(cur_position):
                suc_state, step_action, step_cost = successor
                successor_tuple = (suc_state, step_cost, cur_path + [step_action])
                OPEN.update(successor_tuple, problem.getCostOfActions(cur_path + [step_action]) + heuristic(successor[0], problem))

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
