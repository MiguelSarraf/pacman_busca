# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        """
        Baseado nos slides de aula
        https://edisciplinas.usp.br/pluginfile.php/9583073/mod_resource/content/1/Aula18-PlanejmentoProbabilistico-Parte2_2026.pdf
        slide 21
        """

        # \forall s in S faça
        #    v0(s)<-r(s)
        # v0 começa inicializado com 0

        # n<-0
        n = 0

        # repita
        while True:
            #n<-n+1
            n += 1

            valores_novos = self.values.copy()
            # \forall s in S faça
            for estado in self.mdp.getStates():
                if self.mdp.isTerminal(estado):
                    valores_novos[estado] = self.mdp.getReward(estado, None, estado)
                    continue
                # \forall a in A faça
                novo_Q = None
                for acao in self.mdp.getPossibleActions(estado):
                    # qn(s, a)<-...
                    valor = self.computeQValueFromValues(estado, acao)
                    novo_Q = valor if novo_Q is None else max(novo_Q, valor)
                # vn(s)<-max_{a in A} qn(s, a)
                valores_novos[estado] = novo_Q
                # pin(s)<-argmax_{a in A} qn(s, a)
                # politica não precisa ser atualizada

            # até maximo de iterações
            if n > self.iterations:
                break
            self.values = valores_novos.copy()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        valor_Q = None
        # \forall s in S
        for proximo_estado, probabilidade in self.mdp.getTransitionStatesAndProbs(state, action):
            # T (s, a, s′) ∗ (r(s, a, s′) + γ ∗ V (s′))
            recompensa = self.mdp.getReward(state, action, proximo_estado)
            valor = probabilidade * (recompensa + self.discount * self.getValue(proximo_estado))
            valor_Q = valor if valor_Q is None else valor_Q + valor
        return valor_Q

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        max_Q = None
        acao_escolhida = None

        # \forall a in A
        for acao in self.mdp.getPossibleActions(state):
            valor_Q = self.computeQValueFromValues(state, acao)
            if max_Q is None or valor_Q > max_Q:
                max_Q = valor_Q
                acao_escolhida = acao

        return acao_escolhida

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
