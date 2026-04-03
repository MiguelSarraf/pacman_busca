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
import os

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
		no = nos[0]
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
		#se problema.TESTE-META(nó) então devolve solução (nó)
		if problem.isGoalState(no):
			return solucao
		filhos = problem.getSuccessors(no)
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
		#se problema.TESTE-META(nó) então devolve solução (nó)
		if problem.isGoalState(no):
			return solucao
		#explorado ← INSIRA(nó.ESTADO, explorado)
		explorado.add(no)
		#para cada ação em problema.AÇÕES(nó.ESTADO) faça
		#filho ← NO-FILHO(problema, nó, ação)
		filhos = problem.getSuccessors(no)
		for filho in filhos:
			filho_no, filho_acao, filho_custo = filho
			#se (filho.ESTADO) não está em explorado ou borda então
			if filho_no not in explorado and not verifica_se_esta_na_borda(filho_no, borda):
				#borda ← INSIRA (filho, borda)
				borda.push((filho_no, solucao + [filho_acao]))

def uniformCostSearch(problem: SearchProblem):
	"""Search the node of least total cost first.

	Solução adaptada de https://edisciplinas.usp.br/pluginfile.php/9483368/mod_resource/content/2/Aula4-busca-cega-2026.pdf slide 56
	Acessado em 31/03/2026
	"""
	#nó ← cria um nó com custoCaminho=0 e ESTADO= problema.ESTADO-INICIAL
	no = problem.getStartState()
	custo = 0
	estado = problem.getStartState()
	#borda ← fila de prioridade ordenada pelo CUSTO-DE-CAMINHO, contendo nó
	borda = util.PriorityQueue()
	borda.push((no, []), custo)
	#explorado ← conjunto vazio
	explorado = set()
	#repita
	while True:
		#se VAZIO?(borda) então devolve falha
		if borda.isEmpty():
			raise ValueError("Nenhuma solução encontrada!")
		#nó ← REMOVE(borda)
		no, solucao = borda.pop()
		#se problema.TESTE-META(nó.ESTADO) então devolve SOLUÇÃO(nó)
		if problem.isGoalState(no):
			return solucao
		#adicionar (nó.ESTADO) para explorado
		explorado.add(no)
		#para cada ação em problema.AÇÕES(nó.ESTADO) faça
		#filho ← GERA-NÓ-FILHO(problema, nó, ação)
		filhos = problem.getSuccessors(no)
		for filho in filhos:
			filho_no, filho_acao, filho_custo = filho
			#se (filho.ESTADO) não está na borda ou explorado então
			#	borda ← INSIRA (filho, borda)
			#senão se (filho.ESTADO) está na borda com CUSTO-DE-CAMINHO maior
			#	então substituir aquele nó borda por filho
			#O comportamento de atualização de custo está todo pré-pronto no método update da PriorityQueue
			if filho_no not in explorado:
				borda.update((filho_no, solucao + [filho_acao]), filho_custo+1)

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first.

	Solução adaptada de https://edisciplinas.usp.br/pluginfile.php/9492271/mod_resource/content/4/Aula5-Astar-2026.pdf
	Acessado em 01/04/2026"""
	#nó ← cria um nó com custoCaminho=0 e ESTADO= problema.ESTADO-INICIAL
	no = problem.getStartState()
	custo = 0
	estado = problem.getStartState()
	#borda ← fila de prioridade ordenada pelo CUSTO-DE-CAMINHO, contendo nó
	borda = util.PriorityQueue()
	borda.push((no, []), custo)
	#explorado ← conjunto vazio
	explorado = set()
	#repita
	while True:
		#se VAZIO?(borda) então devolve falha
		if borda.isEmpty():
			raise ValueError("Nenhuma solução encontrada!")
		#nó ← REMOVE(borda)
		no, solucao = borda.pop()
		#se problema.TESTE-META(nó.ESTADO) então devolve SOLUÇÃO(nó)
		if problem.isGoalState(no):
			return solucao
		#adicionar (nó.ESTADO) para explorado
		explorado.add(no)
		#para cada ação em problema.AÇÕES(nó.ESTADO) faça
		#filho ← GERA-NÓ-FILHO(problema, nó, ação)
		filhos = problem.getSuccessors(no)
		for filho in filhos:
			filho_no, filho_acao, filho_custo = filho
			#Adiciona filhos na fila de acordo com heurística calculada
			if filho_no not in explorado:
				heuristica = heuristic(filho_no, problem)
				ordem = filho_custo + heuristica
				borda.update((filho_no, solucao + [filho_acao]), ordem)

# Códigos obrigatórios para a pós-graduação:

def dlsSearch(problem: SearchProblem, limite: int):
	"""Search the deepest nodes in the search tree first limited to limite length.

	Solução adaptada de https://edisciplinas.usp.br/pluginfile.php/9483368/mod_resource/content/2/Aula4-busca-cega-2026.pdf slide 95 e solução para busca em profundidade.
	Acessado em 01/04/2026"""
	#nó ← um nó com custoCaminho=0 e estado igual a problema.ESTADO-INICIAL
	no = problem.getStartState()
	estado = problem.getStartState()
	#borda ← INSIRA(nó,borda)
	borda = util.Stack()
	borda.push((no, [], 0))
	#explorado ← conjunto vazio
	explorado = set()
	#repita
	while True:
		#se VAZIA(borda) então devolve falha
		if borda.isEmpty():
			raise ValueError("Nenhuma solução encontrada!")
		#nó ← REMOVE(borda)
		no, solucao, profundidade = borda.pop()
		#se profundidade > limite então devolve falha
		if profundidade > limite:
			raise ValueError(f"Limite de profundidade atingido: {limite}")
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
				borda.push((filho_no, solucao + [filho_acao], profundidade + 1))

def iddfsSearch(problem: SearchProblem):
	"""Search the deepest nodes in the search tree first, limited by an iteratively increasing depth.

	Solução adaptada de https://edisciplinas.usp.br/pluginfile.php/9483368/mod_resource/content/2/Aula4-busca-cega-2026.pdf slide 105 e solução para busca em profundidade.
	Acessado em 01/04/2026
	"""
	limite = 1
	while True:
		try:
			resultado = dlsSearch(problem, limite)
			return resultado
		except:
			limite += 1

def busca_espaco_de_heuristicas(heuristica, estado, paredes, problema):
	altura = paredes.height
	largura = paredes.width
	heuristica_inicial = {}
	for i in range(largura):
		for j in range(altura):
			if paredes[i][j]:
				continue
			heuristica_inicial[(i, j)] = heuristica((i,j), problema)
	return heuristica_inicial

def salvar_matriz_txt(dados, paredes, caminho_arquivo):
	"""
	dados: dict com chaves (x, y) e valores numéricos
	max_x: maior valor de x (inclusive)
	max_y: maior valor de y (inclusive)
	caminho_arquivo: caminho do arquivo de saída
	"""
	max_y = paredes.height
	max_x = paredes.width

	with open(caminho_arquivo, "w") as f:
		for y in range(max_y):
			linha = []
			for x in range(max_x):
				valor = dados.get((x, max_y - y - 1), "X")
				linha.append(str(valor))
			f.write(",".join(linha) + "\n")

def lrtaStarSearch(problem, heuristic=nullHeuristic):
	"""Execute a number of trials of LRTA* and return the best plan found.

	Solução adaptada de https://arxiv.org/pdf/1110.4076 figura 2.
	Acessado em 02/04/2026"""
	#initialize the heuristic: h ← h0
	heuristica = busca_espaco_de_heuristicas(heuristic, problem.getStartState(), problem.walls, problem)
	trials = int(os.environ.get("NUM_TRIALS", 10))
	trial = 0
	while trial < trials:
		#reset the current state: s ← sstart
		no = problem.getStartState()
		#while s not∈ Sg do
		solucao = []
		passo=1
		while True:
			if problem.isGoalState(no):
				break
			#generate children one move away from state s
			filhos = problem.getSuccessors(no)
			#find the state s with the lowest f = g + h
			custo_meta = 100000000000
			filho_prodigo = None
			proxima_acao = None
			for filho in filhos:
				filho_no, filho_acao, filho_custo = filho
				if heuristica[filho_no] < custo_meta:
					custo_meta = heuristica[filho_no]
					custo_proximo = filho_custo
					filho_prodigo = filho_no
					proxima_acao = filho_acao
			#update h(s) to f(s') if f(s') is greater
			if heuristica[filho_prodigo] + custo_proximo > heuristica[no]:
				heuristica[no] = heuristica[filho_prodigo] + custo_proximo
			#execute the action to get to s
			#input(proxima_acao+"\n")
			no = filho_prodigo
			solucao.append(proxima_acao)
			passo+=1
		trial+=1
	salvar_matriz_txt(heuristica, problem.walls, "heuristicas.csv")
	print(f"Custo estimado do estado inicial: {heuristica[problem.getStartState()]}")
	return solucao


# Abbreviations
# *** DO NOT CHANGE THESE ***
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
iddfs = iddfsSearch
lrta = lrtaStarSearch
