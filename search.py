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
		"""
	# print("Start:", problem.getStartState())
	# print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
	# print("Start's successors:", problem.getSuccessors(problem.getStartState()))

	closed = []

	start_state = problem.getStartState()
	start_item = (start_state, [])

	stack = util.Stack()
	stack.push(start_item)

	while not stack.isEmpty():
		node, actions_list = stack.pop()

		if problem.isGoalState(node):
				return actions_list

		if node not in closed:
			closed = closed + [node]
		
			for successor, action, cost in problem.getSuccessors(node):
				actions = actions_list + [action]
				new_start_item = (successor, actions)
				stack.push(new_start_item)

	return []

# ________________________________________________________________

class _RecursiveDepthFirstSearch(object):
	'''
		=> Output of 'recursive' dfs should match that of 'iterative' dfs you implemented
		above. 
		Key Point: Remember in tutorial you were asked to expand the left-most child 
		first for dfs and bfs for consistency. If you expanded the right-most
		first, dfs/bfs would be correct in principle but may not return the same
		path. 

		=> Useful Hint: self.problem.getSuccessors(node) will return children of 
		a node in a certain "sequence", say (A->B->C), If your 'recursive' dfs traversal 
		is different from 'iterative' traversal, try reversing the sequence.  

	'''
	def __init__(self, problem):
		" Do not change this. " 
		# You'll save the actions that recursive dfs found in self.actions. 
		self.actions = [] 
		# Use self.explored to keep track of explored nodes.  
		self.explored = set()
		self.problem = problem

	def RecursiveDepthFirstSearchHelper(self, node):
		'''
		args: start node 
		outputs: bool => True if path found else Fasle.
		'''
		#mark node as visited
		self.explored.add(node)

		#test node for goal - return true if true
		if self.problem.isGoalState(node):
			return True

		#go to children
		for successor, action, cost in reversed(self.problem.getSuccessors(node)):
			
			if successor in self.explored:
				continue
			else:
				self.actions = self.actions + [action]

				if self.RecursiveDepthFirstSearchHelper(successor) == True:
					return True
				self.actions.pop()

		return False

def RecursiveDepthFirstSearch(problem):
	" You need not change this function. "
	# All your code should be in member function 'RecursiveDepthFirstSearchHelper' of 
	# class '_RecursiveDepthFirstSearch'."

	node = problem.getStartState() 
	rdfs = _RecursiveDepthFirstSearch(problem)
	path_found = rdfs.RecursiveDepthFirstSearchHelper(node)
	return list(rdfs.actions) # Actions your recursive calls return are in opposite order.
# ________________________________________________________________


def depthLimitedSearch(problem, limit = 130):

	"""
	Search the deepest nodes in the search tree first as long as the
	nodes are not not deeper than 'limit'.

	For medium maze, pacman should find food for limit less than 130. 
	If your solution needs 'limit' more than 130, it's bogus.
	Specifically, for:
	'python pacman.py -l mediumMaze -p SearchAgent -a fn=dls', and limit=130
	pacman should work normally.  

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.
	Autograder cannot test this function.  

	Hints: You may need to store additional information in your frontier(queue).

	"""

	#############################################
	#		LIMIT FOR MEDIUM MAZE IS 130		#
	#		LIMIT FOR BIG MAZE IS 210			#
	#############################################

	closed = []

	start_state = problem.getStartState()
	#storing the limit for every node, signifying the depth pf search allowed from here on
	start_item = (start_state, [], limit)

	stack = util.Stack()
	stack.push(start_item)

	while not stack.isEmpty():
		node, actions_list, stored_limit = stack.pop()
		new_limit = stored_limit - 1 #this variable stays the same for nodes belonging to that certain level

		if problem.isGoalState(node):
			return actions_list

		if new_limit >= 0: #only add successors if depth is allowed
			if node not in closed:
				closed = closed + [node]
			
				for successor, action, cost in problem.getSuccessors(node):
					actions = actions_list + [action]
					new_start_item = (successor, actions, new_limit)
					stack.push(new_start_item)

	return []

# ________________________________________________________________

class _RecursiveDepthLimitedSearch(object):
	'''
		=> Output of 'recursive' dfs should match that of 'iterative' dfs you implemented
		above. 
		Key Point: Remember in tutorial you were asked to expand the left-most child 
		first for dfs and bfs for consistency. If you expanded the right-most
		first, dfs/bfs would be correct in principle but may not return the same
		path. 

		=> Useful Hint: self.problem.getSuccessors(node) will return children of 
		a node in a certain "sequence", say (A->B->C), If your 'recursive' dfs traversal 
		is different from 'iterative' traversal, try reversing the sequence.  

	'''
	def __init__(self, problem):
		" Do not change this. " 
		# You'll save the actions that recursive dfs found in self.actions. 
		self.actions = [] 
		# Use self.explored to keep track of explored nodes.  
		self.explored = set()
		self.problem = problem
		self.current_depth = 0
		self.depth_limit = 210 # For medium maze, You should find solution for depth_limit not more than 204.

	def RecursiveDepthLimitedSearchHelper(self, node):
		'''
		args: start node 
		outputs: bool => True if path found else Fasle.
		'''

		#############################################
		#		LIMIT FOR MEDIUM MAZE IS 130		#
		#		LIMIT FOR BIG MAZE IS 210			#
		#############################################

		#mark node as visited
		self.explored.add(node)

		#test node for goal - return true if true
		if self.problem.isGoalState(node):
			return True

		#go to children
		for successor, action, cost in reversed(self.problem.getSuccessors(node)):
			
			if successor in self.explored:
				continue
			else:
				self.actions = self.actions + [action]
				self.current_depth = self.current_depth + 1

				if self.current_depth <= self.depth_limit:
					if self.RecursiveDepthLimitedSearchHelper(successor) == True:
						return True

				self.actions.pop()
				self.current_depth = self.current_depth - 1

		return False


def RecursiveDepthLimitedSearch(problem):
	"You need not change this function. All your code in member function RecursiveDepthLimitedSearchHelper"
	node = problem.getStartState() 
	rdfs = _RecursiveDepthLimitedSearch(problem)
	path_found = rdfs.RecursiveDepthLimitedSearchHelper(node)
	return list(rdfs.actions) # Actions your recursive calls return are in opposite order.
# ________________________________________________________________


def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""

	closed = []

	start_state = problem.getStartState()
	start_item = (start_state, [])

	queue = util.Queue()
	queue.push(start_item)

	while not queue.isEmpty():
		node, actions_list = queue.pop()

		if problem.isGoalState(node):
			return actions_list

		if node not in closed:
			closed = closed + [node]
		
			for successor, action, cost in problem.getSuccessors(node):
				actions = actions_list + [action]
				new_start_item = (successor, actions)
				queue.push(new_start_item)

	return []


def uniformCostSearch(problem):
	"""Search the node of least total cost first.
	   You may need to pay close attention to util.py.
	   Useful Reminder: Note that problem.getSuccessors(node) returns "step_cost". 

	   Key Point: If a node is already present in the queue with higher path cost 
	   (or higher priority), you'll update its cost (or priority) 
	   (Similar to pseudocode in figure 3.14 of your textbook.). 
	   Be careful, autograder cannot catch this bug.
	"""
	closed = []

	path_cost = 0
	start_state = problem.getStartState()
	start_item = (start_state, [])

	pq = util.PriorityQueue()
	pq.push(start_item, path_cost) 

	while not pq.isEmpty(): 
		item, node_path_cost = pq.pop()
		node = item[0]
		actions_list = item[1]

		if problem.isGoalState(node):
				return actions_list

		ret = pq.item_present_with_higher_priority(item, node_path_cost)
		if ret != None: #path found with a higher priority - needs to be updated
			pq.Update_priority(item, node_path_cost, ret[0], ret[1])

		if node not in closed: #if node has not been explored previously
			closed = closed + [node]

			for successor, action, step_cost in problem.getSuccessors(node):
				actions = actions_list + [action]
				path_cost = node_path_cost + step_cost
				new_start_item = (successor, actions)
				pq.push(new_start_item, path_cost)

	return []


def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	'''
	Pay close attention to util.py- specifically, args you pass to member functions. 

	Key Point: If a node is already present in the queue with higher path cost 
	(or higher priority), you'll update its cost (or priority) 
	(Similar to pseudocode in figure 3.14 of your textbook.). 
	Be careful, autograder cannot catch this bug.

	'''
	closed = []

	path_cost = 0
	start_state = problem.getStartState()
	start_item = (start_state, [], path_cost)

	pq = util.PriorityQueue()
	pq.push(start_item, heuristic(start_state, problem)) 

	while not pq.isEmpty(): 
		item = pq.pop()
		node = item[0][0]
		actions_list = item[0][1]
		node_path_cost = item[0][2]
		# print(item)
		# break

		if problem.isGoalState(node):
			return actions_list

		ret = pq.item_present_with_higher_priority(item, node_path_cost)
		if ret != None: #path found with a higher priority - needs to be updated
			pq.Update_priority(item, node_path_cost, ret[0], ret[1])

		if node not in closed: #if node has not been explored previously
			closed = closed + [node]

			for successor, action, step_cost in problem.getSuccessors(node):
				actions = actions_list + [action]
				new_path_cost = node_path_cost + step_cost
				#new_start_item = (successor, actions)
				new_start_item = (successor, actions, new_path_cost)
				pq.push(new_start_item, new_path_cost+heuristic(successor, problem))

	return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
rdfs = RecursiveDepthFirstSearch
dls = depthLimitedSearch
rdls = RecursiveDepthLimitedSearch
astar = aStarSearch
ucs = uniformCostSearch
