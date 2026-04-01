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

def verifica_se_esta_na_borda(no_teste, borda):
	for nos in borda.list:
		no, solucao = nos
		if no == no_teste:
			return True
	return False

def depthFirstSearch(problem: SearchProblem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print("Start:", problem.getStartState())
	print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
	print("Start's successors:", problem.getSuccessors(problem.getStartState()))

	Solução adaptada de https://edisciplinas.usp.br/pluginfile.php/9483368/mod_resource/content/2/Aula4-busca-cega-2026.pdf slide 80
	Acessado em 31/03/2026
	"""
	#nó ← um nó com custoCaminho=0 e estado igual a problema.ESTADO-INICIAL
	no = problem.getStartState()
	estado = problem.getStartState()
	#borda ← INSIRA(nó,borda)
	borda = util.Stack()
	borda.push((no, []))
	#explorado ← conjunto vazio
	explorado = set()
	#repita
	while True:
		#se VAZIA(borda) então devolve falha
		if borda.isEmpty():
			raise ValueError("Nenhuma solução encontrada!")
		#nó ← REMOVE(borda)
		no, solucao = borda.pop()
		#se problema.TESTE-META(filho.ESTADO) então devolve solução(filho)
		filhos = problem.getSuccessors(no)
		for filho in filhos:
			filho_no, filho_acao, filho_custo = filho
			if problem.isGoalState(filho_no):
				return solucao + [filho_acao]
		#explorado ← INSIRA(nó.ESTADO, explorado)
		explorado.add(no)
		#para cada ação em problema.AÇÕES(nó.ESTADO) faça
		#filho ← NO-FILHO(problema, nó, ação)
		for filho in filhos:
			filho_no, filho_acao, filho_custo = filho
			#se (filho.ESTADO) não está em explorado ou borda então
			if filho_no not in explorado and not verifica_se_esta_na_borda(filho_no, borda):
				#borda ← INSIRA (filho, borda)
				borda.push((filho_no, solucao + [filho_acao]))

def breadthFirstSearch(problem: SearchProblem):
	"""Search the shallowest nodes in the search tree first.

	Solução adaptada de https://edisciplinas.usp.br/pluginfile.php/9483368/mod_resource/content/2/Aula4-busca-cega-2026.pdf slide 36
	Acessado em 31/03/2026
	"""
	#nó ← um nó com custoCaminho=0 e estado igual a problema.ESTADO-INICIAL
	no = problem.getStartState()
	estado = problem.getStartState()
	#Se problema.TESTE-META(nó.ESTADO) devolve SOLUÇÃO(nó)
	if problem.isGoalState(no):
		return []
	#borda ← INSIRA(nó,borda)
	borda = util.Queue()
	borda.push((no, []))
	#explorado ← conjunto vazio
	explorado = set()
	#repita
	while True:
		#se VAZIA(borda) então devolve falha
		if borda.isEmpty():
			raise ValueError("Nenhuma solução encontrada!")
		#nó ← REMOVE(borda)
		no, solucao = borda.pop()
		#explorado ← INSIRA(nó.ESTADO, explorado)
		explorado.add(no)
		#para cada ação em problema.AÇÕES(nó.ESTADO) faça
		#filho ← NO-FILHO(problema, nó, ação)
		filhos = problem.getSuccessors(no)
		for filho in filhos:
			filho_no, filho_acao, filho_custo = filho
			#se (filho.ESTADO) não está em explorado ou borda então
			if filho_no not in explorado and not verifica_se_esta_na_borda(filho_no, borda):
				#se problema.TESTE-META(filho.ESTADO) então devolve solução (nó-filho)
				if problem.isGoalState(filho_no):
					return solucao + [filho_acao]
				#borda ← INSIRA (filho, borda)
				borda.push((filho_no, solucao + [filho_acao]))

def uniformCostSearch(problem: SearchProblem):
	"""Search the node of least total cost first."""
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()

# Códigos obrigatórios para a pós-graduação:

def iddfsSearch(problem: SearchProblem):
	"""Search the deepest nodes in the search tree first, limited by an iteratively increasing depth.
	Create an additional function if needed.
	"""
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()

def lrtaStarSearch(problem, heuristic=nullHeuristic):
	"""Execute a number of trials of LRTA* and return the best plan found."""
	"*** ADD YOUR CODE HERE ***"
	util.raiseNotDefined()
	# MAXTRIALS = ...


# Abbreviations
# *** DO NOT CHANGE THESE ***
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
iddfs = iddfsSearch
lrta = lrtaStarSearch
