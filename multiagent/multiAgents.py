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

"""
===============================================================
====================== IMPLEMENTAÇÃO EP2 ======================
===============================================================
=============== Miguel Sarraf Ferreira Santucci ===============
======================== NUSP 10336827 ========================
===============================================================
"""


from util import manhattanDistance
from game import Directions
import random, util
from numpy import inf as infinito

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction'):
        self.evaluationFunction = util.lookup(evalFn, globals())

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        successors = [(gameState.generatePacmanSuccessor(action)) for action in legalMoves]
        scores = [self.evaluationFunction(succesor) for successors in successors]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

def scoreEvaluationFunction(currentGameState: GameState):
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
    Your minimax agent (question 1)

    Implementado baseado no slide 54 da aula 10 e realizados ajustes finos na lógica para comportar multiagentes.
    http://edisciplinas.usp.br/pluginfile.php/9530457/mod_resource/content/1/Aula10-JogoAdversarial-I-2026.pdf
    """
    def gera_lista_de_fantasminhas(self, estado):
        lista_de_fantasminhas = [i for i in range(1, estado.getNumAgents())]
        return lista_de_fantasminhas

    def teste_termino(self, estado, profundidade):
        if profundidade>self.depth: return True
        if estado.isWin(): return True
        if estado.isLose(): return True
        return False

    def valor_max(self, estado, profundidade=1):
        #se TESTE DE TÉRMINO(estado) então devolver UTILIDADE(estado)
        if self.teste_termino(estado, profundidade):
            return self.evaluationFunction(estado)
        #v ← -∞
        v = -infinito
        #Para cada a em AÇÕES(estado) faça
        pacman_indice = 0
        acoes_possiveis = estado.getLegalActions(pacman_indice)
        for acao in acoes_possiveis:
            #RESULTADO(s,a)
            proximo_estado = estado.generateSuccessor(pacman_indice, acao)
            #v ← MAX(v,VALOR-MIN(RESULTADO(s,a)))
            lista_de_fantasminhas = self.gera_lista_de_fantasminhas(estado)
            avaliacao = self.valor_min(proximo_estado, lista_de_fantasminhas, profundidade)
            v = max(v, avaliacao)
        return v

    def valor_min(self, estado, lista_de_fantasminhas, profundidade=1):
        #se TESTE DE TÉRMINO(estado) então devolver UTILIDADE(estado)
        if self.teste_termino(estado, profundidade):
            return self.evaluationFunction(estado)
        fantasminha = lista_de_fantasminhas[0]
        outros_fantasminhas = lista_de_fantasminhas[1:]
        #v ← ∞
        v = infinito
        #Para cada a em AÇÕES(estado) faça
        acoes_possiveis = estado.getLegalActions(fantasminha)
        for acao in acoes_possiveis:
            #RESULTADO(s,a)
            proximo_estado = estado.generateSuccessor(fantasminha, acao)
            if outros_fantasminhas:
                #Se ainda houverem fantasminhas, faz outro valor minimo, antes do pacman jogar de novo
                avaliacao = self.valor_min(proximo_estado, outros_fantasminhas, profundidade)
            else:
                #v ← MIN(v,VALOR-MAX(RESULTADO(s,a)))
                #Profundidade só aumenta se for uma jogada do Pacman (essa foi difícil de decifrar)
                avaliacao = self.valor_max(proximo_estado, profundidade+1)
            v = min(v, avaliacao)
        return v

    def getAction(self, gameState: GameState):
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

        Essa função é semelhante à DECISÃO-MINIMAX do slide
        """
        # A ação buscada é sempre a do pacman
        pacman_indice = 0
        #a ∊ ações(s)
        acoes_possiveis = gameState.getLegalActions(pacman_indice)
        valores = []
        for acao in acoes_possiveis:
            #RESULTADO(estado,a)
            proximo_estado = gameState.generateSuccessor(pacman_indice, acao)
            #VALOR-MIN(RESULTADO(estado,a))
            lista_de_fantasminhas = self.gera_lista_de_fantasminhas(gameState)
            valores.append(self.valor_min(proximo_estado, lista_de_fantasminhas))
        #argmax_{a ∊ ações(s)} VALOR-MIN(RESULTADO(estado,a))
        return acoes_possiveis[valores.index(max(valores))]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)

    Implementado baseado nos slides 99 e 100 da aula 10 e realizados ajustes finos na lógica para comportar multiagentes.
    http://edisciplinas.usp.br/pluginfile.php/9530457/mod_resource/content/1/Aula10-JogoAdversarial-I-2026.pdf
    """
    def gera_lista_de_fantasminhas(self, estado):
        lista_de_fantasminhas = [i for i in range(1, estado.getNumAgents())]
        return lista_de_fantasminhas

    def teste_termino(self, estado, profundidade):
        if profundidade>self.depth: return True
        if estado.isWin(): return True
        if estado.isLose(): return True
        return False

    def valor_max(self, estado, alfa, beta, profundidade=1, volta_acao=False):
        #se TESTE DE TÉRMINO(estado) então devolver UTILIDADE(estado)
        if self.teste_termino(estado, profundidade):
            return self.evaluationFunction(estado)
        #v ← -∞
        v = -infinito
        #Para cada a em AÇÕES(estado) faça
        pacman_indice = 0
        acoes_possiveis = estado.getLegalActions(pacman_indice)
        acao_escolhida = None
        for acao in acoes_possiveis:
            #RESULTADO(s,a)
            proximo_estado = estado.generateSuccessor(pacman_indice, acao)
            #v ← MAX(v,VALOR-MIN(RESULTADO(s,a)))
            lista_de_fantasminhas = self.gera_lista_de_fantasminhas(estado)
            avaliacao = self.valor_min(proximo_estado, lista_de_fantasminhas, alfa, beta, profundidade)
            v = max(v, avaliacao)
            if v == avaliacao:
                acao_escolhida = acao
            #se v>=β então devolve v
            #Conforme instruído no enunciado, não deve ser feito teste de igualdade
            if v > beta:
                break
            #α ← MAX(α,v)
            alfa = max(alfa, v)
        if volta_acao:
            return v, acao_escolhida
        return v

    def valor_min(self, estado, lista_de_fantasminhas, alfa, beta, profundidade=1):
        #se TESTE DE TÉRMINO(estado) então devolver UTILIDADE(estado)
        if self.teste_termino(estado, profundidade):
            return self.evaluationFunction(estado)
        fantasminha = lista_de_fantasminhas[0]
        outros_fantasminhas = lista_de_fantasminhas[1:]
        #v ← ∞
        v = infinito
        #Para cada a em AÇÕES(estado) faça
        acoes_possiveis = estado.getLegalActions(fantasminha)
        for acao in acoes_possiveis:
            #RESULTADO(s,a)
            proximo_estado = estado.generateSuccessor(fantasminha, acao)
            if outros_fantasminhas:
                #Se ainda houverem fantasminhas, faz outro valor minimo, antes do pacman jogar de novo
                avaliacao = self.valor_min(proximo_estado, outros_fantasminhas, alfa, beta, profundidade)
            else:
                #v ← MIN(v,VALOR-MAX(RESULTADO(s,a)))
                #Profundidade só aumenta se for uma jogada do Pacman (essa foi difícil de decifrar)
                avaliacao = self.valor_max(proximo_estado, alfa, beta, profundidade+1)
            v = min(v, avaliacao)
            #se v<=α então devolve v
            #Conforme instruído no enunciado, não deve ser feito teste de igualdade
            if v < alfa:
                break
            #β ← MIN(β, v)
            beta = min(beta, v)
        return v

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction

        Essa função é semelhante à  BUSCA-ALFA-BETA do slide
        """
        #v ← VALOR-MAX(estado, -∞, + ∞)
        v, a = self.valor_max(gameState, -infinito, infinito, volta_acao=True)
        #devolver a ação em AÇÕES(estado) com valor v
        return a

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)

    Implementado baseado na implementação do minimax e no slide 6 da aula 11 e realizados ajustes finos na lógica para comportar multiagentes.
    https://edisciplinas.usp.br/pluginfile.php/9530833/mod_resource/content/3/Aula11-JogoAdversarial-II-2026.pdf
    """
    def gera_lista_de_fantasminhas(self, estado):
        lista_de_fantasminhas = [i for i in range(1, estado.getNumAgents())]
        return lista_de_fantasminhas

    def teste_termino(self, estado, profundidade):
        if profundidade>self.depth: return True
        if estado.isWin(): return True
        if estado.isLose(): return True
        return False

    def valor_max(self, estado, profundidade=1):
        #se TESTE DE TÉRMINO(estado) então devolver UTILIDADE(estado)
        if self.teste_termino(estado, profundidade):
            return self.evaluationFunction(estado)
        #v ← -∞
        v = -infinito
        #Para cada a em AÇÕES(estado) faça
        pacman_indice = 0
        acoes_possiveis = estado.getLegalActions(pacman_indice)
        for acao in acoes_possiveis:
            #RESULTADO(s,a)
            proximo_estado = estado.generateSuccessor(pacman_indice, acao)
            #v ← MAX(v,VALOR-MIN(RESULTADO(s,a)))
            lista_de_fantasminhas = self.gera_lista_de_fantasminhas(estado)
            avaliacao = self.valor_min(proximo_estado, lista_de_fantasminhas, profundidade)
            v = max(v, avaliacao)
        return v

    def valor_min(self, estado, lista_de_fantasminhas, profundidade=1):
        #se TESTE DE TÉRMINO(estado) então devolver UTILIDADE(estado)
        if self.teste_termino(estado, profundidade):
            return self.evaluationFunction(estado)
        fantasminha = lista_de_fantasminhas[0]
        outros_fantasminhas = lista_de_fantasminhas[1:]
        #initialize v = 0
        v = 0
        #for each successor of state:
        acoes_possiveis = estado.getLegalActions(fantasminha)
        num_acoes = len(acoes_possiveis)
        for acao in acoes_possiveis:
            #RESULTADO(s,a)
            proximo_estado = estado.generateSuccessor(fantasminha, acao)
            if outros_fantasminhas:
                #Se ainda houverem fantasminhas, faz outro valor minimo, antes do pacman jogar de novo
                avaliacao = self.valor_min(proximo_estado, outros_fantasminhas, profundidade)
            else:
                #Profundidade só aumenta se for uma jogada do Pacman (essa foi difícil de decifrar)
                avaliacao = self.valor_max(proximo_estado, profundidade+1)
            #v += p * value(successor)
            #Como p=1/(possibilidades de ação), a divisão foi passada para o final do processamento
            v += avaliacao
        v /= num_acoes
        return v

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.

        Essa função é semelhante à DECISÃO-MINIMAX do slide
        """
        # A ação buscada é sempre a do pacman
        pacman_indice = 0
        #a ∊ ações(s)
        acoes_possiveis = gameState.getLegalActions(pacman_indice)
        valores = []
        for acao in acoes_possiveis:
            #RESULTADO(estado,a)
            proximo_estado = gameState.generateSuccessor(pacman_indice, acao)
            #VALOR-MIN(RESULTADO(estado,a))
            lista_de_fantasminhas = self.gera_lista_de_fantasminhas(gameState)
            valores.append(self.valor_min(proximo_estado, lista_de_fantasminhas))
        #argmax_{a ∊ ações(s)} VALOR-MIN(RESULTADO(estado,a))
        return acoes_possiveis[valores.index(max(valores))]

def betterEvaluationFunction(currentGameState: GameState):
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    score = currentGameState.getScore()
    # Incentive to get food
    if food:
        # Minimize distanace to closest food
        minFoodDist = min(manhattanDistance(pos, f) for f in food)
        score += 10.0 / (minFoodDist + 1)
        # Minimize remaining food
        score -= 4 * len(food)
    # Avoid ghosts
    for ghost in ghosts:
        ghostPos = ghost.getPosition()
        dist = manhattanDistance(pos, ghostPos)
        # Get closer to scared ghosts
        if ghost.scaredTimer > 0:
            score += 20.0 / (dist + 1)
        else:
            if dist <= 1:
                # Avoid immediate death
                score -= 500
            else:
                # Get away from ghosts
                score -= 2.0 / dist
    return score

# Abbreviation
better = betterEvaluationFunction
